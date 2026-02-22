#!/bin/bash

# Church Community Bot - Quick Start Script
# Created by: PINLON-YOUTH

echo "=========================================="
echo "Church Community Bot Setup"
echo "Created by: PINLON-YOUTH"
echo "=========================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check pip installation
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip3 found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "📝 Please edit .env file and add your:"
    echo "   1. BOT_TOKEN (get from @BotFather)"
    echo "   2. ADMIN_IDS (get from @userinfobot)"
    echo ""
    echo "Run this command to edit:"
    echo "   nano .env"
    echo ""
    read -p "Press Enter after you've configured .env file..."
fi

echo ""
echo "=========================================="
echo "🚀 Starting Church Community Bot..."
echo "=========================================="
echo ""

# Run the bot
python3 bot.py
