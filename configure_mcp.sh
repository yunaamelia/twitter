#!/bin/bash

# Script untuk mengonfigurasi MCP servers untuk Twitter bot project
# Menghapus yang tidak diperlukan dan mengoptimalkan setup

set -e

echo "🔧 Configuring MCP Servers for Twitter Bot..."
echo ""

MCP_CONFIG_FILE="$HOME/.config/Code - Insiders/User/mcp.json"
MCP_DIR="$HOME/.config/Code - Insiders/User/mcp"
BACKUP_FILE="$MCP_CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"

# Backup existing config
if [ -f "$MCP_CONFIG_FILE" ]; then
    echo "📦 Backing up current MCP config..."
    cp "$MCP_CONFIG_FILE" "$BACKUP_FILE"
    echo "   Backup saved to: $BACKUP_FILE"
    echo ""
fi

# Remove Playwright MCP (not needed for Twitter bot)
PLAYWRIGHT_DIR="$MCP_DIR/microsoft.playwright-mcp-0.0.1-seed"
if [ -d "$PLAYWRIGHT_DIR" ]; then
    echo "🗑️  Removing Playwright MCP (not needed)..."
    rm -rf "$PLAYWRIGHT_DIR"
    echo "   ✅ Removed: microsoft.playwright-mcp"
else
    echo "ℹ️  Playwright MCP not found (already removed or never installed)"
fi
echo ""

# Create optimized MCP configuration
echo "✏️  Creating optimized MCP configuration..."
cat > "$MCP_CONFIG_FILE" << 'EOF'
{
  "servers": {
    "github/github-mcp-server": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "gallery": "https://api.mcp.github.com",
      "version": "0.13.0"
    },
    "upstash/context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "${input:context7_api_key}"
      },
      "gallery": "https://api.mcp.github.com",
      "version": "1.0.0"
    },
    "gitkraken/gitkraken-mcp-server": {
      "type": "http",
      "url": "https://api.mcp.gitkraken.com/mcp/v1",
      "gallery": "https://api.mcp.github.com",
      "version": "1.0.0"
    }
  },
  "inputs": [
    {
      "id": "context7_api_key",
      "type": "promptString",
      "description": "Context7 API key (optional; increases rate limits). Get one at https://context7.com/dashboard",
      "password": true
    }
  ]
}
EOF

echo "   ✅ MCP configuration updated"
echo ""

# Summary
echo "📊 MCP Configuration Summary:"
echo ""
echo "✅ Active MCP Servers:"
echo "   1. GitHub MCP Server      - Repository, PR, and issue management"
echo "   2. Context7 (Upstash)     - Up-to-date library documentation"
echo "   3. GitKraken MCP Server   - Advanced Git operations"
echo "   4. Pylance MCP (built-in) - Python code analysis"
echo ""
echo "❌ Removed:"
echo "   - Playwright MCP - Not needed for Twitter bot"
echo ""
echo "💡 Benefits:"
echo "   • Faster VS Code startup (no unnecessary Node.js processes)"
echo "   • Lower memory usage"
echo "   • Focused toolset for Python + GitHub workflow"
echo ""
echo "🔄 Next Steps:"
echo "   1. Reload VS Code: Ctrl+Shift+P → 'Developer: Reload Window'"
echo "   2. (Optional) Get Context7 API key: https://context7.com/dashboard"
echo "   3. Test MCP: Ask Copilot to 'List recent PRs' or 'Get Tweepy docs'"
echo ""
echo "✅ MCP configuration complete!"
echo ""
echo "📝 Documentation: .vscode/MCP_CONFIG.md"
echo "🔧 Config file: $MCP_CONFIG_FILE"
