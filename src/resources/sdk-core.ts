import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { ServerConfig } from "../config.js";

const SDK_CORE = `# @selfxyz/core v1.2.0-beta.1 — Server-Side Proof Verification SDK

## SelfBackendVerifier Class

The main class for verifying Self zero-knowledge proofs on your backend.

\`\`\`typescript
class SelfBackendVerifier {
  constructor(
    scope: string,                              // Unique scope identifier for your app
    endpoint: string,                           // Your verification endpoint URL
    mockPassport: boolean,                      // true = testnet, false = mainnet
    allowedIds: Map<AttestationId, boolean>,     // Which document types to accept
    configStorage: IConfigStorage,              // Storage for verification configs
    userIdentifierType: UserIdType              // 'uuid' | 'hex'
  )

  async verify(
    attestationId: AttestationId,   // 1=passport, 2=ID, 3=aadhaar, 4=kyc
    proof: VcAndDiscloseProof,      // { a: uint256[2], b: uint256[2][2], c: uint256[2] }
    pubSignals: BigNumberish[],     // Public signals from ZK proof
    userContextData: string         // Hex-encoded context data
  ): Promise<VerifyResult>
}
\`\`\`

### VerifyResult

\`\`\`typescript
{
  attestationId: AttestationId;
  isValidDetails: {
    isValid: boolean;
    isMinimumAgeValid: boolean;
    isOfacValid: boolean;
  };
  forbiddenCountriesList: string[];
  discloseOutput: GenericDiscloseOutput;
  userData: {
    userIdentifier: string;
    userDefinedData: string;
  };
}
\`\`\`

## Verification Checks (in order)

The \`verify()\` method performs these checks sequentially. If any check fails, the corresponding ConfigMismatch error is thrown.

1. **Attestation ID is in allowedIds** — The attestationId must be present and set to \`true\` in the allowedIds map.
2. **User context hash matches circuit output** — The hash of the userContextData must match what the ZK circuit produced.
3. **Scope matches** — The scope embedded in the proof's public signals must match the constructor's scope.
4. **Merkle root exists in on-chain registry** — The merkle root from the proof must exist in the on-chain identity registry for the given attestation type.
5. **Attestation ID matches circuit** — The attestation ID in the public signals must match the provided attestationId parameter.
6. **Config ID found in storage** — The config ID derived from the proof must resolve to a VerificationConfig via the IConfigStorage.
7. **Forbidden countries list matches config** — The excluded countries encoded in the proof must match the config's excludedCountries.
8. **Minimum age matches config** — The minimum age encoded in the proof must match the config's minimumAge.
9. **Timestamp within 24 hours** — The proof's timestamp must be within 24 hours of the current time.
10. **On-chain proof verification via Groth16 verifier contract** — The proof (a, b, c) and public signals are verified against the on-chain Groth16 verifier contract.

## GenericDiscloseOutput

Fields returned in the disclose output after successful verification:

\`\`\`typescript
interface GenericDiscloseOutput {
  issuingState: string;    // ISO 3166-1 alpha-3 country code
  name: string;            // Full name from the document
  idNumber: string;        // Document number (passport number, ID number, etc.)
  nationality: string;     // ISO 3166-1 alpha-3 nationality code
  dateOfBirth: string;     // Date of birth
  gender: string;          // Gender as recorded on the document
  expiryDate: string;      // Document expiry date
  minimumAge: string;      // Minimum age threshold proven (e.g. "18")
  ofac: [string, string, string];  // Three OFAC-related fields
}
\`\`\`

## IConfigStorage Interface

You must implement this interface to store and retrieve verification configurations.

\`\`\`typescript
interface IConfigStorage {
  getActionId(
    userIdentifier: string,
    userDefinedData: string
  ): Promise<string | null>;

  getConfig(configId: string): Promise<VerificationConfig | null>;
}
\`\`\`

## VerificationConfig

\`\`\`typescript
interface VerificationConfig {
  minimumAge?: number;          // Minimum age threshold (e.g. 18, 21)
  ofac?: boolean;               // Whether OFAC screening is required
  excludedCountries?: string[]; // ISO 3166-1 alpha-3 codes to reject
}
\`\`\`

## Error Types

### ConfigMismatchError

Thrown when the proof does not match the expected configuration. Contains an array of issues indicating which checks failed.

\`\`\`typescript
class ConfigMismatchError extends Error {
  issues: ConfigMismatch[];
}
\`\`\`

### ConfigMismatch Enum

\`\`\`typescript
enum ConfigMismatch {
  InvalidId,                    // Attestation ID not in allowedIds
  InvalidUserContextHash,       // User context hash mismatch
  InvalidScope,                 // Scope mismatch
  InvalidRoot,                  // Merkle root not found on-chain
  InvalidAttestationId,         // Attestation ID mismatch in circuit
  ConfigNotFound,               // Config ID not found in storage
  InvalidForbiddenCountriesList,// Excluded countries mismatch
  InvalidMinimumAge,            // Minimum age mismatch
  InvalidTimestamp              // Timestamp outside 24-hour window
}
\`\`\`

### RegistryContractError

Thrown when the identity registry contract for the given attestation type cannot be found on-chain.

### VerifierContractError

Thrown when the Groth16 verifier contract cannot be found on-chain.

## Hub Addresses (hardcoded in SDK)

- **Mainnet (Celo 42220):** \`0xe57F4773bd9c9d8b6Cd70431117d353298B9f5BF\`
- **Testnet (Celo Sepolia 11142220):** \`0x16ECBA51e18a4a7e61fdC417f0d47AFEeDfbed74\`

The SDK automatically selects the correct hub address based on the \`mockPassport\` flag:
- \`mockPassport: false\` → Mainnet hub
- \`mockPassport: true\` → Testnet hub

## ATTESTATION_ID Constants

\`\`\`typescript
enum ATTESTATION_ID {
  E_PASSPORT = 1,
  EU_ID_CARD = 2,
  AADHAAR = 3,
  KYC = 4
}
\`\`\`

## Integration Pattern

\`\`\`typescript
import { SelfBackendVerifier, ATTESTATION_ID } from '@selfxyz/core';

// 1. Configure allowed document types
const allowedIds = new Map([
  [ATTESTATION_ID.E_PASSPORT, true],
  [ATTESTATION_ID.EU_ID_CARD, true],
]);

// 2. Create verifier instance
const verifier = new SelfBackendVerifier(
  'my-app-scope',               // Unique scope for your app
  'https://my-app.com/verify',  // Your verification endpoint
  false,                        // false = mainnet, true = testnet
  allowedIds,                   // Accepted document types
  myConfigStorage,              // Your IConfigStorage implementation
  'uuid'                        // User identifier type
);

// 3. In your webhook handler:
const result = await verifier.verify(
  attestationId,    // From the proof payload
  proof,            // { a, b, c } Groth16 proof
  pubSignals,       // Public signals array
  userContextData   // Hex-encoded context
);

if (result.isValidDetails.isValid) {
  // Proof verified — extract user data from result.discloseOutput
  const { name, nationality, dateOfBirth } = result.discloseOutput;
  const { userIdentifier } = result.userData;
}
\`\`\`
`;

export function registerSdkCore(
  server: McpServer,
  config: ServerConfig
): void {
  server.resource("sdk-core", "self://sdk/core", async (uri) => ({
    contents: [
      {
        uri: uri.href,
        mimeType: "text/plain" as const,
        text: SDK_CORE,
      },
    ],
  }));
}
