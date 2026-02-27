#!/bin/bash

# ==========================================
# 跨境电商选品工具 - 一键启动脚本
# ==========================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${BLUE}=========================================="
    echo -e "  跨境电商选品工具 - Global E-Commerce Skills"
    echo -e "==========================================${NC}"
    echo ""
}

print_step() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python 未安装，请先安装 Python 3.8+"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    print_step "Python 版本: $PYTHON_VERSION"
}

check_node() {
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_step "Node.js 版本: $NODE_VERSION"
        return 0
    else
        print_warning "Node.js 未安装，无法安装 skills"
        return 1
    fi
}

check_npx() {
    if command -v npx &> /dev/null; then
        return 0
    else
        print_warning "npx 未安装"
        return 1
    fi
}

install_skills() {
    echo ""
    echo -e "${BLUE}→ 检查 Skills 安装状态...${NC}"
    
    SKILLS_DIR="$HOME/.claude/skills"
    
    REQUIRED_SKILLS=(
        "temu-pricing-calculator"
        "amazon-movers-shakers"
        "temu-competitor-search"
        "ali1688-sourcing"
        "ecom-product-orchestrator"
    )
    
    MISSING_SKILLS=()
    
    for skill in "${REQUIRED_SKILLS[@]}"; do
        if [ -d "$SKILLS_DIR/$skill" ]; then
            print_step "已安装: $skill"
        else
            MISSING_SKILLS+=("$skill")
        fi
    done
    
    if [ ${#MISSING_SKILLS[@]} -eq 0 ]; then
        print_step "所有 Skills 已安装"
        return 0
    fi
    
    echo ""
    echo -e "${YELLOW}→ 以下 Skills 未安装:${NC}"
    for skill in "${MISSING_SKILLS[@]}"; do
        echo "   - $skill"
    done
    
    if ! check_npx; then
        print_warning "跳过 Skills 安装（npx 不可用）"
        return 1
    fi
    
    echo ""
    echo -e "${BLUE}→ 正在安装 Skills...${NC}"
    
    if npx skills add zhuhongyin/global-ecom-skills --skill '*' -a claude-code -y 2>/dev/null; then
        print_step "Skills 安装成功"
    else
        print_warning "Skills 安装失败，将使用本地脚本"
    fi
}

setup_venv() {
    echo ""
    echo -e "${BLUE}→ 检查虚拟环境...${NC}"
    
    if [ ! -d "$SCRIPT_DIR/venv" ]; then
        print_step "创建虚拟环境..."
        $PYTHON_CMD -m venv "$SCRIPT_DIR/venv"
    else
        print_step "虚拟环境已存在"
    fi
    
    source "$SCRIPT_DIR/venv/bin/activate"
    
    print_step "安装 Python 依赖..."
    pip install fastapi uvicorn requests beautifulsoup4 -i https://pypi.org/simple/ --quiet 2>/dev/null || \
    pip install fastapi uvicorn requests beautifulsoup4 --quiet 2>/dev/null
}

start_server() {
    echo ""
    echo -e "${BLUE}→ 启动服务...${NC}"
    echo ""
    echo -e "${GREEN}=========================================="
    echo -e "  服务已启动"
    echo -e "==========================================${NC}"
    echo ""
    echo -e "  前端地址: ${YELLOW}http://localhost:5000${NC}"
    echo -e "  API 文档: ${YELLOW}http://localhost:5000/api/health${NC}"
    echo ""
    echo -e "  按 ${RED}Ctrl+C${NC} 停止服务"
    echo ""
    echo -e "${GREEN}==========================================${NC}"
    echo ""
    
    $PYTHON_CMD frontend/api_server.py
}

show_help() {
    echo ""
    echo "用法: ./start.sh [选项]"
    echo ""
    echo "选项:"
    echo "  --install-skills    安装 Skills 到 Claude Code"
    echo "  --skip-skills       跳过 Skills 检查"
    echo "  --help              显示帮助信息"
    echo ""
    echo "示例:"
    echo "  ./start.sh                  # 正常启动"
    echo "  ./start.sh --install-skills # 强制安装 Skills"
    echo "  ./start.sh --skip-skills    # 跳过 Skills 检查"
    echo ""
}

main() {
    print_header
    
    SKIP_SKILLS=false
    FORCE_INSTALL=false
    
    for arg in "$@"; do
        case $arg in
            --help|-h)
                show_help
                exit 0
                ;;
            --install-skills)
                FORCE_INSTALL=true
                ;;
            --skip-skills)
                SKIP_SKILLS=true
                ;;
        esac
    done
    
    check_python
    
    if [ "$SKIP_SKILLS" = false ]; then
        check_node
        if [ "$FORCE_INSTALL" = true ]; then
            echo ""
            echo -e "${BLUE}→ 强制安装 Skills...${NC}"
            if check_npx; then
                npx skills add zhuhongyin/global-ecom-skills --skill '*' -a claude-code -y
            fi
        else
            install_skills
        fi
    fi
    
    setup_venv
    start_server
}

main "$@"
