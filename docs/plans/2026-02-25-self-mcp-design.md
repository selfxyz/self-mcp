# Self Protocol MCP Server — Design Document

## Goal

A comprehensive MCP server (`@selfxyz/self-mcp`) that gives AI assistants deep knowledge of the Self Protocol ecosystem — SDK integration, smart contracts, verification flows, supported documents, and architecture — so they can help developers build with Self.

## Scope Boundary

- **This MCP:** Self Protocol for developers — SDK setup, contract integration, verification flows, document/country support
- **self-agent-id-mcp:** Agent identity lifecycle — registration, auth, verification of AI agents (ERC-8004)
- **Cross-reference:** Each MCP references the other when relevant

## Architecture

Layered MCP server with resources organized by domain, prompts for guided workflows, and a small set of active on-chain query tools. Built with the same tech stack as self-agent-id-mcp for consistency (TypeScript, @modelcontextprotocol/sdk, ethers.js, zod).

## Domains

### Resources (read-only knowledge)

| URI | Content |
|-----|---------|
| `self://overview` | Protocol architecture, verification flow, ZK proof pipeline |
| `self://sdk/core` | @selfxyz/core (SelfBackendVerifier) — server-side proof verification |
| `self://sdk/react-native` | @selfxyz/rn-sdk — SelfVerification component, bridge handlers |
| `self://sdk/mobile-alpha` | @selfxyz/mobile-sdk-alpha — adapters, flows, SelfClient |
| `self://sdk/webview-bridge` | @selfxyz/webview-bridge — bridge protocol, domains, message types |
| `self://sdk/kmp` | @selfxyz/kmp-sdk — Kotlin Multiplatform setup |
| `self://sdk/common` | @selfxyz/common — utilities, types, constants |
| `self://contracts` | Hub V2, registries, addresses (mainnet + testnet), ABIs |
| `self://contracts/verifier-guide` | How to build custom verifiers extending SelfVerificationRoot |
| `self://documents` | Supported document types, countries, disclosure attributes |
| `self://circuits` | Circuit types, signature algorithms, attestation IDs |
| `self://cross-reference` | Links to self-agent-id-mcp for agent identity topics |

### Tools (active on-chain queries)

| Tool | Description |
|------|-------------|
| `self_check_verification` | Check if a commitment root is valid in a registry |
| `self_get_contract_addresses` | Get current deployed addresses for a given chain |
| `self_get_registry_info` | Query registry state (merkle root, tree size, OFAC roots) |

### Prompts (guided workflows)

| Prompt | Description |
|--------|-------------|
| `self_integrate_sdk` | Step-by-step guide to adding Self verification to an app (framework-specific) |
| `self_deploy_verifier` | Guide to building and deploying a custom SelfVerificationRoot contract |
| `self_verify_proof_backend` | Guide to setting up server-side proof verification with @selfxyz/core |

## Tech Stack

- TypeScript 5.7, ES2022 target, Node16 modules
- @modelcontextprotocol/sdk ^1.26.0
- ethers ^6.16.0 (for on-chain query tools)
- zod ^3.23.0 (input validation)
- vitest ^3.0.0 (testing)
