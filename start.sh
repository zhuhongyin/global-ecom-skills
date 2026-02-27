#!/bin/bash

# ==========================================
# 跨境电商选品工具 - Skills 管理脚本
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
        print_error "Python 未安装，请先安装 Python 3.9+"
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
    print_step "虚拟环境已激活"
}

install_dependencies() {
    echo ""
    echo -e "${BLUE}→ 检查 Python 依赖...${NC}"
    
    print_step "安装 Python 依赖..."
    pip install requests beautifulsoup4 -i https://pypi.org/simple/ --quiet 2>/dev/null || \
    pip install requests beautifulsoup4 --quiet 2>/dev/null
    
    print_step "依赖安装完成"
}

show_usage() {
    echo ""
    echo "用法: ./start.sh [选项]"
    echo ""
    echo "选项:"
    echo "  --install-skills    安装 Skills 到 Claude Code"
    echo "  --install-deps      安装 Python 依赖"
    echo "  --help              显示帮助信息"
    echo ""
    echo "示例:"
    echo "  ./start.sh                  # 检查并安装所有依赖"
    echo "  ./start.sh --install-skills # 强制安装 Skills"
    echo "  ./start.sh --install-deps   # 仅安装 Python 依赖"
    echo ""
}

show_examples() {
    echo ""
    echo -e "${GREEN}=========================================="
    echo -e "  使用示例"
    echo -e "==========================================${NC}"
    echo ""
    echo "注意：使用前请先激活虚拟环境"
    echo -e "   ${YELLOW}source venv/bin/activate${NC}"
    echo ""
    echo "1. Amazon 飙升榜爬取:"
    echo -e "   ${YELLOW}python3 skills/amazon-movers-shakers/scripts/scrape_amazon.py --site us --category home-garden --limit 10${NC}"
    echo ""
    echo "2. Temu 竞品分析:"
    echo -e "   ${YELLOW}python3 skills/temu-competitor-search/scripts/scrape_temu.py --keyword \"Standing Desk\" --limit 10${NC}"
    echo ""
    echo "3. 1688 供应链查询:"
    echo -e "   ${YELLOW}python3 skills/ali1688-sourcing/scripts/scrape_1688.py --keyword \"Standing Desk\" --limit 10${NC}"
    echo ""
    echo "4. V4.1 核价计算:"
    echo -e "   ${YELLOW}python3 skills/temu-pricing-calculator/scripts/calculate_pricing.py --temu-price 29.99 --ali1688-price 20.0${NC}"
    echo ""
    echo -e "${GREEN}==========================================${NC}"
    echo ""
}

main() {
    print_header
    
    INSTALL_SKILLS=false
    INSTALL_DEPS=false
    
    for arg in "$@"; do
        case $arg in
            --help|-h)
                show_usage
                show_examples
                exit 0
                ;;
            --install-skills)
                INSTALL_SKILLS=true
                ;;
            --install-deps)
                INSTALL_DEPS=true
                ;;
        esac
    done
    
    check_python
    setup_venv
    
    if [ "$INSTALL_SKILLS" = true ]; then
        echo ""
        echo -e "${BLUE}→ 强制安装 Skills...${NC}"
        if check_npx; then
            npx skills add zhuhongyin/global-ecom-skills --skill '*' -a claude-code -y
        fi
    else
        check_node
        install_skills
    fi
    
    if [ "$INSTALL_DEPS" = true ]; then
        install_dependencies
    else
        install_dependencies
    fi
    
    echo ""
    echo -e "${GREEN}=========================================="
    echo -e "  准备完成"
    echo -e "==========================================${NC}"
    echo ""
    show_examples
}

main "$@"
