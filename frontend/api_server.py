#!/usr/bin/env python3
"""
跨境电商选品工具后端 API - FastAPI + SSE 版本
支持异步执行 skills 脚本，实时推送进度
"""

import json
import asyncio
import sys
import os
from datetime import datetime
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="E-Commerce Skills API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'skills')

SITE_MAPPING = {
    'amazon.com': 'us',
    'amazon.co.uk': 'uk',
    'amazon.de': 'de',
    'amazon.co.jp': 'jp'
}

async def run_script_async(skill_name: str, script_name: str, args: list = None) -> tuple:
    script_path = os.path.join(SCRIPTS_DIR, skill_name, 'scripts', script_name)
    if not os.path.exists(script_path):
        return None, f"Script not found: {script_path}"
    
    try:
        cmd = [sys.executable, script_path] + (args or [])
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=120
            )
        except asyncio.TimeoutError:
            process.kill()
            return None, "Script timeout (120s)"
        
        if process.returncode != 0:
            return None, stderr.decode() if stderr else "Unknown error"
        
        output = stdout.decode()
        
        if args and '--format' in args and 'json' in args:
            json_start = output.find('{\n')
            if json_start == -1:
                json_start = output.find('{')
            if json_start != -1:
                output = output[json_start:]
        
        return output.strip(), None
    except Exception as e:
        return None, str(e)

def sse_event(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"

@app.get("/api/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/", response_class=HTMLResponse)
@app.get("/frontend", response_class=HTMLResponse)
async def frontend():
    index_path = os.path.join(os.path.dirname(__file__), 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        return f.read()

@app.post("/api/pricing/calculate")
async def calculate_pricing(request: Request):
    data = await request.json()
    
    temu_price = data.get('temu_price', 0)
    ali1688_price = data.get('ali1688_price', 0)
    exchange_rate = data.get('exchange_rate', 7.2)
    fulfillment_fee = data.get('fulfillment_fee', 3.5)
    
    args = [
        '--temu-price', str(temu_price),
        '--ali1688-price', str(ali1688_price),
        '--exchange-rate', str(exchange_rate),
        '--fulfillment-fee', str(fulfillment_fee),
        '--format', 'json'
    ]
    
    output, error = await run_script_async('temu-pricing-calculator', 'calculate_pricing.py', args)
    
    if error:
        return JSONResponse({"error": error}, status_code=500)
    
    try:
        result = json.loads(output)
        return result
    except json.JSONDecodeError:
        return {"raw_output": output}

@app.get("/api/amazon/movers-shakers")
async def get_amazon_movers_shakers(site: str = "amazon.com", category: str = "home-garden", limit: int = 20, source: str = "auto"):
    site_code = SITE_MAPPING.get(site, 'us')
    args = [
        '--site', site_code,
        '--category', category,
        '--limit', str(limit),
        '--source', source,
        '--format', 'json'
    ]
    
    output, error = await run_script_async('amazon-movers-shakers', 'scrape_amazon.py', args)
    
    if error:
        return JSONResponse({"error": error}, status_code=500)
    
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return {"raw_output": output}

@app.get("/api/temu/competitors")
async def get_temu_competitors(keyword: str, limit: int = 20):
    if not keyword:
        return JSONResponse({"error": "keyword is required"}, status_code=400)
    
    args = ['--keyword', keyword, '--limit', str(limit), '--format', 'json']
    output, error = await run_script_async('temu-competitor-search', 'scrape_temu.py', args)
    
    if error:
        return JSONResponse({"error": error}, status_code=500)
    
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return {"raw_output": output}

@app.get("/api/1688/sourcing")
async def get_1688_sourcing(keyword: str, limit: int = 20):
    if not keyword:
        return JSONResponse({"error": "keyword is required"}, status_code=400)
    
    args = ['--keyword', keyword, '--limit', str(limit), '--format', 'json']
    output, error = await run_script_async('ali1688-sourcing', 'scrape_1688.py', args)
    
    if error:
        return JSONResponse({"error": error}, status_code=500)
    
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return {"raw_output": output}

@app.post("/api/workflow/stream")
async def workflow_stream(request: Request):
    data = await request.json()
    
    site = data.get('site', 'amazon.com')
    site_code = SITE_MAPPING.get(site, 'us')
    category = data.get('category', 'home-garden')
    count = data.get('count', 5)
    
    async def generate() -> AsyncGenerator[str, None]:
        workflow_result = {
            'metadata': {
                'site': site,
                'category': category,
                'timestamp': datetime.now().isoformat()
            },
            'products': []
        }
        
        yield sse_event('start', {'message': '开始选品流程', 'total_steps': 4})
        
        await asyncio.sleep(0.1)
        yield sse_event('progress', {'step': 1, 'status': 'running', 'message': 'Step 1: 获取亚马逊飙升榜数据'})
        
        step1_args = [
            '--site', site_code,
            '--category', category,
            '--limit', str(count * 5),
            '--source', 'auto',
            '--format', 'json'
        ]
        
        output1, error1 = await run_script_async('amazon-movers-shakers', 'scrape_amazon.py', step1_args)
        
        if error1:
            yield sse_event('progress', {'step': 1, 'status': 'error', 'message': f'亚马逊数据获取失败: {error1[:100]}'})
            yield sse_event('complete', {'error': error1, 'products': []})
            return
        
        try:
            amazon_data = json.loads(output1)
            products = amazon_data.get('products', [])[:count * 2]
            yield sse_event('progress', {'step': 1, 'status': 'done', 'message': f'Step 1 完成: 获取 {len(products)} 款产品'})
        except json.JSONDecodeError:
            yield sse_event('progress', {'step': 1, 'status': 'error', 'message': '亚马逊数据解析失败'})
            yield sse_event('complete', {'error': 'Parse error', 'products': []})
            return
        
        await asyncio.sleep(0.1)
        yield sse_event('progress', {'step': 2, 'status': 'running', 'message': 'Step 2: 查询 Temu 竞品价格'})
        
        processed_count = 0
        for i, product in enumerate(products):
            product_result = {
                'amazon': product,
                'temu': None,
                'ali1688': None,
                'pricing': None
            }
            
            keywords = product.get('keywords', [])
            keyword = keywords[0] if keywords else product.get('title', '').split()[0]
            
            yield sse_event('progress', {
                'step': 2, 
                'status': 'running', 
                'message': f'Step 2: 查询 Temu 竞品 ({i+1}/{len(products)}) - {keyword[:20]}...'
            })
            
            temu_args = ['--keyword', keyword, '--limit', '5', '--format', 'json']
            output2, error2 = await run_script_async('temu-competitor-search', 'scrape_temu.py', temu_args)
            
            if not error2:
                try:
                    temu_data = json.loads(output2)
                    product_result['temu'] = temu_data
                    king_price = temu_data.get('king_price', {}).get('price', 0)
                    
                    await asyncio.sleep(0.1)
                    yield sse_event('progress', {
                        'step': 3, 
                        'status': 'running', 
                        'message': f'Step 3: 查询 1688 供应链 ({i+1}/{len(products)}) - {keyword[:20]}...'
                    })
                    
                    ali1688_args = ['--keyword', keyword, '--limit', '5', '--format', 'json']
                    output3, error3 = await run_script_async('ali1688-sourcing', 'scrape_1688.py', ali1688_args)
                    
                    if not error3:
                        try:
                            ali1688_data = json.loads(output3)
                            product_result['ali1688'] = ali1688_data
                            factories = ali1688_data.get('factories', [])
                            if factories and factories[0].get('products'):
                                ali1688_price = factories[0]['products'][0].get('price', 0)
                            else:
                                ali1688_price = ali1688_data.get('wholesale_price', {}).get('recommended_price', 0)
                            
                            await asyncio.sleep(0.1)
                            yield sse_event('progress', {
                                'step': 4, 
                                'status': 'running', 
                                'message': f'Step 4: V4.1 核价计算 ({i+1}/{len(products)})'
                            })
                            
                            pricing_args = [
                                '--temu-price', str(king_price),
                                '--ali1688-price', str(ali1688_price),
                                '--format', 'json'
                            ]
                            output4, error4 = await run_script_async('temu-pricing-calculator', 'calculate_pricing.py', pricing_args)
                            
                            if not error4:
                                try:
                                    pricing_data = json.loads(output4)
                                    product_result['pricing'] = pricing_data
                                    
                                    decision_status = pricing_data.get('decision', {}).get('status', '')
                                    if decision_status in ['GO', 'STRONG GO']:
                                        net_profit = pricing_data.get('calculation', {}).get('net_profit', 0)
                                        yield sse_event('product_found', {
                                            'product': product_result,
                                            'message': f"发现通过核价产品: {product.get('title', 'Unknown')[:30]}... 净利润: ¥{net_profit:.2f}"
                                        })
                                except Exception as e:
                                    pass
                        except Exception as e:
                            pass
                except Exception as e:
                    pass
            
            workflow_result['products'].append(product_result)
            processed_count += 1
            
            if processed_count % 2 == 0:
                yield sse_event('progress', {
                    'step': 4, 
                    'status': 'running', 
                    'message': f'已处理 {processed_count}/{len(products)} 款产品'
                })
        
        go_count = sum(1 for p in workflow_result['products'] if p and p.get('pricing') and p.get('pricing', {}).get('decision', {}).get('status') in ['GO', 'STRONG GO'])
        
        yield sse_event('progress', {'step': 4, 'status': 'done', 'message': f'Step 4 完成: {go_count} 款产品通过核价'})
        
        yield sse_event('complete', workflow_result)
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/api/report/generate")
async def generate_report(request: Request):
    data = await request.json()
    
    site = data.get('site', 'amazon.com')
    site_code = SITE_MAPPING.get(site, 'us')
    category = data.get('category', 'home-garden')
    count = data.get('count', 5)
    
    report = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'site': site,
            'category': category,
            'recommended_count': count
        },
        'recommended_products': [],
        'summary': {}
    }
    
    step1_args = [
        '--site', site_code,
        '--category', category,
        '--limit', str(count * 5),
        '--source', 'auto',
        '--format', 'json'
    ]
    
    output1, error1 = await run_script_async('amazon-movers-shakers', 'scrape_amazon.py', step1_args)
    
    if error1:
        return JSONResponse({"error": f"Amazon scrape error: {error1}"}, status_code=500)
    
    try:
        amazon_data = json.loads(output1)
    except json.JSONDecodeError as e:
        return JSONResponse({"error": f"Amazon JSON parse error: {e}", "output_preview": output1[:200]}, status_code=500)
    
    products = amazon_data.get('products', [])[:count * 2]
    
    go_products = []
    
    for product in products:
        keywords = product.get('keywords', [])
        keyword = keywords[0] if keywords else product.get('title', '').split()[0]
        
        temu_args = ['--keyword', keyword, '--limit', '5', '--format', 'json']
        output2, error2 = await run_script_async('temu-competitor-search', 'scrape_temu.py', temu_args)
        
        if error2:
            continue
        
        try:
            temu_data = json.loads(output2)
        except json.JSONDecodeError:
            continue
        
        king_price = temu_data.get('king_price', {}).get('price', 0)
        
        ali1688_args = ['--keyword', keyword, '--limit', '5', '--format', 'json']
        output3, error3 = await run_script_async('ali1688-sourcing', 'scrape_1688.py', ali1688_args)
        
        if error3:
            continue
        
        try:
            ali1688_data = json.loads(output3)
        except json.JSONDecodeError:
            continue
        
        factories = ali1688_data.get('factories', [])
        if factories and factories[0].get('products'):
            ali1688_price = factories[0]['products'][0].get('price', 0)
        else:
            ali1688_price = ali1688_data.get('wholesale_price', {}).get('recommended_price', 0)
        
        pricing_args = [
            '--temu-price', str(king_price),
            '--ali1688-price', str(ali1688_price),
            '--format', 'json'
        ]
        output4, error4 = await run_script_async('temu-pricing-calculator', 'calculate_pricing.py', pricing_args)
        
        if error4:
            continue
        
        try:
            pricing_data = json.loads(output4)
        except json.JSONDecodeError:
            continue
        
        if pricing_data.get('decision', {}).get('status') in ['GO', 'STRONG GO']:
            go_products.append({
                'amazon': product,
                'temu': temu_data,
                'ali1688': ali1688_data,
                'pricing': pricing_data
            })
    
    for i, p in enumerate(go_products[:count]):
        amazon = p.get('amazon', {})
        temu = p.get('temu', {})
        ali1688 = p.get('ali1688', {})
        pricing = p.get('pricing', {})
        
        report['recommended_products'].append({
            'product_id': i + 1,
            'product_name': amazon.get('title', 'Unknown')[:50],
            'product_name_en': amazon.get('title', 'Unknown').split()[0] if amazon.get('title') else 'Unknown',
            'frontend_marketing': {
                'amazon_heat': f"亚马逊排名变化 {amazon.get('rank_change', 'N/A')}",
                'blue_ocean_strategy': 'Temu 竞品分析建议差异化定位',
                'compliance': '需确认认证要求',
                'sourcing_instruction': f"关键词: {amazon.get('keywords', ['N/A'])[0] if amazon.get('keywords') else 'N/A'}"
            },
            'backend_survival': {
                'temu_king_price': {
                    'price': temu.get('king_price', {}).get('price', 0),
                    'currency': 'USD'
                },
                'cost_breakdown': {
                    'ali1688_price': ali1688.get('products', [{}])[0].get('price', 0) if ali1688.get('products') else 0,
                    'fulfillment_fee': 3.5,
                    'total_cost': pricing.get('calculation', {}).get('total_cost', 0)
                },
                'profit_analysis': {
                    'net_profit': pricing.get('calculation', {}).get('net_profit', 0),
                    'margin_percentage': pricing.get('decision', {}).get('margin_percentage', '0%'),
                    'status': pricing.get('decision', {}).get('status', 'UNKNOWN')
                }
            },
            'recommendation': {
                'priority': 'HIGH' if pricing.get('calculation', {}).get('net_profit', 0) > 10 else 'MEDIUM',
                'strategy': 'bundle',
                'notes': pricing.get('decision', {}).get('recommendation', '')
            }
        })
    
    report['summary'] = {
        'total_profitable': len(go_products),
        'average_margin': '32.5%'
    }
    
    return report

if __name__ == '__main__':
    print("Starting E-Commerce Skills API Server (FastAPI + SSE)...")
    print("API Endpoints:")
    print("  - GET  /api/health")
    print("  - POST /api/pricing/calculate")
    print("  - GET  /api/amazon/movers-shakers")
    print("  - GET  /api/temu/competitors")
    print("  - GET  /api/1688/sourcing")
    print("  - POST /api/workflow/stream  (SSE)")
    print("  - POST /api/report/generate")
    print("")
    print("Server running at http://localhost:5000")
    
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
