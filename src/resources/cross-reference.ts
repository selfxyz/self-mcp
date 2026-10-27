import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { ServerConfig } from "../config.js";

const CONTENT = `# Self Protocol: Cross-Reference Guide

## Two MCP Servers

Self has two MCP servers. Route each question to the one that matches it.

### self-protocol MCP (this server)
For **developers** integrating Self identity verification into their apps. It covers:
- Passport/ID card NFC scanning and ZK proof generation
- On-chain proof verification via IdentityVerificationHub V2
- Selective disclosure (age, nationality, OFAC, etc.)
- Building custom verifier contracts (SelfVerificationRoot)
- React Native SDK integration (@selfxyz/rn-sdk)
- Server-side verification (@selfxyz/core)

### Self Agent ID MCP
For **AI agents** and the services they talk to. Self Agent ID is an ERC-8004 agent registry on Celo with a proof-of-human extension: each agent is a soulbound ERC-721 bound to a human verified with Self. It covers:
- Registering an agent with proof-of-human (the human scans their document in the Self app)
- Checking registration status, looking up agents, listing a human's agents, deregistering
- Signing outgoing HTTP requests as a registered agent
- Verifying another agent's identity or an incoming signed request

Connect either way:
- Hosted, zero install: \`https://agent-api.self.xyz/api/mcp\`
- npm stdio package: \`@selfxyz/mcp-server\` (\`npx @selfxyz/mcp-server\`), source at https://github.com/selfxyz/self-agent-id-mcp

MCP guide: https://docs.self.xyz/docs/agent-id/guides/mcp-user/

## When To Use Each

| Question | MCP Server |
|----------|------------|
| "How do I verify a user's passport/identity?" | **self-protocol MCP** (this one) |
| "How do I build a custom verifier contract?" | **self-protocol MCP** (this one) |
| "How do I integrate the Self SDK into my React Native app?" | **self-protocol MCP** (this one) |
| "How do I register my AI agent with proof-of-human?" | **Self Agent ID MCP** |
| "How do I sign HTTP requests as an authenticated agent?" | **Self Agent ID MCP** |
| "How do I verify another AI agent is human-backed?" | **Self Agent ID MCP** |
| "How do I check agent requests in my backend?" | **Self Agent ID MCP** |

## Self Agent ID Quick Reference

Docs: https://docs.self.xyz/docs/agent-id/overview/

**SDK and API**
- TypeScript: \`@selfxyz/agent-sdk\` (0.3.0), the only SDK. \`SelfAgent\` signs requests; \`SelfAgentVerifier\` verifies them, with chainable requirements such as \`.requireAge(18)\`, \`.requireOFAC()\`, \`.requireNationality("USA")\`.
- Other languages: the REST API at https://agent-api.self.xyz
- Agents sign requests with ECDSA (or Ed25519) and send \`x-self-agent-*\` headers.

**Contracts (Celo)**

| Contract | Celo Mainnet (42220) | Celo Sepolia (11142220) |
|----------|----------------------|-------------------------|
| SelfAgentRegistry | \`0xaC3DF9ABf80d0F5c020C06B04Cced27763355944\` | \`0x043DaCac8b0771DD5b444bCC88f2f8BBDBEdd379\` |
| SelfReputationRegistry | \`0x69Da18CF4Ac27121FD99cEB06e38c3DC78F363f4\` | \`0x3Bb0A898C1C0918763afC22ff624131b8F420CC2\` |
| SelfValidationRegistry | \`0x71a025e0e338EAbcB45154F8b8CA50b41e7A0577\` | \`0x84cA20B8A1559F136dA03913dbe6A7F68B6B240B\` |

- **SelfAgentRegistry**: ERC-8004 identity registry plus \`IERC8004ProofOfHuman\`. Agents register through Self Hub V2 (Self app flow) or \`registerWithHumanProof()\`; the plain ERC-8004 \`register()\` overloads revert with \`ProofRequired()\` while \`requireHumanProof\` is on (the default). Proofs expire at the earlier of document expiry and \`maxProofAge\` (default 365 days); use \`isProofFresh(agentId)\` to check.
- **SelfReputationRegistry**: ERC-8004 reputation registry for SelfAgentRegistry agents. Registration records a "proof-of-human" feedback entry weighted by document type.
- **SelfValidationRegistry**: ERC-8004 validation registry. External validators use \`validationRequest\`/\`validationResponse\`; \`submitFreshnessValidation(agentId)\` records Self's built-in proof-freshness check.

For contract details, registration modes and agent documents (ERC-8004 registration file / A2A Agent Card), see the Agent ID docs above.
`;

export function registerCrossReference(
  server: McpServer,
  config: ServerConfig
): void {
  server.resource(
    "cross-reference",
    "self://cross-reference",
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          mimeType: "text/plain" as const,
          text: CONTENT,
        },
      ],
    })
  );
}
