#!/usr/bin/env python3
"""CLI entry point for self-mcp"""

import subprocess
import sys
from pathlib import Path


def main():
    """Start the Self MCP server"""
    # Import and run directly to avoid subprocess import issues
    from self_mcp.server import run
    run()


if __name__ == "__main__":
    main()