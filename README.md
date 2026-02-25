# Self Protocol MCP Server

MCP server that provides AI assistants with comprehensive knowledge of the [Self Protocol](https://self.xyz) ecosystem — identity verification SDK, smart contracts, ZK circuits, and integration guidance.

## What This Does

When connected to an AI assistant (Claude, Cursor, Windsurf, etc.), this MCP server gives it deep context about Self Protocol so it can help developers:

- Integrate the Self SDK into React Native, web, and Kotlin apps
- Build custom on-chain verifier contracts using `SelfVerificationRoot`
- Set up server-side proof verification with `@selfxyz/core`
- Understand the contract architecture, supported documents, and ZK circuits
- Query on-chain registry state

## Installation

### Claude Code / Cursor / Windsurf

Add to your `.mcp.json`:

```json
{
  "self-protocol": {
    "command": "npx",
    "args": ["@selfxyz/self-mcp"]
  }
}
```

### Manual

```bash
npm install -g @selfxyz/self-mcp
self-mcp
```

## Resources

| URI | Description |
|-----|-------------|
| `self://overview` | Protocol architecture, verification flow, key components |
| `self://contracts` | Deployed contract addresses (mainnet + testnet), interface signatures |
| `self://contracts/verifier-guide` | How to build custom verifiers with `SelfVerificationRoot` |
| `self://sdk/core` | `@selfxyz/core` — server-side proof verification API |
| `self://sdk/react-native` | `@selfxyz/rn-sdk` — React Native integration |
| `self://sdk/mobile-alpha` | `@selfxyz/mobile-sdk-alpha` — cross-platform SDK core |
| `self://sdk/webview-bridge` | `@selfxyz/webview-bridge` — bridge protocol (10 domains) |
| `self://sdk/kmp` | `@selfxyz/kmp-sdk` — Kotlin Multiplatform SDK |
| `self://sdk/common` | `@selfxyz/common` — shared utilities, types, `SelfAppBuilder` |
| `self://documents` | Supported document types, countries, disclosure attributes |
| `self://circuits` | ZK circuit types, signature algorithms, proof structure |
| `self://cross-reference` | Relationship to self-agent-id MCP, ERC-8004 agent identity |

## Tools

| Tool | Description |
|------|-------------|
| `self_get_contract_addresses` | Get deployed contract addresses for mainnet or testnet |
| `self_check_verification` | Check if a merkle root is valid in an identity registry |
| `self_get_registry_info` | Query registry state (merkle root, OFAC roots) |

## Prompts

| Prompt | Description |
|--------|-------------|
| `self_integrate_sdk` | Step-by-step SDK integration guide (React Native, web, Kotlin, server) |
| `self_deploy_verifier` | Guide to building and deploying a custom verifier contract |
| `self_verify_proof_backend` | Server-side proof verification setup (Express, Hono, Next.js) |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SELF_NETWORK` | `mainnet` | Network: `mainnet` or `testnet` |
| `SELF_RPC_URL` | (per network) | Custom Celo RPC URL |

## Related

- **[self-agent-id-mcp](https://github.com/selfxyz/self-agent-id-mcp)** — MCP server for AI agent identity (ERC-8004 proof-of-human registration, authentication, verification)
- **[Self Protocol](https://self.xyz)** — Identity verification using passport NFC + zero-knowledge proofs
- **[Self on Celo](https://celoscan.io/address/0xe57F4773bd9c9d8b6Cd70431117d353298B9f5BF)** — IdentityVerificationHub on mainnet

## License

MIT
