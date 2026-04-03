const CONTENT = `# Self Protocol — Cross-Reference Guide

## Two-MCP Architecture

Self's tooling is split across two separate MCP servers, each serving a distinct audience and purpose.

### self-protocol MCP (this server)
Helps **developers** integrate Self identity verification into their apps. This is the MCP you are currently using. It covers:
- Passport/ID card NFC scanning and ZK proof generation
- On-chain proof verification via IdentityVerificationHub V2
- Selective disclosure (age, nationality, OFAC, etc.)
- Building custom verifier contracts (SelfVerificationRoot)
- React Native SDK integration (@selfxyz/rn-sdk)
- Server-side verification (@selfxyz/core)

### self-agent-id MCP
Helps **AI agents** manage their own on-chain identity via ERC-8004. It covers:
- Registering an AI agent with a soulbound NFT on Celo
- Proof-of-human verification using Self's ZK passport system
- EIP-712 agent wallet signing for HTTP request authentication
- Verifying other agents' human-backed status
- Agent reputation and validation registries
- TypeScript SDK for agent identity management (@selfxyz/agent-sdk)

## When To Use Each

| Question | MCP Server |
|----------|------------|
| "How do I verify a user's passport/identity?" | **self-protocol MCP** (this one) |
| "How do I build a custom verifier contract?" | **self-protocol MCP** (this one) |
| "How do I integrate the Self SDK into my React Native app?" | **self-protocol MCP** (this one) |
| "How do I register my AI agent with proof-of-human?" | **self-agent-id MCP** |
| "How do I sign HTTP requests as an authenticated agent?" | **self-agent-id MCP** |
| "How do I verify another AI agent is human-backed?" | **self-agent-id MCP** |

## Self Agent ID System (ERC-8004)

The agent identity system has undergone a major ERC-8004 compliance overhaul.

### SelfAgentRegistry

ERC-721 + soulbound + IERC8004ProofOfHuman extension.

**Registration Modes:**
- Simple — minimal registration
- Advanced — full metadata at registration time
- Wallet-free — gasless registration via relayer
- Smart-wallet — account abstraction compatible

**Base ERC-8004 register() Overloads (3 required by spec):**
- \`register()\` — minimal registration, no arguments
- \`register(agentURI)\` — register with a URI pointing to the agent document
- \`register(metadataKeys[], metadataValues[])\` — register with inline key-value metadata

**Proof-of-Human Registration:**
- \`registerWithHumanProof()\` — ZK passport verification via Self Hub V2 async callback
- \`requireHumanProof\` flag (default: true) — when enabled, the 3 base overloads revert with \`ProofRequired()\` unless the flag is disabled by governance
- This ensures agents are human-backed by default

**Agent URI and Metadata:**
- \`agentURI\` storage with \`Registered\` and \`URIUpdated\` events
- Key-value metadata store: \`getMetadata(agentId, key)\`, \`setMetadata(agentId, key, value)\`
- \`MetadataSet\` event emitted on metadata changes

**EIP-712 Agent Wallet:**
- \`setAgentWallet(agentId, wallet)\` — bind an operational wallet to the agent
- \`getAgentWallet(agentId)\` — retrieve the bound wallet
- \`unsetAgentWallet(agentId)\` — remove the binding

**ERC-165:**
- \`supportsInterface()\` — reports support for ERC-721, ERC-8004, and IERC8004ProofOfHuman

**Proof Expiry System:**
- \`proofExpiresAt(agentId)\` — returns the expiry timestamp, calculated as min(passport_expiry, registration_time + maxProofAge)
- \`isProofFresh(agentId)\` — returns true only if the proof exists AND has not expired
- \`maxProofAge\` — default 365 days, configurable by governance
- \`maxAgentsPerHuman\` — default 1, limits how many agents a single human can register
- No keeper or oracle needed — expiry is based on block.timestamp comparison
- Expired proof means \`hasHumanProof()\` returns false, but the soulbound NFT remains as a historical record

### SelfReputationRegistry

Full ERC-8004 Reputation Registry, scoped to SelfAgentRegistry.

- Auto proof-of-human feedback at registration time (value=100, tag1="proof-of-human")
- \`giveFeedback(agentId, value, tag1, tag2, comment)\`
- \`revokeFeedback(feedbackId)\`
- \`appendResponse(feedbackId, response)\`
- \`getSummary(agentId)\` — aggregated reputation summary

Note: This is a separate registry from the canonical ERC-8004 one because \`giveFeedback()\` reverts for agentIds that do not exist in the associated identity registry. SelfReputationRegistry is scoped to agents registered in SelfAgentRegistry.

### SelfValidationRegistry

Full ERC-8004 Validation Registry, scoped to SelfAgentRegistry.

- \`submitFreshnessValidation(agentId)\` — built-in freshness checker using day buckets
- \`getFreshnessHistory(agentId)\` — historical freshness records for off-chain polling
- \`getLatestFreshness(agentId)\` — most recent freshness check result
- External validator request/response pattern for third-party validation

### Agent Registry Addresses

| Network | Chain ID | Address |
|---------|----------|---------|
| Celo Mainnet | 42220 | \`0x60651482a3033A72128f874623Fc790061cc46D4\` |
| Celo Sepolia Testnet | 11142220 | \`0x29d941856134b1D053AfFF57fa560324510C79fa\` |

### TypeScript SDK (@selfxyz/agent-sdk)

**VerifyResult — Discriminated Union:**
- \`{ verified: true, agentId, expiresAt }\` — agent is registered and proof is fresh
- \`{ verified: false, reason: 'NOT_REGISTERED' }\` — agent has no registration
- \`{ verified: false, reason: 'NO_HUMAN_PROOF' }\` — registered but no proof-of-human
- \`{ verified: false, reason: 'PROOF_EXPIRED', expiredAt, reauthUrl }\` — proof has expired, includes URL for re-authentication

**Utility Functions:**
- \`isProofExpiringSoon(expiresAt, threshold?)\` — returns true if proof expires within the threshold (default 30 days)
- \`generateRegistrationJSON()\` — synchronous builder for agent registration documents
- \`buildAgentCard(agentId)\` — fetches on-chain data to construct a full agent card

**SelfAgentVerifier:**
- Chainable configuration: \`.requireAge(18)\`, \`.requireOFAC()\`, \`.requireNationality("USA")\`
- Verifies agent registration and proof-of-human status

### Dual-Protocol Agent Document

The \`agentURI\` can point to a document that is simultaneously valid as both an ERC-8004 registration file and an A2A (Agent-to-Agent) Agent Card.

**Required ERC-8004 fields:**
- \`type\` — document type identifier
- \`name\` — agent display name
- \`description\` — agent description
- \`image\` — agent avatar/icon URL
- \`services\` — list of services the agent provides

**Optional A2A Agent Card fields:**
- \`version\` — A2A protocol version
- \`url\` — agent endpoint URL
- \`provider\` — provider information
- \`capabilities\` — agent capabilities declaration
- \`securitySchemes\` — authentication schemes

**Self Protocol Extension (\`selfProtocol\` block):**
- \`agentId\` — on-chain agent token ID
- \`registry\` — SelfAgentRegistry contract address
- \`chainId\` — chain ID (42220 for mainnet, 11142220 for testnet)
- \`proofProvider\` — proof provider contract address
- \`verificationStrength\` — numeric strength value (100 for Self passport verification)
- \`trustModel\` — trust model description
- \`credentials\` — verified credential claims

This dual-protocol format enables agents to be discoverable and verifiable in both the ERC-8004 ecosystem and the A2A agent communication protocol simultaneously.
`;
export function registerCrossReference(server, config) {
    server.resource("cross-reference", "self://cross-reference", async (uri) => ({
        contents: [
            {
                uri: uri.href,
                mimeType: "text/plain",
                text: CONTENT,
            },
        ],
    }));
}
//# sourceMappingURL=cross-reference.js.map