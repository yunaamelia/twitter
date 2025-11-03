# Development Setup Guide

## VS Code Configuration Complete! 🚀

Your workspace is now configured with powerful Python development tools.

## What's Been Configured

### ✅ VS Code Extensions Installed

- **Python & Pylance** - IntelliSense, linting, debugging
- **Black Formatter** - Auto code formatting
- **isort** - Import sorting
- **SQLite Viewer** - Database inspection
- **Error Lens** - Inline error display
- **Better Comments** - Enhanced code comments
- **GitLens** - Advanced Git features
- **DotENV** - .env file syntax highlighting
- **Todo Tree** - Task tracking
- **Material Icon Theme** - Beautiful file icons
- **Thunder Client** - REST API testing

### ✅ Configuration Files Created

```
.vscode/
  ├── settings.json           # VS Code workspace settings
  ├── launch.json            # Debug configurations
  ├── tasks.json             # Build & run tasks
  ├── extensions.json        # Recommended extensions
  └── snippets.code-snippets # Custom code snippets

.github/
  ├── copilot-instructions.md # AI coding agent instructions
  └── copilot-mcp.json       # MCP server configuration

Development Files:
  ├── Makefile               # Development commands
  ├── .editorconfig          # Editor configuration
  ├── .pylintrc             # Pylint configuration
  ├── .flake8               # Flake8 configuration
  ├── pyproject.toml        # Python project config
  ├── .pre-commit-config.yaml # Pre-commit hooks
  └── requirements-dev.txt   # Dev dependencies
```

### ✅ MCP Servers Configured

- **GitHub** - Repository management
- **Filesystem** - File operations
- **SQLite** - Database queries
- **Context7** - Documentation lookup
- **Browser** - Web automation with Playwright

## Quick Start Commands

### Using Makefile (Recommended)

```bash
# View all available commands
make help

# Complete setup (creates venv, installs deps, verifies)
make setup

# Run the bot
make run

# Format code
make format

# Run linters
make lint

# View statistics
make stats

# View logs in real-time
make logs

# Open database
make db-shell
```

### Using VS Code Tasks

Press `Ctrl+Shift+P` and type "Run Task" to access:

- Run Bot
- Setup Verify
- Show Statistics
- Format Code
- Lint Code
- View Bot Logs
- And more...

### Using VS Code Debug

Press `F5` or use Debug panel:

- **Python: Bot Main** - Debug full bot
- **Python: Bot (Single Cycle)** - Debug one cycle
- **Python: Setup Verify** - Debug setup
- **Python: Current File** - Debug any Python file

## Development Workflow

### 1. Initial Setup

```bash
# Create virtual environment and install dependencies
make setup

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit with your credentials
nano .env

# Verify setup
make verify
# or: python setup_verify.py
```

### 3. Start Coding

- Open any Python file
- IntelliSense will auto-activate
- Format on save is enabled
- Errors shown inline with Error Lens

### 4. Before Committing

```bash
# Format and lint
make format
make lint

# Or use pre-commit hooks
pre-commit install
pre-commit run --all-files
```

## VS Code Features Enabled

### 🎨 Auto-Formatting

- **Black** formatter runs on save
- **isort** organizes imports automatically
- Line length: 100 characters (PEP 8 compliant)

### 🔍 Code Analysis

- **Type checking** with Pylance (basic mode)
- **Linting** with Pylint and Flake8
- **Error Lens** shows errors inline
- **Inlay hints** for function returns and variable types

### 🐛 Debugging

- Breakpoints in any Python file
- Variable inspection
- Call stack navigation
- Multiple debug configurations
- Environment variables auto-loaded from .env

### 📊 Database Tools

- SQLite Viewer extension installed
- Right-click `giveaways.db` → "Open Database"
- Visual query builder
- Table browsing

### 🤖 GitHub Copilot Enhanced

- Instructions file linked (`.github/copilot-instructions.md`)
- Project-specific patterns understood
- MCP servers available for advanced operations

## Code Snippets Available

Type these prefixes and press Tab:

- `tw-client` - Create Tweepy client
- `db-session` - Database session with context
- `log-setup` - Setup module logger
- `try-log` - Try-except with logging
- `tw-search` - Twitter search query
- `rate-limit` - Add rate limiting delay
- `cfg-account` - Get account credentials
- `parse-rules` - Giveaway rules dictionary
- `cg-price` - CoinGecko price check
- `doc-func` - Function docstring template

## Keyboard Shortcuts

### Essential

- `F5` - Start Debugging
- `Ctrl+Shift+P` - Command Palette
- `Ctrl+Shift+B` - Run Build Task
- `Ctrl+\`` - Toggle Terminal
- `Ctrl+Shift+F` - Search in Files

### Python-Specific

- `Shift+Alt+F` - Format Document
- `Ctrl+.` - Quick Fix
- `F12` - Go to Definition
- `Shift+F12` - Find All References
- `Ctrl+Space` - Trigger IntelliSense

### GitHub Copilot

- `Ctrl+I` - Open Copilot Chat
- `Alt+\` - Toggle Copilot Suggestions
- `Tab` - Accept Suggestion

## Terminal Commands

### Development

```bash
# Activate virtual environment
source venv/bin/activate

# Run bot
python main.py

# Verify setup
python setup_verify.py

# View statistics
python stats.py

# Format code
black --line-length 100 *.py
isort *.py

# Lint code
pylint *.py
flake8 *.py --max-line-length=100

# Run tests (when created)
pytest -v
```

### Database

```bash
# Open database shell
sqlite3 giveaways.db

# Query examples:
SELECT * FROM giveaways ORDER BY created_at DESC LIMIT 10;
SELECT * FROM accounts WHERE is_active = 1;
SELECT * FROM winner_notifications;

# Backup database
cp giveaways.db backups/giveaways_$(date +%Y%m%d).db
```

## Troubleshooting

### Python Not Found

```bash
# Install Python extension
Ctrl+Shift+P → "Python: Select Interpreter"
# Choose venv/bin/python
```

### Linting Errors

```bash
# Install dev dependencies
pip install -r requirements-dev.txt
```

### Import Errors

```bash
# Set PYTHONPATH (automatically done in terminal)
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

### Extension Not Working

```bash
# Reload VS Code
Ctrl+Shift+P → "Developer: Reload Window"
```

## Advanced Features

### MCP Servers Usage

MCP servers provide enhanced capabilities:

```python
# GitHub operations via MCP
# - Create branches, PRs
# - Search issues
# - Manage repositories

# SQLite operations via MCP
# - Query database
# - Export data
# - Analyze schema

# Browser automation via MCP
# - Test Twitter login
# - Verify giveaway pages
# - Screenshot results
```

### Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files

# Update hooks
pre-commit autoupdate
```

### Custom Tasks

Edit `.vscode/tasks.json` to add custom tasks:

```json
{
  "label": "My Custom Task",
  "type": "shell",
  "command": "python my_script.py",
  "problemMatcher": []
}
```

## Tips & Tricks

### 💡 Productivity Tips

1. Use `Ctrl+P` to quickly open files
2. Use `Ctrl+Shift+O` to navigate symbols in file
3. Use multi-cursor editing with `Ctrl+Alt+Down`
4. Use `Ctrl+/` to toggle comments
5. Use `Alt+Up/Down` to move lines

### 🔥 Hot Reload

The bot doesn't support hot reload, but you can:

```bash
# Run in debug mode for quick restarts
F5 → Make changes → Stop → F5
```

### 📝 Code Quality

- Error Lens shows issues immediately
- Todo Tree tracks TODOs automatically
- GitLens shows git blame inline

### 🎯 Focus Mode

- `Ctrl+B` - Toggle sidebar
- `Ctrl+J` - Toggle terminal
- `F11` - Fullscreen

## Next Steps

1. **Install Dependencies**

   ```bash
   make install-dev
   ```

2. **Configure Credentials**

   ```bash
   cp .env.example .env
   # Edit .env with your Twitter API keys
   ```

3. **Verify Setup**

   ```bash
   make verify
   ```

4. **Start Developing!**
   - Open any Python file
   - Make changes
   - Code auto-formats on save
   - Errors shown inline

## Resources

- [VS Code Python Documentation](https://code.visualstudio.com/docs/python/python-tutorial)
- [Black Formatter](https://black.readthedocs.io/)
- [Pylint](https://pylint.pycqa.org/)
- [GitHub Copilot](https://github.com/features/copilot)
- [MCP Servers](https://modelcontextprotocol.io/)

---

**Happy Coding! 🎉**

Your VS Code is now a powerful Python development environment!
