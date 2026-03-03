#!/bin/bash
# 4supply-sourcing skill 安装脚本

set -e

SKILL_NAME="4supply-sourcing"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "Installing $SKILL_NAME skill..."

if [ ! -d "$SKILL_DIR" ]; then
    echo "Error: Skill directory not found: $SKILL_DIR"
    exit 1
fi

chmod +x "$SCRIPT_DIR/scrape_4supply.py"

echo "✓ $SKILL_NAME skill installed successfully"
echo "  Location: $SKILL_DIR"
echo ""
echo "Usage:"
echo "  python $SCRIPT_DIR/scrape_4supply.py --keyword 'standing desk' --limit 20"
echo "  python $SCRIPT_DIR/scrape_4supply.py --keyword 'desk converter' --format json"
