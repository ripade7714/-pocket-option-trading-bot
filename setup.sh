#!/bin/bash

# Pocket Option Trading Bot - Quick Start Script

echo "=========================================="
echo "Pocket Option Trading Bot - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "  Found: $python_version"
echo ""

# Create virtual environment
echo "✓ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "  Virtual environment created and activated"
echo ""

# Install dependencies
echo "✓ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "  Dependencies installed"
echo ""

# Create directories
echo "✓ Creating directories..."
mkdir -p logs charts
echo "  Directories created"
echo ""

# Setup environment file
echo "✓ Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "  Created .env file from template"
    echo "  ⚠️  IMPORTANT: Edit .env with your credentials:"
    echo "     - POCKET_OPTION_EMAIL"
    echo "     - POCKET_OPTION_PASSWORD"
    echo "     - TELEGRAM_BOT_TOKEN"
    echo "     - TELEGRAM_CHAT_ID"
else
    echo "  .env file already exists"
fi
echo ""

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Run: python trading_bot_engine.py"
echo "3. Monitor logs in: logs/trading_bot.log"
echo ""
echo "For more info, see README.md"
