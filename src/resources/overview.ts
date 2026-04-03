import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { ServerConfig } from "../config.js";

const OVERVIEW = `# Self Protocol — Overview

## What is Self?

Self is a privacy-preserving identity protocol on the Celo blockchain with three products:

- **Self Pass** — Identity verification using zero-knowledge proofs. Users scan passports, biometric ID cards, Aadhaar, or complete KYC, then prove facts about themselves (age, nationality, sanctions status) to any dApp without revealing personal data.
- **Self Connect** — Identifier-to-address mapping protocol. Maps phone numbers, emails, Twitter handles, and other identifiers to blockchain addresses using a federated attestation model with ODIS for privacy. Drives the majority of Self's user base via MiniPay integration. See \`self://connect\` for full details.
- **Self Agent ID** — On-chain identity registry (ERC-8004) for AI agents to prove they are backed by a real, passport-verified human. See the self-agent-id MCP server.

## Self Pass — Verification Flow

1. **Document Scan** — The user scans their passport or ID card via NFC, Aadhaar via QR/PDF, or completes KYC via Didit. The app extracts document data on-device.
2. **ZK Proof Generation** — The app generates a Groth16 zero-knowledge proof locally on the device inside a TEE. This proof attests to specific claims (e.g. "user is over 18", "user is not on OFAC list") without revealing the raw document data.
3. **On-Chain Verification** — The proof is submitted to the IdentityVerificationHub V2 smart contract on Celo. The hub delegates to the appropriate circuit verifier, validates the proof, and stores a commitment in the relevant identity registry.
4. **Result** — The verifier contract (or off-chain SDK) can now confirm the user's claims. The user's personal data never leaves their device.

## Supported Document Types (Self Pass)

| attestationId | Document Type         |
|---------------|-----------------------|
| 1             | E-Passport            |
| 2             | EU Biometric ID Card  |
| 3             | Aadhaar (India)       |
| 4             | KYC (via Didit)       |

## Key On-Chain Components

- **IdentityVerificationHub V2** — The main entry point for all proof verification. Receives proofs, delegates to the correct circuit verifier, and writes commitments to registries.
- **Identity Registries** — Separate registry contracts per document type (passport, ID card, Aadhaar, KYC). Each stores merkle-tree commitments for verified identities.
- **Circuit Verifiers** — Groth16 verifier contracts for the three main circuits:
  - \`register\` — Proves identity document authenticity and registers a commitment.
  - \`dsc\` — Proves the Document Signing Certificate (DSC) chain of trust.
  - \`vc_and_disclose\` — Proves selective disclosure claims (age, nationality, etc.) against a registered commitment.
- **SelfVerificationRoot** — Abstract base contract that developers inherit to build custom on-chain verifier contracts. Handles proof validation, scope binding, and attestation checks.

## SDK Packages

- **@selfxyz/core** — Server-side verification library. Use this to verify proofs in your backend, configure required disclosures, and interact with on-chain registries.
- **@selfxyz/rn-sdk** — React Native SDK. Provides the \`SelfVerification\` component for integrating passport scanning and proof generation into React Native apps.
- **@selfxyz/mobile-sdk-alpha** — Cross-platform mobile core. Lower-level SDK used by the React Native and native mobile integrations.
- **@selfxyz/webview-bridge** — Bridge protocol for communicating between a host app and Self's verification webview. Handles message passing, session management, and proof delivery.
- **@selfxyz/kmp-sdk** — Kotlin Multiplatform SDK. Enables native Android and iOS integrations from shared Kotlin code.
- **@selfxyz/common** — Shared utilities, types, and constants used across all Self packages.

## Deployment

- **Celo Mainnet** — Chain ID 42220. Production deployment.
- **Celo Sepolia Testnet** — Chain ID 11142220. Test deployment for development and integration testing.

## Disclosure Options

When configuring a verification request, you can require disclosure of any combination of the following fields:

- \`issuing_state\` — The country that issued the document (ISO 3166-1 alpha-3).
- \`name\` — Full name as it appears on the document.
- \`passport_number\` — Document number.
- \`nationality\` — Nationality (ISO 3166-1 alpha-3).
- \`date_of_birth\` — Date of birth.
- \`gender\` — Gender as recorded on the document.
- \`expiry_date\` — Document expiry date.
- \`older_than\` — Age verification threshold (e.g. 18, 21). Proves the user is at least N years old without revealing their exact date of birth.
- \`ofac\` — OFAC sanctions screening. Proves the user is not on the US OFAC sanctions list.

## Related: AI Agent Identity

For AI agent identity registration with proof-of-human verification (ERC-8004), see the self-agent-id MCP server. The SelfAgentRegistry contract uses Self's passport verification as a soulbound proof-of-human mechanism for agent NFTs.
`;

export function registerOverview(
  server: McpServer,
  config: ServerConfig
): void {
  server.resource("protocol-overview", "self://overview", async (uri) => ({
    contents: [
      {
        uri: uri.href,
        mimeType: "text/plain" as const,
        text: OVERVIEW,
      },
    ],
  }));
}
