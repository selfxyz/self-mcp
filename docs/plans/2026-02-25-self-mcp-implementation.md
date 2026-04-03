# Self Protocol MCP Server — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a comprehensive MCP server that provides AI assistants with deep knowledge of the Self Protocol ecosystem for helping developers integrate Self verification.

**Architecture:** Layered MCP server with 12 resources (knowledge by domain), 3 tools (on-chain queries), and 3 prompts (guided workflows). Same tech stack as self-agent-id-mcp for consistency.

**Tech Stack:** TypeScript 5.7, @modelcontextprotocol/sdk 1.26.0, ethers 6.x, zod 3.x, vitest 3.x

---

## Task 1: Project Scaffolding

**Files:**
- Create: `package.json`
- Create: `tsconfig.json`
- Create: `.gitignore`
- Create: `src/index.ts`
- Create: `src/server.ts`
- Create: `src/config.ts`

**Step 1: Initialize git repo**

```bash
cd ~/Documents/self-mcp
git init
```

**Step 2: Create package.json**

```json
{
  "name": "@selfxyz/self-mcp",
  "version": "0.1.0",
  "description": "MCP server for Self Protocol — identity verification SDK, contracts, and integration guidance",
  "type": "module",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "bin": {
    "self-mcp": "dist/index.js"
  },
  "files": ["dist", "README.md"],
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "start": "node dist/index.js",
    "test": "vitest run",
    "test:watch": "vitest",
    "lint": "tsc --noEmit",
    "prepublishOnly": "npm run build"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.26.0",
    "ethers": "^6.16.0",
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "typescript": "^5.7.0",
    "vitest": "^3.0.0"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/selfxyz/self-mcp.git"
  },
  "author": "Self Protocol",
  "keywords": [
    "mcp", "self-protocol", "identity-verification", "zk-proofs",
    "passport", "model-context-protocol", "claude", "cursor", "celo"
  ]
}
```

**Step 3: Create tsconfig.json**

Use identical config to self-agent-id-mcp:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

**Step 4: Create .gitignore**

```
node_modules/
dist/
*.tgz
.env
```

**Step 5: Create src/config.ts**

```typescript
export interface ServerConfig {
  network: "mainnet" | "testnet";
  rpcUrl: string;
}

const NETWORKS = {
  mainnet: {
    rpcUrl: "https://forno.celo.org",
  },
  testnet: {
    rpcUrl: "https://forno.celo-sepolia.celo-testnet.org",
  },
} as const;

export function loadConfig(): ServerConfig {
  const network = (process.env.SELF_NETWORK ?? "mainnet") as "mainnet" | "testnet";
  const rpcUrl = process.env.SELF_RPC_URL ?? NETWORKS[network].rpcUrl;
  return { network, rpcUrl };
}
```

**Step 6: Create src/server.ts**

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { loadConfig } from "./config.js";
import type { ServerConfig } from "./config.js";

export function createServer(): { server: McpServer; config: ServerConfig } {
  const config = loadConfig();

  const server = new McpServer(
    { name: "self-protocol", version: "0.1.0" },
    { capabilities: { logging: {} } }
  );

  // Resources, tools, and prompts registered in subsequent tasks

  return { server, config };
}
```

**Step 7: Create src/index.ts**

```typescript
#!/usr/bin/env node
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createServer } from "./server.js";

const { server } = createServer();
const transport = new StdioServerTransport();
await server.connect(transport);
```

**Step 8: Install dependencies and verify build**

```bash
cd ~/Documents/self-mcp && npm install && npm run build
```

**Step 9: Commit**

Stage files and suggest commit: `feat: scaffold self-mcp project with config, server, and entry point`

---

## Task 2: Resource — Protocol Overview

**Files:**
- Create: `src/resources/overview.ts`
- Create: `src/resources/index.ts`
- Modify: `src/server.ts` (import and register resources)

**Step 1: Create src/resources/overview.ts**

This resource provides the high-level architecture of Self Protocol. Content should cover:
- What Self is (identity verification using passport NFC + ZK proofs)
- The verification flow: scan document → generate ZK proof → verify on-chain
- Document types: passport (attestationId=1), EU ID card (2), Aadhaar (3), KYC (4)
- Key components: IdentityVerificationHub V2, registries, circuits, SDK packages
- Deployment: Celo mainnet (42220) and Celo Sepolia testnet (11142220)
- Cross-reference to self-agent-id-mcp for AI agent identity (ERC-8004)

Register as resource `self://overview`.

**Step 2: Create src/resources/index.ts**

Export a `registerResources(server, config)` function that registers all resource URIs.

**Step 3: Update src/server.ts to import and call registerResources**

**Step 4: Build and verify**

```bash
npm run build
```

**Step 5: Commit**

Stage and suggest: `feat: add self://overview protocol architecture resource`

---

## Task 3: Resource — Contract Addresses & Info

**Files:**
- Create: `src/resources/contracts.ts`
- Modify: `src/resources/index.ts`

**Step 1: Create src/resources/contracts.ts**

Register `self://contracts` resource containing:

**Mainnet (Celo 42220):**
- IdentityVerificationHub (Proxy): `0xe57F4773bd9c9d8b6Cd70431117d353298B9f5BF`
- IdentityVerificationHubImplV2: `0xa267e58B2d6BA9fc07Af06471423AFb56e4e82B3`
- IdentityRegistry (Passports): `0xd603Fa8C8f4694E8DD1DcE1f27C0C3fc91e32Ac4`
- IdentityRegistryKyc: `0x9cABdeBC3aF136efD69EB881e02118AC612c63b9`
- IdentityRegistryAadhaar: `0x70D543432782D460C96753b52c2aC2797f26924B`
- PoseidonT3: `0xF134707a4C4a3a76b8410fC0294d620A7c341581`
- Verifier_gcp_jwt: `0x87785cC7E9Bc70f87E6F454235214bDEc853C044`
- Security Multisig: `0x738f0bb37FD3b6C4Cdf8eb6FcdFaAA0CA208CB4A` (3/5)
- Operations Multisig: `0x067b18e09A10Fa03d027c1D60A098CEbbE5637f0` (2/5)

**Testnet (Celo Sepolia 11142220):**
- IdentityVerificationHub (Proxy): `0x16ECBA51e18a4a7e61fdC417f0d47AFEeDfbed74`
- IdentityVerificationHubImplV2: `0x48985ec4f71cBC8f387c5C77143110018560c7eD`
- IdentityRegistry: `0x1651ec77c3dC5997eC05f3EE6C2B0b904b516d1d`
- PoseidonT3: `0x0a782f7F9f8Aac6E0bacAF3cD4aA292C3275C6f2`
- IdentityRegistryKyc: `0x90e907E4AaB6e9bcFB94997Af4A097e8CAadBdf3`
- PCR0Manager: `0xf2810D5E9938816D42F0Ae69D33F013a23C0aED2`
- Verifier_gcp_jwt: `0x13ee8CEa15a262D81a245b37889F7b4bEd015f4c`

Also include key interface function signatures for:
- IIdentityVerificationHubV2: `registerCommitment()`, `registerDscKeyCommitment()`, `setVerificationConfigV2()`, `verify()`, `registry()`, `discloseVerifier()`
- IIdentityRegistryV1: `registerCommitment()`, `checkIdentityCommitmentRoot()`, `getIdentityCommitmentMerkleRoot()`, `nullifiers()`, OFAC root getters
- IIdentityRegistryKycV1: `registerCommitment()`, `checkIdentityCommitmentRoot()`, `checkPubkeyCommitment()`, OFAC root getters

**Step 2: Register in resources/index.ts**

**Step 3: Build and verify**

**Step 4: Commit**

Stage and suggest: `feat: add self://contracts resource with addresses and interfaces`

---

## Task 4: Resource — Custom Verifier Guide

**Files:**
- Create: `src/resources/verifier-guide.ts`
- Modify: `src/resources/index.ts`

**Step 1: Create src/resources/verifier-guide.ts**

Register `self://contracts/verifier-guide` with comprehensive guide covering:

1. **SelfVerificationRoot** — abstract base contract developers extend
   - Constructor: `(address hub, string scopeSeed)`
   - Override `getConfigId()` — return verification config ID
   - Override `customVerificationHook()` — business logic
   - Scope auto-calculation via Poseidon hash

2. **GenericDiscloseOutputV2** struct:
   ```
   attestationId, userIdentifier, nullifier, forbiddenCountriesListPacked[4],
   issuingState, name[], idNumber, nationality, dateOfBirth, gender,
   expiryDate, olderThan, ofac[3]
   ```

3. **Integration checklist** (from our research)

4. **HappyBirthday example** — real-world reference showing:
   - Config ID pattern
   - Birthday window check
   - Nullifier double-spend prevention
   - User identifier extraction: `address(uint160(output.userIdentifier))`

5. **AttestationId constants:**
   - E_PASSPORT = 1, EU_ID_CARD = 2, AADHAAR = 3, KYC = 4

6. **Celo-specific gotchas:**
   - Stale ERC1967 storage during gas estimation → explicit `{ gasLimit: 200000 }`
   - OZ Upgrades manifest staleness
   - Use Alchemy for deploy reliability
   - Aadhaar registry initialize bug (call `updateHub()` separately)

**Step 2: Register in resources/index.ts**

**Step 3: Build and verify**

**Step 4: Commit**

Stage and suggest: `feat: add self://contracts/verifier-guide resource with SelfVerificationRoot guide`

---

## Task 5: Resource — SDK Core (Backend Verifier)

**Files:**
- Create: `src/resources/sdk-core.ts`
- Modify: `src/resources/index.ts`

**Step 1: Create src/resources/sdk-core.ts**

Register `self://sdk/core` with documentation for `@selfxyz/core` v1.2.0-beta.1:

- **SelfBackendVerifier** class — server-side proof verification
  - Constructor: `(scope, endpoint, mockPassport, allowedIds, configStorage, userIdentifierType)`
  - `verify(attestationId, proof, pubSignals, userContextData)` — full verification pipeline
  - Checks: attestation ID, scope, merkle root, timestamp, forbidden countries, minimum age
  - Returns: `{ attestationId, isValidDetails, forbiddenCountriesList, discloseOutput, userData }`

- **ATTESTATION_ID** constant

- **Integration pattern:**
  ```typescript
  import { SelfBackendVerifier, ATTESTATION_ID } from '@selfxyz/core';
  const verifier = new SelfBackendVerifier(scope, endpoint, false, allowedIds, configStorage, 'uuid');
  const result = await verifier.verify(attestationId, proof, pubSignals, userContextData);
  ```

- **ConfigStorage interface** — IConfigStorage with `getActionId()` and `getConfig()`

- **Error types:** ConfigMismatchError, RegistryContractError, VerifierContractError

**Step 2: Register in resources/index.ts**

**Step 3: Build and verify**

**Step 4: Commit**

Stage and suggest: `feat: add self://sdk/core resource for SelfBackendVerifier documentation`

---

## Task 6: Resources — Client SDKs (RN, Mobile Alpha, WebView Bridge, KMP)

**Files:**
- Create: `src/resources/sdk-rn.ts`
- Create: `src/resources/sdk-mobile.ts`
- Create: `src/resources/sdk-bridge.ts`
- Create: `src/resources/sdk-kmp.ts`
- Create: `src/resources/sdk-common.ts`
- Modify: `src/resources/index.ts`

**Step 1: Create sdk-rn.ts — `self://sdk/react-native`**

Document `@selfxyz/rn-sdk` v0.0.1-alpha.1:
- `SelfVerification` component — main entry point, wraps WebView
- Props: `SelfVerificationProps` with `VerificationRequest` and callbacks
- `MessageRouter` — bridge message routing
- 5 bridge handlers: Lifecycle, Biometric, Keychain, NFC, Camera
- Peer deps: react-native-webview, react-native-keychain, react-native-nfc-manager, react-native-biometrics
- Bundled webview-app HTML assets

**Step 2: Create sdk-mobile.ts — `self://sdk/mobile-alpha`**

Document `@selfxyz/mobile-sdk-alpha` v0.0.1-alpha.1:
- `createSelfClient()` — main factory
- `SelfClientProvider` / `useSelfClient()` — React context
- Adapters: Crypto, NFC, Documents, Network, Auth
- Browser-specific: `createIndexedDBDocumentsAdapter()`, `createWebCryptoAdapter()`
- Flows: onboarding (document selection → NFC scan → proof generation), disclosing
- Key types: `Adapters`, `Config`, `VerificationRequest`, `SelfClient`

**Step 3: Create sdk-bridge.ts — `self://sdk/webview-bridge`**

Document `@selfxyz/webview-bridge` v0.0.1-alpha.1:
- Bridge Protocol v1
- `WebViewBridge` class
- 10 domains: nfc, biometrics, secureStorage, camera, crypto, haptic, analytics, lifecycle, documents, navigation
- Message types: BridgeRequest, BridgeResponse, BridgeEvent
- Transport: `window.ReactNativeWebView.postMessage()` (RN) or `window.parent.postMessage()` (web)
- Default timeout: 30,000ms

**Step 4: Create sdk-kmp.ts — `self://sdk/kmp`**

Document `@selfxyz/kmp-sdk` v0.0.1-alpha:
- `SelfSdk.configure(config).launch(request, callback)` — Kotlin API
- 5 native handlers: NFC, Camera, Biometrics, Keychain, Lifecycle
- Same bridge protocol as RN SDK
- Gradle-based build: AAR + XCFramework
- Android complete, iOS in progress

**Step 5: Create sdk-common.ts — `self://sdk/common`**

Document `@selfxyz/common` v0.0.9:
- Categories: constants (countries, attestation IDs, URLs), types (PassportData, IDDocument, etc.), utilities (circuit inputs, hashing, MRZ parsing, certificate handling, OFAC trees)
- Key functions: `generateCircuitInputsRegister()`, `generateCircuitInputsVCandDisclose()`, `SelfAppBuilder`, `hashEndpointWithScope()`
- `SelfAppBuilder` — the developer-facing request builder with disclosure config
- `SelfAppDisclosureConfig`: issuing_state, name, passport_number, nationality, date_of_birth, gender, expiry_date, ofac, excludedCountries, minimumAge

**Step 6: Register all in resources/index.ts**

**Step 7: Build and verify**

**Step 8: Commit**

Stage and suggest: `feat: add SDK documentation resources (rn, mobile-alpha, bridge, kmp, common)`

---

## Task 7: Resource — Documents, Countries & Circuits

**Files:**
- Create: `src/resources/documents.ts`
- Create: `src/resources/circuits.ts`
- Modify: `src/resources/index.ts`

**Step 1: Create documents.ts — `self://documents`**

Content:
- 4 document types: E_PASSPORT (1), EU_ID_CARD (2), AADHAAR (3), KYC (4)
- 195 supported countries (ISO 3166-1 alpha-3)
- Disclosure attributes per document type:
  - Passport: issuing_state, name, passport_number, nationality, date_of_birth, gender, expiry_date, older_than, ofac (3 variants)
  - ID card: same attributes, different byte positions
  - Aadhaar: separate field structure
  - KYC: country, idType, idNumber, issuanceDate, expiryDate, fullName, DOB, photoHash, phoneNumber, gender, address
- Revealed data type indices (0-10)
- Max 40 forbidden countries per verification config
- OFAC tree variants: passport-no-nationality, name-dob, name-yob
- Tree URLs: `https://tree.self.xyz/{dsc,csca,identity}` (mainnet), `https://tree.staging.self.xyz/...` (staging)

**Step 2: Create circuits.ts — `self://circuits`**

Content:
- Circuit types: dsc, register, vc_and_disclose
- 52 register circuit variants (hash × signature algorithm combinations)
- 20 DSC circuit variants
- Supported signature algorithms: RSA (2048-4096), ECDSA (secp256r1, secp384r1, secp521r1, brainpool variants), RSA-PSS
- Supported hash functions: SHA1, SHA224, SHA256, SHA384, SHA512
- Proof structure: Groth16 (a[2], b[2][2], c[2], pubSignals)
- Public signals layout per attestation type
- Key constants: COMMITMENT_TREE_DEPTH=33, CSCA_TREE_DEPTH=12, DSC_TREE_DEPTH=21, OFAC_TREE_LEVELS=64

**Step 3: Register in resources/index.ts**

**Step 4: Build and verify**

**Step 5: Commit**

Stage and suggest: `feat: add self://documents and self://circuits knowledge resources`

---

## Task 8: Resource — Cross-Reference

**Files:**
- Create: `src/resources/cross-reference.ts`
- Modify: `src/resources/index.ts`

**Step 1: Create cross-reference.ts — `self://cross-reference`**

Content:
- Explains the two-MCP architecture:
  - `self-protocol` MCP (this one) — developer integration with Self verification
  - `self-agent-id` MCP — AI agent identity lifecycle (ERC-8004)
- When to use each:
  - "How do I verify a user's identity?" → this MCP
  - "How do I register my AI agent?" → self-agent-id-mcp
  - "How do I build a custom verifier contract?" → this MCP
  - "How do I sign requests as an agent?" → self-agent-id-mcp
- Reference: `@selfxyz/agent-sdk` for agent operations, `@selfxyz/core` for proof verification
- Agent registry addresses:
  - Mainnet: `0x60651482a3033A72128f874623Fc790061cc46D4`
  - Testnet: `0x29d941856134b1D053AfFF57fa560324510C79fa`

**Step 2: Register in resources/index.ts**

**Step 3: Build and verify**

**Step 4: Commit**

Stage and suggest: `feat: add self://cross-reference resource linking to self-agent-id-mcp`

---

## Task 9: Tools — On-Chain Queries

**Files:**
- Create: `src/tools/contracts.ts`
- Create: `src/tools/contracts.test.ts`
- Modify: `src/server.ts`

**Step 1: Write failing tests for contract query tools**

Test that tools are registered and handle inputs correctly (mock ethers provider).

**Step 2: Implement src/tools/contracts.ts**

Three tools:

**`self_get_contract_addresses`**
- Input: `{ network: "mainnet" | "testnet" }` (optional, defaults to config)
- Returns: JSON with all deployed contract addresses for that network
- No RPC call needed — static data

**`self_check_verification`**
- Input: `{ attestationId: number, merkleRoot: string, network?: string }`
- Calls `registry(attestationId)` on Hub, then `checkIdentityCommitmentRoot(root)` on registry
- Returns: `{ valid: boolean, registryAddress: string }`

**`self_get_registry_info`**
- Input: `{ attestationId: number, network?: string }`
- Calls registry to get: merkle root, OFAC roots, tree size (where available)
- Returns: JSON with registry state

**Step 3: Run tests to verify they pass**

```bash
npm test
```

**Step 4: Update src/server.ts to register tools**

**Step 5: Build and verify**

**Step 6: Commit**

Stage and suggest: `feat: add on-chain query tools (addresses, verification, registry info)`

---

## Task 10: Prompts — Guided Workflows

**Files:**
- Create: `src/prompts/index.ts`
- Modify: `src/server.ts`

**Step 1: Create src/prompts/index.ts**

Three prompts:

**`self_integrate_sdk`**
- Arguments: `{ platform: "react-native" | "web" | "kotlin" | "server", framework?: string }`
- Returns step-by-step integration guide:
  - Package installation
  - SelfAppBuilder configuration
  - Component/client setup
  - Verification callback handling
  - Testing with devMode/testnet

**`self_deploy_verifier`**
- Arguments: `{ features: string[] }` (e.g., ["age_check", "ofac", "nationality"])
- Returns guide for building a SelfVerificationRoot contract:
  - Inheriting SelfVerificationRoot
  - Setting verification config
  - Implementing customVerificationHook
  - Deploying to Celo
  - Testing with testnet

**`self_verify_proof_backend`**
- Arguments: `{ framework: string }` (e.g., "express", "fastapi", "hono")
- Returns guide for server-side proof verification:
  - Installing @selfxyz/core
  - Setting up SelfBackendVerifier
  - Handling the webhook/callback
  - Validating results

**Step 2: Register in server.ts**

**Step 3: Build and verify**

**Step 4: Commit**

Stage and suggest: `feat: add guided workflow prompts (sdk integration, verifier deployment, backend verification)`

---

## Task 11: Integration Test & README

**Files:**
- Create: `src/integration.test.ts`
- Create: `README.md`

**Step 1: Write integration test**

Test that `createServer()` produces a valid McpServer with all expected resources, tools, and prompts registered.

**Step 2: Run tests**

```bash
npm test
```

**Step 3: Create README.md**

Cover:
- What this MCP does
- Installation (npx, npm, manual)
- Configuration (.mcp.json example)
- Available resources (table with URIs and descriptions)
- Available tools (table)
- Available prompts (table)
- Environment variables (SELF_NETWORK, SELF_RPC_URL)
- Relationship to self-agent-id-mcp
- Links to Self Protocol docs

**Step 4: Build final**

```bash
npm run build && npm test
```

**Step 5: Commit**

Stage and suggest: `feat: add integration tests and README documentation`

---

## Task 12: Utility Helpers

**Files:**
- Create: `src/utils/format.ts`
- Create: `src/utils/errors.ts`
- Create: `src/utils/format.test.ts`
- Create: `src/utils/errors.test.ts`

**Step 1: Create format.ts**

Helper functions for formatting tool/resource responses consistently:
- `formatSuccess(data)` — wrap in success envelope
- `formatError(message)` — wrap in error envelope
- `formatResource(content)` — format resource text content

**Step 2: Create errors.ts**

Error response builders matching the pattern from self-agent-id-mcp.

**Step 3: Write tests for both**

**Step 4: Run tests**

```bash
npm test
```

**Step 5: Commit**

Stage and suggest: `feat: add utility helpers for response formatting`

---

## Execution Order

Tasks 1 → 12 (utility helpers) → 2-8 (resources, can be parallelized) → 9 (tools) → 10 (prompts) → 11 (integration test + README)

Recommended: Task 1, then 12, then 2-8 in parallel batches, then 9-11 sequentially.

---

## Validation

After all tasks complete:

```bash
cd ~/Documents/self-mcp
npm run build    # TypeScript compiles cleanly
npm test         # All tests pass
npm run lint     # No type errors
node dist/index.js  # Server starts without errors (will hang waiting for stdio — Ctrl+C)
```
