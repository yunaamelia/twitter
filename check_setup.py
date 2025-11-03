#!/usr/bin/env python3
"""
Quick verification script to check VS Code setup
"""
import subprocess
import sys
from pathlib import Path


def check_command(cmd, name):
    """Check if command exists"""
    try:
        subprocess.run([cmd, "--version"], capture_output=True, check=True)
        print(f"✅ {name} installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"❌ {name} not found")
        return False

def check_file(path, name):
    """Check if file exists"""
    if Path(path).exists():
        print(f"✅ {name} exists")
        return True
    else:
        print(f"❌ {name} missing")
        return False

def main():
    print("🔍 Checking VS Code Development Setup\n")
    
    checks = []
    
    # Check Python
    checks.append(check_command("python3", "Python 3"))
    
    # Check venv
    venv_path = Path(".venv/bin/python")
    if venv_path.exists():
        print(f"✅ Virtual environment exists")
        checks.append(True)
    else:
        print(f"❌ Virtual environment missing")
        checks.append(False)
    
    # Check pip packages
    print("\n📦 Checking Python packages:")
    try:
        result = subprocess.run(
            [str(venv_path), "-m", "pip", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        packages = result.stdout.lower()
        
        for pkg in ["tweepy", "black", "isort", "pylint", "flake8", "pytest"]:
            if pkg in packages:
                print(f"  ✅ {pkg}")
            else:
                print(f"  ❌ {pkg}")
    except Exception as e:
        print(f"  ❌ Error checking packages: {e}")
    
    # Check configuration files
    print("\n📁 Checking configuration files:")
    config_files = [
        (".vscode/settings.json", "VS Code settings"),
        (".vscode/launch.json", "Debug configs"),
        (".vscode/tasks.json", "Tasks"),
        (".vscode/extensions.json", "Extensions"),
        (".github/copilot-instructions.md", "Copilot instructions"),
        ("Makefile", "Makefile"),
        (".pylintrc", "Pylint config"),
        (".flake8", "Flake8 config"),
        ("pyproject.toml", "Project config"),
        (".env", "Environment file"),
    ]
    
    for file_path, name in config_files:
        checks.append(check_file(file_path, name))
    
    # Check directories
    print("\n📂 Checking directories:")
    dirs = [
        (".vscode", "VS Code config"),
        (".github", "GitHub config"),
        ("tests", "Tests"),
    ]
    
    for dir_path, name in dirs:
        checks.append(check_file(dir_path, name))
    
    # Summary
    print("\n" + "="*50)
    passed = sum(checks)
    total = len(checks)
    print(f"✅ {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! VS Code is ready for development!")
        print("\nNext steps:")
        print("1. Edit .env with your Twitter API credentials")
        print("2. Run: make verify")
        print("3. Run: make run")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
