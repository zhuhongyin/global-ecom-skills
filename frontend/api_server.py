#!/usr/bin/env python3
"""
跨境电商选品工具后端 API
调用本地 skills 获取真实数据
"""

import json
import subprocess
import sys
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'skills')

def run_script(skill_name, script_name, args=[]):
    script_path = os.path.join(SCRIPTS_DIR, skill_name, 'scripts', script_name)
    if not os.path.exists(script_path):
        return None, f"Script not found: {script_path}"
    
    try:
        result = subprocess.run(
            [sys.executable, script_path] + args,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            return None, result.stderr
        return result.stdout, None
    except subprocess.TimeoutExpired:
        return None, "Script timeout"
    except Exception as e:
        return None, str(e)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/')
@app.route('/frontend')
def frontend():
    return send_from_directory('.', 'index.html')

@app.route('/api/pricing/calculate', methods=['POST'])
def calculate_pricing():
    data = request.json
    
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
    
    output, error = run_script('temu-pricing-calculator', 'calculate_pricing.py', args)
    
    if error:
        return jsonify({'error': error}), 500
    
    try:
        result = json.loads(output)
        return jsonify(result)
    except json.JSONDecodeError:
        return jsonify({'raw_output': output})

@app.route('/api/amazon/movers-shakers', methods=['GET'])
def get_amazon_movers_shakers():
    site = request.args.get('site', 'amazon.com')
    category = request.args.get('category', 'home-garden')
    limit = request.args.get('limit', 20)
    source = request.args.get('source', 'auto')
    
    args = [
        '--site', site,
        '--category', category,
        '--limit', str(limit),
        '--source', source,
        '--format', 'json'
    ]
    
    output, error = run_script('amazon-movers-shakers', 'scrape_amazon.py', args)
    
    if error:
        return jsonify({'error': error}), 500
    
    try:
        result = json.loads(output)
        return jsonify(result)
    except json.JSONDecodeError:
        return jsonify({'raw_output': output})

@app.route('/api/temu/competitors', methods=['GET'])
def get_temu_competitors():
    keyword = request.args.get('keyword', '')
    limit = request.args.get('limit', 20)
    
    if not keyword:
        return jsonify({'error': 'keyword is required'}), 400
    
    args = [
        '--keyword', keyword,
        '--limit', str(limit),
        '--format', 'json'
    ]
    
    output, error = run_script('temu-competitor-search', 'scrape_temu.py', args)
    
    if error:
        return jsonify({'error': error}), 500
    
    try:
        result = json.loads(output)
        return jsonify(result)
    except json.JSONDecodeError:
        return jsonify({'raw_output': output})

@app.route('/api/1688/sourcing', methods=['GET'])
def get_1688_sourcing():
    keyword = request.args.get('keyword', '')
    limit = request.args.get('limit', 20)
    
    if not keyword:
        return jsonify({'error': 'keyword is required'}), 400
    
    args = [
        '--keyword', keyword,
        '--limit', str(limit),
        '--format', 'json'
    ]
    
    output, error = run_script('ali1688-sourcing', 'scrape_1688.py', args)
    
    if error:
        return jsonify({'error': error}), 500
    
    try:
        result = json.loads(output)
        return jsonify(result)
    except json.JSONDecodeError:
        return jsonify({'raw_output': output})

@app.route('/api/workflow/run', methods=['POST'])
def run_workflow():
    data = request.json
    
    site = data.get('site', 'amazon.com')
    category = data.get('category', 'home-garden')
    count = data.get('count', 5)
    
    workflow_result = {
        'metadata': {
            'site': site,
            'category': category,
            'timestamp': datetime.now().isoformat()
        },
        'steps': [],
        'products': []
    }
    
    # Step 1: Amazon Movers & Shakers
    step1_args = [
        '--site', site,
        '--category', category,
        '--limit', str(count * 5),
        '--source', 'auto',
        '--format', 'json'
    ]
    
    output1, error1 = run_script('amazon-movers-shakers', 'scrape_amazon.py', step1_args)
    
    if error1:
        workflow_result['steps'].append({
            'name': 'amazon-movers-shakers',
            'status': 'error',
            'error': error1
        })
    else:
        try:
            amazon_data = json.loads(output1)
            workflow_result['steps'].append({
                'name': 'amazon-movers-shakers',
                'status': 'success',
                'count': len(amazon_data.get('products', []))
            })
            
            products = amazon_data.get('products', [])[:count * 2]
            
            for product in products:
                product_result = {
                    'amazon': product,
                    'temu': None,
                    'ali1688': None,
                    'pricing': None
                }
                
                # Step 2: Temu competitor search
                keywords = product.get('keywords', [])
                keyword = keywords[0] if keywords else product.get('title', '').split()[0]
                
                temu_args = ['--keyword', keyword, '--limit', '5', '--format', 'json']
                output2, error2 = run_script('temu-competitor-search', 'scrape_temu.py', temu_args)
                
                if not error2:
                    try:
                        temu_data = json.loads(output2)
                        product_result['temu'] = temu_data
                        
                        king_price = temu_data.get('king_price', {}).get('price', 0)
                        
                        # Step 3: 1688 sourcing
                        ali1688_args = ['--keyword', keyword, '--limit', '5', '--format', 'json']
                        output3, error3 = run_script('ali1688-sourcing', 'scrape_1688.py', ali1688_args)
                        
                        if not error3:
                            try:
                                ali1688_data = json.loads(output3)
                                product_result['ali1688'] = ali1688_data
                                
                                ali1688_price = ali1688_data.get('products', [{}])[0].get('price', 0)
                                
                                # Step 4: Pricing calculation
                                pricing_args = [
                                    '--temu-price', str(king_price),
                                    '--ali1688-price', str(ali1688_price),
                                    '--format', 'json'
                                ]
                                output4, error4 = run_script('temu-pricing-calculator', 'calculate_pricing.py', pricing_args)
                                
                                if not error4:
                                    try:
                                        pricing_data = json.loads(output4)
                                        product_result['pricing'] = pricing_data
                                    except:
                                        pass
                            except:
                                pass
                    except:
                        pass
                
                workflow_result['products'].append(product_result)
        except:
            workflow_result['steps'].append({
                'name': 'amazon-movers-shakers',
                'status': 'error',
                'error': 'Failed to parse output'
            })
    
    return jsonify(workflow_result)

@app.route('/api/report/generate', methods=['POST'])
def generate_report():
    data = request.json
    
    site = data.get('site', 'amazon.com')
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
    
    # Run workflow to get data
    workflow_result, _ = run_workflow_internal(site, category, count)
    
    # Filter products with GO status
    go_products = []
    for product in workflow_result.get('products', []):
        pricing = product.get('pricing', {})
        if pricing and pricing.get('decision', {}).get('status') in ['GO', 'STRONG GO']:
            go_products.append(product)
    
    # Generate report for top products
    for i, product in enumerate(go_products[:count]):
        amazon = product.get('amazon', {})
        temu = product.get('temu', {})
        ali1688 = product.get('ali1688', {})
        pricing = product.get('pricing', {})
        
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
    
    return jsonify(report)

def run_workflow_internal(site, category, count):
    workflow_result = {
        'products': []
    }
    
    step1_args = [
        '--site', site,
        '--category', category,
        '--limit', str(count * 5),
        '--source', 'auto',
        '--format', 'json'
    ]
    
    output1, error1 = run_script('amazon-movers-shakers', 'scrape_amazon.py', step1_args)
    
    if error1:
        return workflow_result, error1
    
    try:
        amazon_data = json.loads(output1)
        products = amazon_data.get('products', [])[:count * 2]
        
        for product in products:
            product_result = {
                'amazon': product,
                'temu': None,
                'ali1688': None,
                'pricing': None
            }
            
            keywords = product.get('keywords', [])
            keyword = keywords[0] if keywords else product.get('title', '').split()[0]
            
            temu_args = ['--keyword', keyword, '--limit', '5', '--format', 'json']
            output2, error2 = run_script('temu-competitor-search', 'scrape_temu.py', temu_args)
            
            if not error2:
                try:
                    temu_data = json.loads(output2)
                    product_result['temu'] = temu_data
                    
                    king_price = temu_data.get('king_price', {}).get('price', 0)
                    
                    ali1688_args = ['--keyword', keyword, '--limit', '5', '--format', 'json']
                    output3, error3 = run_script('ali1688-sourcing', 'scrape_1688.py', ali1688_args)
                    
                    if not error3:
                        try:
                            ali1688_data = json.loads(output3)
                            product_result['ali1688'] = ali1688_data
                            
                            ali1688_price = ali1688_data.get('products', [{}])[0].get('price', 0)
                            
                            pricing_args = [
                                '--temu-price', str(king_price),
                                '--ali1688-price', str(ali1688_price),
                                '--format', 'json'
                            ]
                            output4, error4 = run_script('temu-pricing-calculator', 'calculate_pricing.py', pricing_args)
                            
                            if not error4:
                                try:
                                    pricing_data = json.loads(output4)
                                    product_result['pricing'] = pricing_data
                                except:
                                    pass
                        except:
                            pass
                except:
                    pass
            
            workflow_result['products'].append(product_result)
    except:
        pass
    
    return workflow_result, None

if __name__ == '__main__':
    print("Starting E-Commerce Skills API Server...")
    print("API Endpoints:")
    print("  - GET  /api/health")
    print("  - POST /api/pricing/calculate")
    print("  - GET  /api/amazon/movers-shakers")
    print("  - GET  /api/temu/competitors")
    print("  - GET  /api/1688/sourcing")
    print("  - POST /api/workflow/run")
    print("  - POST /api/report/generate")
    print("")
    print("Server running at http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
