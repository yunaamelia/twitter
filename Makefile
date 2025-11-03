.PHONY: help install install-dev venv setup run verify stats clean format lint test

# Default target
help:
	@echo "Twitter Giveaway Bot - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make venv          - Create virtual environment"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make setup         - Complete setup (venv + install + verify)"
	@echo ""
	@echo "Running:"
	@echo "  make run           - Run the bot"
	@echo "  make verify        - Verify setup and credentials"
	@echo "  make stats         - Show bot statistics"
	@echo ""
	@echo "Development:"
	@echo "  make format        - Format code with black and isort"
	@echo "  make lint          - Run linters (pylint + flake8)"
	@echo "  make test          - Run tests"
	@echo "  make clean         - Clean cache and temporary files"
	@echo ""
	@echo "Database:"
	@echo "  make db-shell      - Open SQLite database shell"
	@echo "  make db-backup     - Backup database"
	@echo ""
	@echo "Logs:"
	@echo "  make logs          - View bot logs (tail -f)"
	@echo "  make logs-clear    - Clear bot logs"

# Virtual Environment
venv:
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "Activating and upgrading pip..."
	. venv/bin/activate && pip install --upgrade pip
	@echo "✅ Virtual environment created! Activate with: source venv/bin/activate"

# Install Dependencies
install:
	@echo "Installing production dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements-dev.txt
	@echo "✅ Development dependencies installed!"

# Complete Setup
setup: venv install install-dev
	@echo "Setting up environment file..."
	@if [ ! -f .env ]; then cp .env.example .env && echo "⚠️  Please edit .env with your credentials"; fi
	@echo "Running setup verification..."
	python setup_verify.py
	@echo "✅ Setup complete!"

# Running the Bot
run:
	@echo "Starting Twitter Giveaway Bot..."
	python main.py

verify:
	@echo "Verifying setup..."
	python setup_verify.py

stats:
	@echo "Bot Statistics:"
	python stats.py

# Development Tools
format:
	@echo "Formatting code with black..."
	black --line-length 100 *.py
	@echo "Sorting imports with isort..."
	isort *.py
	@echo "✅ Code formatted!"

lint:
	@echo "Running pylint..."
	-pylint *.py
	@echo ""
	@echo "Running flake8..."
	-flake8 *.py --max-line-length=100
	@echo "✅ Linting complete!"

test:
	@echo "Running tests..."
	pytest -v --cov=. --cov-report=html
	@echo "✅ Tests complete! See htmlcov/index.html for coverage report"

# Database Operations
db-shell:
	@echo "Opening SQLite database..."
	sqlite3 giveaways.db

db-backup:
	@echo "Backing up database..."
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	cp giveaways.db "backups/giveaways_$$timestamp.db" && \
	echo "✅ Database backed up to backups/giveaways_$$timestamp.db"

db-query:
	@echo "Recent giveaways:"
	sqlite3 giveaways.db "SELECT tweet_id, token_symbol, estimated_value_usd, participated FROM giveaways ORDER BY created_at DESC LIMIT 10;"

# Logs
logs:
	@echo "Tailing bot logs (Ctrl+C to stop)..."
	tail -f bot.log

logs-clear:
	@echo "Clearing bot logs..."
	> bot.log
	@echo "✅ Logs cleared!"

# Cleanup
clean:
	@echo "Cleaning Python cache files..."
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.mypy_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name 'htmlcov' -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"

# Create necessary directories
init-dirs:
	@mkdir -p backups logs
	@echo "✅ Directories created!"

# Full rebuild
rebuild: clean
	@echo "Rebuilding environment..."
	rm -rf venv
	$(MAKE) setup
	@echo "✅ Rebuild complete!"
