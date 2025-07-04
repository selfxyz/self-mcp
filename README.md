# Self MCP Server

MCP server for [Self protocol](https://self.xyz) integration assistance. Helps developers add privacy-preserving identity verification to their apps.

## Installation

```bash
pip install git+https://github.com/selfxyz/self-mcp.git
```

After installation, run with: `self-mcp`

### Development Installation
```bash
git clone https://github.com/selfxyz/self-mcp.git
cd self-mcp/self-mcp
pip install -e .
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
      "command": "self-mcp"
    }
  }
}
```

### For Cursor

Create `mcp.json` in your project root:

```json
{
  "mcpServers": {
    "self-mcp": {
      "command": "self-mcp"
    }
  }
}
```

Then enable MCP in Cursor settings → Features → Composer → Model Context Protocol.

## Available Tools

### 1. `explain_self_integration`
Get integration guides for specific use cases.
- **use_case**: `"airdrop"` | `"age-verification"` | `"humanity-check"`

### 2. `generate_verification_code`
Generate code for Self integration.
- **component**: `"frontend-qr"` | `"backend-verify"` | `"smart-contract"`
- **language**: `"typescript"` | `"javascript"` | `"solidity"`

### 3. `debug_verification_error`
Debug Self verification errors.
- **error_message**: The error you're seeing
- **context**: Optional hint about error type

### 4. `check_self_status`
Check Self protocol network status and contracts.
- **network**: `"celo-mainnet"` | `"celo-testnet"`

### 5. `generate_verification_config`
Generate complete verification configuration.
- **requirements**: Dict with app settings

### 6. `explain_sdk_setup`
Understand SDK backend requirements.
- **topic**: `"config-storage"` | `"user-id-type"` | `"attestation-ids"` | `"full-setup"`

### 7. `generate_eu_id_verification`
Generate EU ID card verification code (V2).
- **component**: `"frontend"` | `"backend"` | `"smart-contract"`
- **language**: `"typescript"` | `"javascript"` | `"solidity"`

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