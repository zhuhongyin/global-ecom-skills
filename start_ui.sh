#!/bin/bash
# ==========================================
# 跨境电商选品工具 - UI 启动脚本
# 先拉取 main-ui 分支代码，再直接启动 API 服务
# ==========================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}=========================================="
echo -e "  选品工具 UI 启动 (main-ui 分支)"
echo -e "==========================================${NC}"
echo ""

if [ -d "$SCRIPT_DIR/.git" ]; then
    echo -e "${BLUE}→ 获取 main-ui 分支代码...${NC}"
    if git fetch origin main-ui 2>/dev/null; then
        if git rev-parse --verify origin/main-ui &>/dev/null; then
            git checkout main-ui 2>/dev/null || git checkout -b main-ui origin/main-ui
            git pull origin main-ui 2>/dev/null || true
            echo -e "${GREEN}[✓] 已切换到 main-ui 分支${NC}"
        else
            echo -e "${YELLOW}[!] 远程未找到 main-ui 分支，使用当前分支${NC}"
        fi
    else
        echo -e "${YELLOW}[!] 获取远程失败，使用当前分支${NC}"
    fi
    echo ""
else
    echo -e "${YELLOW}[!] 非 Git 仓库，直接启动${NC}"
    echo ""
fi

if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo -e "${BLUE}→ 启动 API 服务...${NC}"
echo -e "  前端: ${GREEN}http://localhost:5000${NC}"
echo -e "  按 ${RED}Ctrl+C${NC} 停止"
echo ""
exec "$PYTHON_CMD" frontend/api_server.py
