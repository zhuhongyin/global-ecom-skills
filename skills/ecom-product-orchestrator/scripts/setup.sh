#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Setting up ecom-product-orchestrator..."

chmod +x "$SCRIPT_DIR/orchestrator.py"

echo "Setup complete!"
