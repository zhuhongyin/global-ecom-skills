#!/bin/bash
echo "=========================================="
echo "跨境电商选品工具 - 启动服务"
echo "=========================================="
echo ""

cd "$(dirname "$0")/.."

echo "1. 检查 Python 环境..."
python3 --version

echo ""
echo "2. 安装依赖..."
pip3 install flask flask-cors --quiet 2>/dev/null

echo ""
echo "3. 启动 API 服务..."
echo "   API 地址: http://localhost:5000"
echo "   前端地址: http://localhost:5000/frontend"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python3 frontend/api_server.py
