#!/bin/bash
# MCP Tools Testing Script for Twitter Bot
# Tests all configured MCP servers and their functionality

set -e

echo "==================================="
echo "MCP Tools Testing for Twitter Bot"
echo "==================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in VS Code Insiders
if [ -d "$HOME/.config/Code - Insiders" ]; then
    MCP_DIR="$HOME/.config/Code - Insiders/User/mcp"
else
    MCP_DIR="$HOME/.config/Code/User/mcp"
fi

echo "1. Checking MCP Server Installation..."
echo "======================================="
if [ -d "$MCP_DIR" ]; then
    echo -e "${GREEN}✓${NC} MCP directory found: $MCP_DIR"
    echo ""
    echo "Installed MCP servers:"
    ls -1 "$MCP_DIR" 2>/dev/null || echo "No servers installed yet"
else
    echo -e "${RED}✗${NC} MCP directory not found"
    echo "MCP servers will be installed on first use"
fi
echo ""

echo "2. Checking Environment Variables..."
echo "====================================="
check_env() {
    if [ -z "${!1}" ]; then
        echo -e "${RED}✗${NC} $1 not set"
        return 1
    else
        echo -e "${GREEN}✓${NC} $1 set"
        return 0
    fi
}

# Check GitHub token
check_env "GITHUB_TOKEN" || echo "  Required for GitHub MCP server"

# Check Twitter credentials (at least one account)
if [ -n "$TWITTER_API_KEY_1" ]; then
    echo -e "${GREEN}✓${NC} Twitter credentials configured"
else
    echo -e "${YELLOW}⚠${NC} Twitter credentials not in environment (may be in .env file)"
fi
echo ""

echo "3. Checking Database..."
echo "======================="
if [ -f "giveaways.db" ]; then
    echo -e "${GREEN}✓${NC} giveaways.db exists"

    # Check if sqlite3 is available
    if command -v sqlite3 &> /dev/null; then
        echo ""
        echo "Database tables:"
        sqlite3 giveaways.db ".tables"
        echo ""

        echo "Record counts:"
        echo "  Giveaways: $(sqlite3 giveaways.db 'SELECT COUNT(*) FROM Giveaway;')"
        echo "  Accounts: $(sqlite3 giveaways.db 'SELECT COUNT(*) FROM Account;')"
        echo "  Winners: $(sqlite3 giveaways.db 'SELECT COUNT(*) FROM WinnerNotification;')"
    else
        echo -e "${YELLOW}⚠${NC} sqlite3 not installed, skipping table checks"
    fi
else
    echo -e "${YELLOW}⚠${NC} giveaways.db not found (will be created on first bot run)"
fi
echo ""

echo "4. Checking Python Environment..."
echo "=================================="
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} Python 3 found: $(python3 --version)"

    # Check critical packages
    echo ""
    echo "Checking required packages:"
    for pkg in tweepy sqlalchemy schedule requests; do
        if python3 -c "import $pkg" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} $pkg installed"
        else
            echo -e "  ${RED}✗${NC} $pkg missing"
        fi
    done
else
    echo -e "${RED}✗${NC} Python 3 not found"
fi
echo ""

echo "5. Checking Git Repository..."
echo "=============================="
if [ -d ".git" ]; then
    echo -e "${GREEN}✓${NC} Git repository initialized"

    echo "  Remote: $(git remote get-url origin 2>/dev/null || echo 'Not configured')"
    echo "  Branch: $(git branch --show-current)"
    echo "  Uncommitted changes: $(git status --short | wc -l) files"
else
    echo -e "${RED}✗${NC} Not a git repository"
fi
echo ""

echo "6. Checking Bot Files..."
echo "========================"
critical_files=(
    "bot.py"
    "main.py"
    "config.py"
    "models.py"
    "account_manager.py"
    "price_checker.py"
    "giveaway_parser.py"
    "winner_detector.py"
)

for file in "${critical_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file missing"
    fi
done
echo ""

echo "7. Checking Log Files..."
echo "========================"
if [ -f "bot.log" ]; then
    echo -e "${GREEN}✓${NC} bot.log exists"
    echo "  Size: $(du -h bot.log | cut -f1)"
    echo "  Last modified: $(stat -c %y bot.log 2>/dev/null || stat -f %Sm bot.log 2>/dev/null)"
    echo ""
    echo "Last 5 log entries:"
    tail -5 bot.log | sed 's/^/  /'
else
    echo -e "${YELLOW}⚠${NC} bot.log not found (will be created on first bot run)"
fi
echo ""

echo "8. Testing MCP Configuration..."
echo "================================"
if [ -f ".github/copilot-mcp.json" ]; then
    echo -e "${GREEN}✓${NC} .github/copilot-mcp.json exists"

    # Check if jq is available for JSON parsing
    if command -v jq &> /dev/null; then
        echo ""
        echo "Enabled MCP servers:"
        jq -r '.mcpServers | to_entries[] | select(.value.disabled == false) | "  ✓ \(.key)"' .github/copilot-mcp.json

        echo ""
        echo "Disabled MCP servers:"
        jq -r '.mcpServers | to_entries[] | select(.value.disabled == true) | "  ✗ \(.key)"' .github/copilot-mcp.json
    else
        echo -e "${YELLOW}⚠${NC} jq not installed, skipping JSON parsing"
    fi
else
    echo -e "${RED}✗${NC} .github/copilot-mcp.json not found"
fi
echo ""

echo "9. Testing CoinGecko API..."
echo "============================"
if command -v curl &> /dev/null; then
    response=$(curl -s "https://api.coingecko.com/api/v3/ping")
    if echo "$response" | grep -q "gecko_says"; then
        echo -e "${GREEN}✓${NC} CoinGecko API reachable"
        echo "  Response: $(echo $response | jq -r '.gecko_says' 2>/dev/null || echo 'OK')"
    else
        echo -e "${RED}✗${NC} CoinGecko API unreachable"
    fi
else
    echo -e "${YELLOW}⚠${NC} curl not installed, skipping API test"
fi
echo ""

echo "10. MCP Tools Ready Status..."
echo "=============================="
errors=0

# Count critical issues
[ ! -f "giveaways.db" ] && ((errors++))
[ ! -f "bot.py" ] && ((errors++))
[ ! -d ".git" ] && ((errors++))

if [ $errors -eq 0 ]; then
    echo -e "${GREEN}✓ All MCP tools ready for use!${NC}"
    echo ""
    echo "You can now:"
    echo "  • Query database: 'Show me top accounts by wins'"
    echo "  • Read logs: 'Analyze bot.log for errors'"
    echo "  • Test code: 'Execute price_checker with test input'"
    echo "  • Check git: 'What files have uncommitted changes?'"
    echo "  • Store context: 'Remember rate limit patterns'"
    echo "  • Fetch APIs: 'Check CoinGecko Bitcoin price'"
else
    echo -e "${YELLOW}⚠ $errors critical issue(s) found${NC}"
    echo "Some MCP functionality may be limited"
fi
echo ""

echo "==================================="
echo "Testing Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "  1. Start VS Code Insiders (MCP servers will auto-install)"
echo "  2. Open GitHub Copilot Chat"
echo "  3. Try: '@workspace Show database statistics'"
echo "  4. See .github/MCP_TOOLS.md for full documentation"
echo ""
