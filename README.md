# Self MCP Server

A Model Context Protocol (MCP) server that helps developers integrate the Self protocol for privacy-preserving identity verification using government-issued IDs.

## Overview

This MCP server provides AI-powered assistance for developers working with the Self protocol. It helps with integration, code generation, and debugging - making it easier to add passport-based verification to your applications.

## Current Capabilities

### 🛠️ Five Core Tools

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

4. **`check_self_status`**
   - Check Self protocol deployment status
   - Get contract addresses for different networks
   - View RPC endpoints and block explorers

5. **`generate_verification_config`**
   - Generate complete verification configurations
   - Creates matching frontend and backend code
   - Supports all verification options

## Installation

### Prerequisites

- Python 3.12 or higher
- pip package manager

### Install Steps

1. Clone the repository:
   ```bash
   git clone git@github.com:selfxyz/self-mcp.git
   cd self-mcp
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package:
   ```bash
   pip install -e .
   ```
   
   Or install directly without editable mode:
   ```bash
   pip install .
   ```

4. Verify installation:
   ```bash
   python -c "import self_mcp; print('✅ Self MCP installed successfully')"
   ```

## Usage

### With Cursor

1. **Create MCP configuration file:**

   Create a file called `mcp.json` in your project root with this configuration:
   
   ```json
   {
     "mcpServers": {
       "self-mcp": {
         "command": "python",
         "args": ["/path/to/self-mcp/server.py"],
         "env": {
           "PYTHONPATH": "/path/to/self-mcp"
         }
       }
     }
   }
   ```

   **For virtual environment (recommended):**
   ```json
   {
     "mcpServers": {
       "self-mcp": {
         "command": "/path/to/self-mcp/venv/bin/python",
         "args": ["/path/to/self-mcp/server.py"],
         "env": {
           "PYTHONPATH": "/path/to/self-mcp"
         }
       }
     }
   }
   ```

2. **Enable in Cursor:**
   - Open Cursor Settings
   - Go to Features → Composer
   - Enable "Model Context Protocol"
   - Cursor will automatically detect the `mcp.json` file

3. **Use in Composer:**
   - Open Composer (Cmd/Ctrl + K)
   - The Self MCP tools will appear under "Available Tools"
   - Ask questions like:
     - "How do I integrate Self for age verification?"
     - "Generate TypeScript code for Self QR verification"
     - "Debug Self error: Invalid scope validation"

4. **Toggle specific tools:**
   - Click on tool names in the tools list to enable/disable them
   - Disabled tools won't be loaded into context

### With Claude Desktop

1. **Add to Claude Desktop configuration:**

   Find your config file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

   Add this configuration with **ABSOLUTE PATHS** (replace with your actual paths):
   
   **Option 1: Using system Python**
   ```json
   {
     "mcpServers": {
       "self-mcp": {
         "command": "python3",
         "args": ["server.py"],
         "cwd": "/Users/YOUR_USERNAME/path/to/self-mcp"
       }
     }
   }
   ```

   **Option 2: Using virtual environment (RECOMMENDED)**
   ```json
   {
     "mcpServers": {
       "self-mcp": {
         "command": "/Users/YOUR_USERNAME/path/to/self-mcp/venv/bin/python",
         "args": ["/Users/YOUR_USERNAME/path/to/self-mcp/server.py"],
         "cwd": "/Users/YOUR_USERNAME/path/to/self-mcp"
       }
     }
   }
   ```

   **Important Notes:**
   - ⚠️ Use ABSOLUTE paths (starting with `/` on macOS/Linux or `C:\` on Windows)
   - ⚠️ Replace `YOUR_USERNAME` with your actual username
   - ⚠️ The `cwd` should point to the directory containing `server.py`
   - ✅ Using a virtual environment is recommended for dependency isolation

2. **Restart Claude Desktop**

3. **Look for the MCP indicator** (plug icon) in the chat interface

4. **Start using it!** Try these prompts:
   - "How do I integrate Self for an airdrop?"
   - "Generate backend verification code for Self in TypeScript"
   - "Help me debug: Invalid scope validation failed"

### Manual Testing

Test the server directly:
```bash
python server.py
```

Or test individual tools:
```bash
python test_server.py
```

### Real Example Configuration

Here's an actual working configuration (replace paths with yours):

```json
{
  "mcpServers": {
    "self-mcp": {
      "command": "/Users/nightmare/Projects/self-mcp/venv/bin/python",
      "args": ["/Users/nightmare/Projects/self-mcp/server.py"],
      "cwd": "/Users/nightmare/Projects/self-mcp"
    }
  }
}
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
- Access contract addresses and network configurations
- Generate custom verification configurations
- View complete example implementations
- Access best practices documentation

### 📚 New Resources Available:
- `self://contracts/addresses` - Get deployed contract addresses
- `self://examples/airdrop` - Complete airdrop example
- `self://examples/age-gate` - Age verification example
- `self://docs/best-practices` - Integration best practices

### 💬 New Prompts:
- `design-verification-flow` - Interactive flow design
- `troubleshoot-integration` - Step-by-step troubleshooting

❌ **Not yet implemented:**
- Direct blockchain interaction
- Proof generation/validation
- Live testing tools
- Sampling (LLM callbacks)

## Technical Details

- Built with FastMCP 2.0 for enhanced MCP server capabilities
- Uses tool annotations for better LLM understanding
- Implements Context support for logging and progress reporting
- Uses real Self protocol SDK patterns and best practices
- No external API calls - all knowledge is embedded
- Supports async operations
- Type-safe with Python type hints

## Project Structure

```
self-mcp/
├── server.py             # Entry point for MCP server
├── self_mcp/             # Main package directory
│   ├── __init__.py       # Package initialization
│   ├── server.py         # MCP server setup
│   ├── tools/            # Tool implementations
│   │   ├── integration.py
│   │   ├── code_generation.py
│   │   ├── debugging.py
│   │   ├── status.py
│   │   └── config_generation.py
│   ├── resources/        # Resource handlers
│   │   ├── contract_addresses.py
│   │   ├── examples.py
│   │   └── best_practices.py
│   ├── prompts/          # Interactive prompts
│   │   ├── design_flow.py
│   │   └── troubleshooting.py
│   └── templates/        # Data templates
│       ├── integration_guides.py
│       ├── code_templates.py
│       ├── error_solutions.py
│       └── examples.py
├── test_server.py        # Testing script
├── pyproject.toml        # Package configuration
├── README.md             # This file
└── .gitignore           # Git ignore rules
```

## Troubleshooting

### Common Issues

**"MCP server not found" or "spawn python ENOENT"**
- ❌ Problem: Claude can't find Python
- ✅ Solution: Use full absolute path to Python executable
  ```json
  "command": "/usr/bin/python3"  // or wherever your Python is
  ```
- To find your Python path: `which python3`

**"No module named server" or "Module not found"**
- ❌ Problem: Python can't find the server module
- ✅ Solution: Use absolute path in args
  ```json
  "args": ["/Users/YOUR_USERNAME/path/to/self-mcp/server.py"]
  ```

**"Server disconnected" immediately**
- ❌ Problem: Server crashes on startup
- ✅ Solution: Test manually first
  ```bash
  cd /path/to/self-mcp
  python server.py  # Should wait quietly (Ctrl+C to stop)
  ```

**Virtual environment issues**
- ❌ Problem: Dependencies not found
- ✅ Solution: Use venv Python in config
  ```json
  "command": "/path/to/self-mcp/venv/bin/python"
  ```

### Debugging Steps

1. **Test the server manually:**
   ```bash
   cd /path/to/self-mcp
   /path/to/venv/bin/python server.py
   ```
   Should run without output. Press Ctrl+C to stop.

2. **Check Claude logs:**
   - Open Claude Desktop
   - View → Developer → Developer Tools
   - Check Console for errors

3. **Verify paths are absolute:**
   - ✅ Good: `/Users/john/Projects/self-mcp`
   - ❌ Bad: `~/Projects/self-mcp` or `./self-mcp`

4. **Common working configuration:**
   ```json
   {
     "mcpServers": {
       "self-mcp": {
         "command": "/Users/YOUR_USERNAME/Projects/self-mcp/venv/bin/python",
         "args": ["/Users/YOUR_USERNAME/Projects/self-mcp/server.py"],
         "cwd": "/Users/YOUR_USERNAME/Projects/self-mcp"
       }
     }
   }
   ```

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