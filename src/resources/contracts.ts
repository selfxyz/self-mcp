import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { ServerConfig } from "../config.js";

const CONTRACTS_REFERENCE = `# Self Protocol — Deployed Contract Addresses

## Mainnet (Celo — Chain ID 42220)

| Contract | Address |
|---|---|
| IdentityVerificationHub (Proxy) | 0xe57F4773bd9c9d8b6Cd70431117d353298B9f5BF |
| IdentityVerificationHubImplV2 | 0xa267e58B2d6BA9fc07Af06471423AFb56e4e82B3 |
| IdentityRegistry (Passports) | 0xd603Fa8C8f4694E8DD1DcE1f27C0C3fc91e32Ac4 |
| IdentityRegistryKyc | 0x9cABdeBC3aF136efD69EB881e02118AC612c63b9 |
| IdentityRegistryAadhaar | 0x70D543432782D460C96753b52c2aC2797f26924B |
| PoseidonT3 | 0xF134707a4C4a3a76b8410fC0294d620A7c341581 |
| Verifier_gcp_jwt | 0x87785cC7E9Bc70f87E6F454235214bDEc853C044 |
| Security Multisig (3/5) | 0x738f0bb37FD3b6C4Cdf8eb6FcdFaAA0CA208CB4A |
| Operations Multisig (2/5) | 0x067b18e09A10Fa03d027c1D60A098CEbbE5637f0 |

## Testnet (Celo Sepolia — Chain ID 11142220)

| Contract | Address |
|---|---|
| IdentityVerificationHub (Proxy) | 0x16ECBA51e18a4a7e61fdC417f0d47AFEeDfbed74 |
| IdentityVerificationHubImplV2 | 0x48985ec4f71cBC8f387c5C77143110018560c7eD |
| IdentityRegistry | 0x1651ec77c3dC5997eC05f3EE6C2B0b904b516d1d |
| PoseidonT3 | 0x0a782f7F9f8Aac6E0bacAF3cD4aA292C3275C6f2 |
| IdentityRegistryKyc | 0x90e907E4AaB6e9bcFB94997Af4A097e8CAadBdf3 |
| PCR0Manager | 0xf2810D5E9938816D42F0Ae69D33F013a23C0aED2 |
| Verifier_gcp_jwt | 0x13ee8CEa15a262D81a245b37889F7b4bEd015f4c |

---

## Key Interface Function Signatures

### IIdentityVerificationHubV2

- registerCommitment(bytes32 attestationId, uint256 registerCircuitVerifierId, RegisterCircuitProof proof)
- registerDscKeyCommitment(bytes32 attestationId, uint256 dscCircuitVerifierId, DscCircuitProof proof)
- setVerificationConfigV2(VerificationConfigV2 config) → bytes32 configId
- verify(bytes baseVerificationInput, bytes userContextData)
- registry(bytes32 attestationId) → address
- discloseVerifier(bytes32 attestationId) → address

### IIdentityRegistryV1

- registerCommitment(bytes32 attestationId, uint256 nullifier, uint256 commitment)
- checkIdentityCommitmentRoot(uint256 root) → bool
- getIdentityCommitmentMerkleRoot() → uint256
- nullifiers(bytes32 attestationId, uint256 nullifier) → bool
- getPassportNoOfacRoot() → uint256
- getNameAndDobOfacRoot() → uint256
- getNameAndYobOfacRoot() → uint256

### IIdentityRegistryKycV1

- registerCommitment(uint256 nullifier, uint256 commitment)
- checkIdentityCommitmentRoot(uint256 root) → bool
- checkPubkeyCommitment(uint256 pubkeyCommitment) → bool
`;

export function registerContracts(
  server: McpServer,
  _config: ServerConfig,
): void {
  server.resource("contracts", "self://contracts", async (uri) => ({
    contents: [
      { uri: uri.href, mimeType: "text/plain", text: CONTRACTS_REFERENCE },
    ],
  }));
}
