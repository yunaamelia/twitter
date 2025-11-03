#!/usr/bin/env python3
"""
Quick development script runner
Usage: python dev.py [command]
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    """Run shell command"""
    return subprocess.run(cmd, shell=True, cwd=Path(__file__).parent)

def main():
    commands = {
        'run': 'python main.py',
        'verify': 'python setup_verify.py',
        'stats': 'python stats.py',
        'format': 'black --line-length 100 *.py && isort *.py',
        'lint': 'pylint *.py && flake8 *.py --max-line-length=100',
        'clean': 'find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; find . -type f -name "*.pyc" -delete',
        'db': 'sqlite3 giveaways.db',
        'logs': 'tail -f bot.log',
        'install': 'pip install -r requirements.txt',
        'install-dev': 'pip install -r requirements-dev.txt',
    }
    
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print("Available commands:")
        for cmd, desc in commands.items():
            print(f"  {cmd:12} - {desc}")
        sys.exit(1)
    
    cmd = sys.argv[1]
    print(f"Running: {commands[cmd]}")
    run_command(commands[cmd])

if __name__ == '__main__':
    main()
