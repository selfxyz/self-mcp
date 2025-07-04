#!/usr/bin/env python3
"""CLI entry point for self-mcp"""

import subprocess
import sys
from pathlib import Path


def main():
    """Start the Self MCP server"""
    # Find the server.py file relative to this package
    server_path = Path(__file__).parent / "server.py"
    
    # Run the server with the same Python interpreter
    subprocess.run([sys.executable, str(server_path)])


if __name__ == "__main__":
    main()