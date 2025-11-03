#!/bin/bash

# Script untuk menghapus VS Code extensions yang tidak diperlukan
# Dan install extensions yang recommended

echo "🧹 Cleaning up unnecessary VS Code extensions..."
echo ""

# Extensions yang akan dihapus (tidak diperlukan untuk Python bot project)
EXTENSIONS_TO_REMOVE=(
    "aaron-bond.better-comments"              # Nice to have, tapi tidak essential
    "bierner.markdown-mermaid"                # Tidak perlu mermaid untuk project ini
    "christian-kohler.npm-intellisense"       # Project Python, bukan Node.js
    "formulahendry.code-runner"               # Sudah ada tasks.json
    "gruntfuggly.todo-tree"                   # Duplikat dengan wayou.vscode-todo-highlight
    "humao.rest-client"                       # Duplikat dengan Thunder Client
    "rangav.vscode-thunder-client"            # Tidak perlu API testing untuk bot ini
    "miguelsolorio.fluent-icons"              # Duplikat dengan material-icon-theme
    "oderwat.indent-rainbow"                  # Visual noise, tidak essential
    "shardulm94.trailing-spaces"              # Sudah ditangani formatters
    "wayou.vscode-todo-highlight"             # Tidak essential
    "ms-vscode.azure-repos"                   # Tidak pakai Azure
    "ms-vscode.remote-explorer"               # Tidak perlu remote
    "ms-vscode.remote-repositories"           # Tidak perlu remote
    "ms-vscode.remote-server"                 # Tidak perlu remote
    "github.remotehub"                        # Tidak perlu remote hub
    "mijur.copilot-terminal-tools"            # Experimental, belum stable
    "davidanson.vscode-markdownlint"          # Markdown linting tidak critical
    "2gua.rainbow-brackets"                   # Built-in di VS Code modern
)

# Extensions yang HARUS TETAP ADA (essential)
ESSENTIAL_EXTENSIONS=(
    "ms-python.python"
    "ms-python.vscode-pylance"
    "ms-python.black-formatter"
    "ms-python.isort"
    "ms-python.flake8"
    "ms-python.pylint"
    "github.copilot"
    "github.copilot-chat"
    "github.vscode-pull-request-github"
    "github.vscode-github-actions"
)

# Hitung total
total=${#EXTENSIONS_TO_REMOVE[@]}
count=0

# Uninstall extensions yang tidak diperlukan
for ext in "${EXTENSIONS_TO_REMOVE[@]}"; do
    count=$((count + 1))
    echo "[$count/$total] Removing: $ext"
    code-insiders --uninstall-extension "$ext" 2>/dev/null || echo "  ⚠️  Extension not found or already removed"
done

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📦 Verifying essential extensions are installed..."
echo ""

# Pastikan essential extensions terinstall
for ext in "${ESSENTIAL_EXTENSIONS[@]}"; do
    if code-insiders --list-extensions | grep -q "^$ext$"; then
        echo "  ✅ $ext"
    else
        echo "  ⚠️  Installing: $ext"
        code-insiders --install-extension "$ext" --force
    fi
done

echo ""
echo "🎉 VS Code cleanup and configuration complete!"
echo ""
echo "Remaining extensions:"
code-insiders --list-extensions | wc -l
echo ""
echo "Run 'code-insiders --list-extensions' to see all installed extensions"
