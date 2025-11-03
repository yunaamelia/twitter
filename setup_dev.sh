#!/bin/bash
# Quick setup script for development environment

set -e

echo "🚀 Twitter Giveaway Bot - Development Setup"
echo "=========================================="
echo ""

# Check Python version
echo "📌 Checking Python version..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install production dependencies
echo "📥 Installing production dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "📥 Installing development dependencies..."
pip install -r requirements-dev.txt

# Setup environment file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your Twitter API credentials"
fi

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backups logs

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your Twitter API credentials"
echo "2. Run: python setup_verify.py"
echo "3. Run: python main.py"
echo ""
echo "Available commands:"
echo "  make help          - Show all available commands"
echo "  make run           - Run the bot"
echo "  make verify        - Verify setup"
echo "  make stats         - Show statistics"
echo "  make format        - Format code"
echo "  make lint          - Lint code"
echo ""
echo "Happy coding! 🎉"
