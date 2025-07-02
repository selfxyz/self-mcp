# Self MCP Server

A Model Context Protocol (MCP) server that helps developers integrate the Self protocol for privacy-preserving identity verification using government-issued IDs.

## Overview

This MCP server provides AI-powered assistance for developers working with the Self protocol. It helps with integration, code generation, and debugging - making it easier to add passport-based verification to your applications.

## Current Capabilities

### 🛠️ Three Core Tools

1. **`explain_self_integration`**
   - Get detailed integration guides for specific use cases
   - Available use cases:
     - `"airdrop"` - Protect token distributions from bots
     - `"age-verification"` - Verify age without revealing birthdate
     - `"humanity-check"` - Confirm users are real humans

2. **`generate_verification_code`**
   - Generate working code snippets for your integration
   - Components available:
     - `"frontend-qr"` - QR code setup for web apps
     - `"backend-verify"` - Server-side proof verification
     - `"smart-contract"` - Solidity contracts for on-chain verification
   - Languages supported:
     - `"typescript"` (default)
     - `"javascript"`
     - `"solidity"` (for smart contracts only)

3. **`debug_verification_error`**
   - Diagnose and fix Self verification errors
   - Provides solutions for common issues:
     - Scope mismatches
     - Invalid proofs
     - Age verification problems
     - Nullifier reuse
     - Network errors

## Installation

### Prerequisites

- Python 3.12 or higher
- pip package manager

### Install Steps

1. Clone or download this repository
2. Navigate to the server directory:
   ```bash
   cd /path/to/self-mcp
   ```
3. Install the package:
   ```bash
   pip install -e .
   ```

## Usage

### With Claude Desktop

1. **Add to Claude Desktop configuration:**

   Find your config file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

   Add this configuration:
   ```json
   {
     "mcpServers": {
       "self-mcp": {
         "command": "python",
         "args": ["-m", "server"],
         "cwd": "/absolute/path/to/self-mcp"
       }
     }
   }
   ```

2. **Restart Claude Desktop**

3. **Look for the MCP indicator** (plug icon) in the chat interface

4. **Start using it!** Try these prompts:
   - "How do I integrate Self for an airdrop?"
   - "Generate backend verification code for Self in TypeScript"
   - "Help me debug: Invalid scope validation failed"

### Manual Testing

Test the server directly:
```bash
python -m server
```

Or test individual tools:
```bash
python test_server.py
```

### With MCP Inspector

For debugging and testing:
```bash
npm install -g @modelcontextprotocol/inspector
mcp-inspector python -m server
```

## Examples

### Integration Guide
```
User: "How do I integrate Self for age verification?"
Assistant: [Provides detailed guide with steps, code examples, and best practices]
```

### Code Generation
```
User: "Generate frontend QR code for Self"
Assistant: [Provides complete TypeScript/React code with configuration]
```

### Error Debugging
```
User: "Debug: Invalid scope validation failed"
Assistant: [Explains the scope mismatch issue and shows how to fix it]
```

## What Values Are Required?

### For `explain_self_integration`:
- `use_case`: Must be one of: `"airdrop"`, `"age-verification"`, `"humanity-check"`

### For `generate_verification_code`:
- `component`: Must be one of: `"frontend-qr"`, `"backend-verify"`, `"smart-contract"`
- `language` (optional): Defaults to `"typescript"`. Can be `"javascript"` or `"solidity"`

### For `debug_verification_error`:
- `error_message`: The error text you're seeing
- `context` (optional): Hint about error type like `"scope-mismatch"`, `"proof-invalid"`, etc.

## What's Possible Currently?

✅ **You can:**
- Get step-by-step integration guides
- Generate working code for frontend, backend, and smart contracts
- Debug common Self protocol errors
- Learn best practices for privacy-preserving verification
- Understand how to implement airdrops, age gates, and humanity checks

❌ **Not yet implemented:**
- Direct blockchain interaction
- Proof generation/validation
- Live testing tools
- Resource access (documentation, contract addresses)
- Interactive prompts for guided setup

## Technical Details

- Built with FastMCP for simple, Pythonic MCP server creation
- Uses real Self protocol SDK patterns and best practices
- No external API calls - all knowledge is embedded
- Supports async operations
- Type-safe with Python type hints

## Project Structure

```
self-mcp/
├── server.py          # Main MCP server with tools
├── test_server.py     # Local testing script
├── pyproject.toml     # Package configuration
├── README.md          # This file
├── __init__.py        # Package init
└── .gitignore        # Git ignore rules
```

## Troubleshooting

**"MCP server not found"**
- Ensure Python path is correct in Claude config
- Use absolute paths, not relative
- Check Python version: `python --version` (needs 3.12+)

**"Module not found"**
- Make sure you ran `pip install -e .` in the correct directory
- Try using `python3` instead of `python` in config

**"Tools not showing"**
- Restart Claude Desktop completely
- Check for errors in Claude's developer console
- Verify the server runs manually: `python -m server`

## Future Enhancements

Potential additions:
- More tools for testing and deployment
- Resources for accessing documentation
- Prompts for interactive setup workflows
- Support for more signature algorithms
- Integration with live blockchain data

## License

MIT License

## Contributing

This is an MVP implementation. Contributions welcome for:
- Additional error patterns and solutions
- More code templates
- Extended use case guides
- Support for more frameworks and languages