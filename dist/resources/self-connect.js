const SELF_CONNECT = `# Self Connect — Identifier-to-Address Mapping Protocol

## Overview

Self Connect is an open-source protocol that maps off-chain personal identifiers (phone numbers, emails, Twitter handles, GitHub usernames) to on-chain blockchain addresses on Celo. It enables users to discover and transact with each other using familiar identifiers instead of hex wallet addresses.

Self Connect uses a **federated attestation model** — anyone can become an issuer who verifies identifiers and registers mappings on-chain. Applications choose which issuers to trust. Privacy is preserved through ODIS (Oblivious Decentralized Identifier Service), which uses threshold cryptography to obfuscate identifiers before on-chain storage.

Self Connect drives the majority of Self protocol's user base, primarily through MiniPay integration enabling phone-number-based cryptocurrency payments on Celo.

**Origin:** Self Connect evolved from Celo's SocialConnect protocol (formerly ASv2). The original implementation is at \`celo-org/SocialConnect\` on GitHub.

## Architecture

\`\`\`
User/Client → ODIS (Privacy) + Issuer (Verification) → FederatedAttestations Smart Contract
\`\`\`

### Three Core Components

1. **FederatedAttestations Smart Contract** — On-chain registry storing obfuscated identifier → address mappings. Issuers register attestations; applications look them up.
2. **ODIS (Oblivious Decentralized Identifier Service)** — Privacy layer using threshold cryptography. Implements a rate-limited Oblivious Pseudorandom Function (OPRF) to generate "peppers" for identifier obfuscation. No single party can reverse the obfuscation.
3. **Issuers** — Independent entities that verify identifier ownership (via SMS, OAuth, email, etc.) and register attestation mappings on-chain. Permissionless — anyone can become an issuer.

## Identifier Types & Prefixes

| Prefix | Type | Example |
|--------|------|---------|
| \`PHONE_NUMBER\` | Phone numbers | \`+12345678901\` |
| \`email://\` | Email addresses | \`alice@example.com\` |
| \`twitter://\` | Twitter handles | \`@alice\` |
| \`github://\` | GitHub usernames | \`alicecodes\` |

Custom identifier types are supported — any string prefix can be used.

## How Identifier Obfuscation Works

Identifiers are obfuscated before on-chain storage to prevent reverse-engineering:

1. **Format:** Combine prefix with plaintext: \`"PHONE_NUMBER://+12345678901"\`
2. **Hash:** \`hashedIdentifier = sha3(formatted)\`
3. **Blind:** Client blinds the hash so ODIS cannot see the plaintext
4. **Query ODIS:** Send blinded hash to ODIS operators (threshold k-of-m scheme)
5. **Combine Signatures:** k operators return partial signatures; client combines them
6. **Unblind:** Client unblinds the combined signature
7. **Generate Pepper:** \`pepper = sha256(unblindedSignature)[0:13]\`
8. **Create Obfuscated ID:** \`sha3(hashedIdentifier + "__" + pepper)\`

**Security Properties:**
- Requires k of m ODIS operators to cooperate — no single operator can compute the pepper
- Rate-limited to prevent mass scraping and rainbow table attacks
- Deterministic — same identifier always produces the same obfuscated form

## ODIS Details

- **Threshold Cryptography:** (k, m) scheme — e.g., 5-of-7 operators required
- **Oblivious:** ODIS operators process blinded requests; they never see the plaintext identifier
- **Rate-Limited:** Quota prevents mass scraping. 10 cUSD = 10,000 queries (~0.001 cUSD/query)
- **Key Rotation:** Supported without disrupting existing attestations
- **Availability:** Can tolerate (m - k) operators being offline

## Registration Flow

1. User requests verification from issuer, provides identifier and wallet address
2. Issuer verifies ownership (SMS for phone, OAuth for Twitter, email link, etc.)
3. Issuer queries ODIS for pepper (consuming ODIS quota)
4. Issuer computes obfuscated identifier
5. Issuer calls \`registerAttestationAsIssuer()\` on the FederatedAttestations contract
6. Gas can be paid by issuer or user
7. User receives confirmation

## Lookup Flow

1. Application queries ODIS for pepper (consuming quota)
2. Application computes obfuscated identifier locally
3. Application calls \`lookupAttestations()\` on FederatedAttestations contract
4. Application specifies which issuers to trust
5. Contract returns: attestation counts, account addresses, signer addresses, issued timestamps

**Lookups are free** — no gas required (view function), only ODIS quota.

## Contract Interface

\`\`\`solidity
// Register an attestation as an issuer
function registerAttestationAsIssuer(
    bytes32 identifier,      // obfuscated identifier
    address account,         // user's wallet address
    uint64 issuedOn          // verification timestamp
) external

// Lookup attestations for an identifier
function lookupAttestations(
    bytes32 identifier,           // obfuscated identifier
    address[] calldata trustedIssuers  // issuers to query
) external view returns (
    uint256[] memory countsPerIssuer,
    address[] memory accounts,
    address[] memory signers,
    uint64[] memory issuedOns,
    uint64[] memory publishedOns
)
\`\`\`

## Contract Addresses

| Contract | Network | Address |
|----------|---------|---------|
| FederatedAttestations | Celo Mainnet | \`0x0aD5b1d0C25ecF6266Dd951403723B2687d6aff2\` |
| FederatedAttestations | Alfajores Testnet | \`0x70F9314aF173c246669cFb0EEe79F9Cfd9C34ee3\` |
| ODIS Payments | Alfajores Testnet | \`0x645170cdB6B5c1bc80847bb728dBa56C50a20a49\` |
| Stable Token (cUSD) | Alfajores Testnet | \`0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1\` |

## Active Issuers

| Issuer | Address | Network |
|--------|---------|---------|
| Kaala | \`0x6549aF2688e07907C1b821cA44d6d65872737f05\` | Mainnet |
| Libera | \`0x388612590F8cC6577F19c9b61811475Aa432CB44\` | Mainnet |
| Libera | \`0xe3475047EF9F9231CD6fAe02B3cBc5148E8eB2c8\` | Alfajores Testnet |

## SDK & Integration

### Required Packages

\`\`\`bash
npm install @celo/identity @celo/abis viem
\`\`\`

**Why Viem (not Web3.js/Ethers):** Modern, type-safe, lightweight, modular, actively maintained, native EIP-1193 support. ContractKit is deprecated.

### Authentication Methods

Issuers authenticate with ODIS using one of:
- **Wallet Key Authentication** — Direct wallet signing
- **Encryption Key (DEK) Authentication** — Derived encryption key

### Integration Example

\`\`\`typescript
import { OdisUtils } from '@celo/identity';
import { createPublicClient, createWalletClient, http } from 'viem';
import { celo } from 'viem/chains';

// 1. Set up ODIS service context
const serviceContext = OdisUtils.Query.getServiceContext(
  OdisContextName.MAINNET  // or ALFAJORES for testnet
);

// 2. Check ODIS quota
const { remainingQuota } = await OdisUtils.Quota.getPnpQuotaStatus(
  issuerAddress, authSigner, serviceContext
);

// 3. Get obfuscated identifier
const { obfuscatedIdentifier } = await OdisUtils.Identifier.getObfuscatedIdentifier(
  '+12345678901',           // plaintext identifier
  OdisUtils.Identifier.IdentifierPrefix.PHONE_NUMBER,
  issuerAddress,
  authSigner,
  serviceContext
);

// 4. Register attestation on-chain
await federatedAttestationsContract.write.registerAttestationAsIssuer([
  obfuscatedIdentifier,
  userAccountAddress,
  BigInt(Math.floor(Date.now() / 1000))  // verification timestamp
]);

// 5. Lookup attestations (from application side)
const attestations = await federatedAttestationsContract.read.lookupAttestations([
  obfuscatedIdentifier,
  [kaalaAddress, liberaAddress]  // trusted issuers
]);
\`\`\`

## Trust Model

Applications choose their trust model based on requirements:

| Model | Approach | Trade-off |
|-------|----------|-----------|
| **Single Issuer** | Trust one issuer | Maximum control, limited to issuer's user base |
| **Multiple Issuers** | Trust several issuers | Broader coverage, must evaluate each issuer's quality |
| **Consensus** | Require attestations from multiple issuers | Highest confidence, reduced coverage |

## Key Use Cases

1. **Phone-Number Payments (MiniPay)** — Send crypto to a phone number without knowing wallet addresses. Primary driver of adoption.
2. **Social Discovery** — Find blockchain accounts by Twitter handle or other identifiers
3. **Cross-Wallet Interoperability** — Different wallet apps discovering and transacting with each other
4. **Contact List Integration** — Import phone contacts and discover which have crypto wallets

## Reference Repositories

- \`celo-org/SocialConnect\` — Original protocol implementation and documentation
- \`celo-org/social-connect-examples\` — Example integrations (Next.js, React Native, Twitter, MiniPay)

## Security Considerations

- **Privacy:** Requires k ODIS operators to remain honest. Rate limiting prevents mass scraping.
- **Sybil Resistance:** User verification requirements + ODIS quota costs + unique identifiers
- **Best Practices:** Select issuers carefully, validate results, handle multi-issuer conflicts, monitor ODIS quota usage
`;
export function registerSelfConnect(server, config) {
    server.resource("self-connect", "self://connect", async (uri) => ({
        contents: [
            {
                uri: uri.href,
                mimeType: "text/plain",
                text: SELF_CONNECT,
            },
        ],
    }));
}
//# sourceMappingURL=self-connect.js.map