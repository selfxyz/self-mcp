# Self MCP Server

MCP server for [Self protocol](https://self.xyz) integration assistance. Helps developers add privacy-preserving identity verification to their apps.

## Features

- **Core Self Protocol Tools**: Integration guides, code generation, debugging assistance
- **Tools.self.xyz Integration**: Direct interaction with blockchain for reading configurations and generating hashes
- **Web3 Integration**: Read-only blockchain operations (no write operations to keep it free)
- **Comprehensive Documentation**: Resources and prompts for Self protocol development

## Installation

### Option 1: Install from GitHub (Recommended)
```bash
pip install git+https://github.com/selfxyz/self-mcp.git
```

After installation, run with: `self-mcp`

### Option 2: Local Development Setup

1. **Clone the repository**:
```bash
git clone https://github.com/selfxyz/self-mcp.git
cd self-mcp
```

2. **Create virtual environment**:
```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**:
```bash
cd self-mcp
pip install -e .
```

4. **Verify installation**:
```bash
python server.py  # Should start without errors
```

## Configuration

### For Claude Desktop

Add to `claude_desktop_config.json`:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "self-mcp": {
      "command": "/path/to/your/python",
      "args": [
        "/path/to/self-mcp/self-mcp/server.py"
      ],
      "cwd": "/path/to/self-mcp/self-mcp"
    }
  }
}
```

### For Cursor

Create `mcp.json` in your project root:

#### Option 1: Using Python directly (simple)
```json
{
  "mcpServers": {
    "self-mcp": {
      "command": "/path/to/your/python",
      "args": [
        "/path/to/self-mcp/self-mcp/server.py"
      ],
      "cwd": "/path/to/self-mcp/self-mcp"
    }
  }
}
```

#### Option 2: Using uv (recommended for dependency management)
```json
{
  "mcpServers": {
    "self-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--with", "fastmcp",
        "--with", "web3",
        "--with", "aiohttp",
        "python",
        "/path/to/self-mcp/self-mcp/server.py"
      ],
      "cwd": "/path/to/self-mcp/self-mcp"
    }
  }
}
```

Replace `/path/to/your/python` with your Python interpreter path (e.g., `/Users/nightmare/Projects/self-work/self-mcp/venv/bin/python`) and `/path/to/self-mcp` with the actual path to your self-mcp directory.

**Note**: The `cwd` (current working directory) parameter sets the directory where the server process will run. This is important for relative file paths and ensuring the server finds its dependencies.

Then enable MCP in Cursor settings → cursor settings → Tools and Integrations → New MCP Server
This will open mcp.json of cursor where you can put the above configuration.

## Available Tools

### Core Tools

#### 1. `explain_self_integration`
Get integration guides for specific use cases.
- **use_case**: `"airdrop"` | `"age-verification"` | `"humanity-check"`

#### 2. `generate_verification_code`
Generate code for Self integration.
- **component**: `"frontend-qr"` | `"backend-verify"` | `"smart-contract"`
- **language**: `"typescript"` | `"javascript"` | `"solidity"`

#### 3. `debug_verification_error`
Debug Self verification errors.
- **error_message**: The error you're seeing
- **context**: Optional hint about error type

#### 4. `check_self_status`
Check Self protocol network status and contracts.
- **network**: `"celo-mainnet"` | `"celo-testnet"`

#### 5. `generate_verification_config`
Generate complete verification configuration.
- **requirements**: Dict with app settings

#### 6. `explain_sdk_setup`
Understand SDK backend requirements.
- **topic**: `"config-storage"` | `"user-id-type"` | `"attestation-ids"` | `"full-setup"`

#### 7. `generate_eu_id_verification`
Generate EU ID card verification code (V2).
- **component**: `"frontend"` | `"backend"` | `"smart-contract"`
- **language**: `"typescript"` | `"javascript"` | `"solidity"`

### Tools.self.xyz Integration Tools

#### 8. `generate_scope_hash`
Generate a deterministic scope hash for an address/URL and seed.
- **address_or_url**: The address or URL to hash
- **scope_seed**: The seed value for scope generation

#### 9. `generate_config_id`
Generate a config ID from verification requirements and check blockchain existence.
- **minimum_age**: Optional minimum age requirement
- **excluded_countries**: Optional list of excluded country codes
- **ofac_enabled**: Optional list of OFAC check settings for each ID type
- **network**: `"mainnet"` | `"testnet"`

#### 10. `read_hub_config`
Read configuration details from the Hub contract.
- **config_id**: The config ID to read
- **network**: `"mainnet"` | `"testnet"`

#### 11. `list_country_codes`
List available country codes for verification configuration.
- **search**: Optional search term to filter countries

#### 12. `guide_to_tools`
Generate a link to tools.self.xyz with pre-filled parameters.
- **action**: `"deploy-config"` | `"connect-wallet"` | `"select-countries"` | `"generate-scope"` | `"read-config"`
- **parameters**: Optional dict with pre-fill values

## Example Usage

```
User: "How do I integrate Self for age verification?"
Assistant: [Provides step-by-step guide with code examples]

User: "Generate backend verification code in TypeScript"
Assistant: [Provides complete backend code with proper SDK setup]

User: "Explain config storage setup"
Assistant: [Shows IConfigStorage implementation examples]
```

## Resources

- **Contract Addresses**: `self://contracts/addresses`
- **Integration Examples**: `self://examples/{airdrop|age-gate}`
- **Best Practices**: `self://docs/best-practices`

## Prompts

- **Design Flow**: `design-verification-flow`
- **Troubleshooting**: `troubleshoot-integration`

## Development

```bash
# Clone repo
git clone https://github.com/selfxyz/self-mcp.git
cd self-mcp

# Install in development mode
pip install -e .

# Run tests
python test_server.py
```

## License

MIT