import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

export function registerPrompts(server: McpServer): void {
  server.prompt(
    "self_integrate_sdk",
    "Step-by-step guide to adding Self identity verification to your app",
    {
      platform: z
        .enum(["react-native", "web", "kotlin", "server"])
        .describe("Target platform"),
      framework: z
        .string()
        .optional()
        .describe("Web framework (express, fastapi, hono, etc.)"),
    },
    async ({ platform, framework }) => {
      const guides: Record<string, string> = {
        "react-native": `# Integrating Self Verification — React Native

## 1. Install packages
\`\`\`bash
npm install @selfxyz/rn-sdk react-native-webview react-native-nfc-manager react-native-keychain react-native-biometrics
cd ios && pod install
\`\`\`

## 2. Configure the verification request
\`\`\`typescript
import { SelfAppBuilder } from '@selfxyz/common';

const selfApp = new SelfAppBuilder({
  appName: 'My App',
  scope: 'my-app-scope',
  endpoint: 'https://my-app.com/api/verify',
  userId: crypto.randomUUID(),
  endpointType: 'https',
  disclosures: {
    nationality: true,
    minimumAge: 18,
    ofac: true,
  },
}).build();
\`\`\`

## 3. Add the SelfVerification component
\`\`\`tsx
import { SelfVerification } from '@selfxyz/rn-sdk';

<SelfVerification
  selfApp={selfApp}
  onSuccess={(result) => {
    console.log('Verified:', result.userId);
    // result.claims contains disclosed attributes
  }}
  onFailure={(error) => console.error(error)}
/>
\`\`\`

## 4. Set up your backend webhook
Your endpoint receives the proof and verifies it using @selfxyz/core (see self_verify_proof_backend prompt).

## 5. Test with devMode
Set \`devMode: true\` in SelfAppBuilder to use testnet and mock passports.
The app connects to Celo Sepolia (chain 11142220) instead of mainnet.`,

        web: `# Integrating Self Verification — Web

## 1. Install packages
\`\`\`bash
npm install @selfxyz/mobile-sdk-alpha @selfxyz/common
\`\`\`

## 2. Configure verification request
\`\`\`typescript
import { SelfAppBuilder } from '@selfxyz/common';
import { getUniversalLink } from '@selfxyz/common';

const selfApp = new SelfAppBuilder({
  appName: 'My Web App',
  scope: 'my-web-scope',
  endpoint: 'https://my-app.com/api/verify',
  userId: crypto.randomUUID(),
  endpointType: 'https',
  disclosures: { nationality: true, minimumAge: 18 },
}).build();

// Generate deep link for Self app
const link = getUniversalLink(selfApp);
// Display as QR code or redirect
\`\`\`

## 3. Use browser adapters for WebView mode
\`\`\`typescript
import { createIndexedDBDocumentsAdapter, createWebCryptoAdapter } from '@selfxyz/mobile-sdk-alpha/browser';
\`\`\`

## 4. Handle verification callback on your server
Use @selfxyz/core SelfBackendVerifier (see self_verify_proof_backend prompt).`,

        kotlin: `# Integrating Self Verification — Kotlin (KMP)

## 1. Add Gradle dependency
\`\`\`kotlin
// build.gradle.kts
dependencies {
    implementation("xyz.self.sdk:kmp-sdk:0.0.1-alpha")
}
\`\`\`

## 2. Configure and launch
\`\`\`kotlin
val config = SelfSdkConfig(
    endpoint = "https://api.self.xyz",
    debug = false
)

val request = VerificationRequest(
    userId = UUID.randomUUID().toString(),
    disclosures = listOf("nationality", "minimumAge:18")
)

val sdk = SelfSdk.configure(config)
sdk.launch(request, object : SelfSdkCallback {
    override fun onSuccess(result: VerificationResult) {
        // result.claims contains disclosed attributes
    }
    override fun onFailure(error: SelfSdkError) {
        Log.e("Self", error.message)
    }
    override fun onCancelled() { }
})
\`\`\`

## 3. Bridge handlers
The KMP SDK uses the same WebView bridge protocol as the React Native SDK.
5 native handlers: NFC, Camera, Biometrics, Keychain, Lifecycle.
Android is fully implemented; iOS is in progress.`,

        server: `# Integrating Self Verification — Server-Side

## 1. Install
\`\`\`bash
npm install @selfxyz/core @selfxyz/common
\`\`\`

## 2. Set up SelfBackendVerifier
\`\`\`typescript
import { SelfBackendVerifier, ATTESTATION_ID } from '@selfxyz/core';

const allowedIds = new Map([
  [1, true],  // E_PASSPORT
  [2, true],  // EU_ID_CARD
]);

const verifier = new SelfBackendVerifier(
  'my-scope',
  'https://my-app.com/verify',
  false,  // false = mainnet, true = testnet
  allowedIds,
  myConfigStorage,  // implements IConfigStorage
  'uuid'
);
\`\`\`

## 3. Handle webhook${framework ? ` (${framework})` : ""}
\`\`\`typescript
// Your POST /api/verify endpoint
const { attestationId, proof, pubSignals, userContextData } = req.body;
const result = await verifier.verify(attestationId, proof, pubSignals, userContextData);

if (result.isValidDetails.isValid) {
  const { discloseOutput } = result;
  // discloseOutput.nationality, discloseOutput.minimumAge, etc.
}
\`\`\`

## 4. IConfigStorage implementation
\`\`\`typescript
interface IConfigStorage {
  getActionId(userIdentifier: string, userDefinedData: string): Promise<string | null>;
  getConfig(configId: string): Promise<VerificationConfig | null>;
}
\`\`\`

Store verification configs keyed by configId. The SDK calls getActionId to map user+data to a config, then getConfig to retrieve it.`,
      };

      return {
        messages: [
          {
            role: "user" as const,
            content: {
              type: "text" as const,
              text: guides[platform] ?? `No guide available for platform: ${platform}`,
            },
          },
        ],
      };
    }
  );

  server.prompt(
    "self_deploy_verifier",
    "Guide to building and deploying a custom SelfVerificationRoot contract on Celo",
    {
      features: z
        .string()
        .optional()
        .describe(
          "Comma-separated features: age_check, ofac, nationality, birthday, token_gate"
        ),
    },
    async ({ features }) => {
      const featureList = features?.split(",").map((f) => f.trim()) ?? [];
      const hasAge = featureList.includes("age_check");
      const hasOfac = featureList.includes("ofac");

      const guide = `# Deploying a Custom Self Verifier Contract

## 1. Set up your Solidity project
\`\`\`bash
forge init my-verifier && cd my-verifier
forge install selfxyz/self --no-commit
\`\`\`

## 2. Create your contract
\`\`\`solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {SelfVerificationRoot} from "self/abstract/SelfVerificationRoot.sol";
import {ISelfVerificationRoot} from "self/interfaces/ISelfVerificationRoot.sol";
import {AttestationId} from "self/constants/AttestationId.sol";

contract MyVerifier is SelfVerificationRoot {
    bytes32 public verificationConfigId;
    mapping(uint256 => bool) public nullifierUsed;

    constructor(
        address hub,
        string memory scopeSeed,
        bytes32 _configId
    ) SelfVerificationRoot(hub, scopeSeed) {
        verificationConfigId = _configId;
    }

    function getConfigId(
        bytes32, bytes32, bytes memory
    ) public view override returns (bytes32) {
        return verificationConfigId;
    }

    function customVerificationHook(
        ISelfVerificationRoot.GenericDiscloseOutputV2 memory output,
        bytes memory userData
    ) internal override {
        // Prevent double-use
        require(!nullifierUsed[output.nullifier], "Already used");
        nullifierUsed[output.nullifier] = true;

        // Extract recipient
        address recipient = address(uint160(output.userIdentifier));
${hasAge ? `
        // Age check
        require(output.olderThan >= 18, "Must be 18+");` : ""}
${hasOfac ? `
        // OFAC check (any of the 3 variants)
        require(
            output.ofac[0] || output.ofac[1] || output.ofac[2],
            "OFAC screening required"
        );` : ""}

        // Your business logic here
        // e.g., mint NFT, transfer tokens, grant access
    }
}
\`\`\`

## 3. Set up verification config
Before deploying, create a VerificationConfigV2 on the hub:
\`\`\`solidity
SelfStructs.VerificationConfigV2 memory config = SelfStructs.VerificationConfigV2({
    // ... your config params
});
bytes32 configId = hub.setVerificationConfigV2(config);
\`\`\`

## 4. Deploy to Celo
\`\`\`bash
# Use Alchemy RPC for reliability
export CELO_RPC_URL="https://celo-mainnet.g.alchemy.com/v2/YOUR_KEY"

forge create MyVerifier \\
  --rpc-url $CELO_RPC_URL \\
  --constructor-args \\
    0xe57F4773bd9c9d8b6Cd70431117d353298B9f5BF \\  # Hub (mainnet)
    "my-unique-scope" \\
    <your-config-id>
\`\`\`

## 5. Test on Celo Sepolia first
Use testnet hub: \`0x16ECBA51e18a4a7e61fdC417f0d47AFEeDfbed74\`

## Key Gotchas
- Use explicit \`{ gasLimit: 200000 }\` for proxy calls (stale ERC1967 storage)
- Use Alchemy RPC for deployments (drpc.org unreliable for confirmations)
- PoseidonT3 mainnet: \`0xF134707a4C4a3a76b8410fC0294d620A7c341581\`

## AttestationId Constants
- E_PASSPORT = bytes32(1)
- EU_ID_CARD = bytes32(2)
- AADHAAR = bytes32(3)
- KYC = bytes32(4)`;

      return {
        messages: [
          {
            role: "user" as const,
            content: { type: "text" as const, text: guide },
          },
        ],
      };
    }
  );

  server.prompt(
    "self_verify_proof_backend",
    "Guide to setting up server-side proof verification with @selfxyz/core",
    {
      framework: z
        .string()
        .optional()
        .describe("Web framework (express, fastapi, hono, nextjs)"),
    },
    async ({ framework }) => {
      const fw = framework ?? "express";

      const frameworkExamples: Record<string, string> = {
        express: `## Express.js Handler
\`\`\`typescript
import express from 'express';
import { SelfBackendVerifier } from '@selfxyz/core';

const app = express();
app.use(express.json());

const verifier = new SelfBackendVerifier(
  'my-scope', 'https://my-app.com/verify', false,
  new Map([[1, true], [2, true]]),
  myConfigStorage, 'uuid'
);

app.post('/api/verify', async (req, res) => {
  try {
    const { attestationId, proof, pubSignals, userContextData } = req.body;
    const result = await verifier.verify(attestationId, proof, pubSignals, userContextData);

    if (result.isValidDetails.isValid) {
      res.json({
        success: true,
        nationality: result.discloseOutput.nationality,
        ageVerified: result.isValidDetails.isMinimumAgeValid,
        userId: result.userData.userIdentifier,
      });
    } else {
      res.status(400).json({ success: false, details: result.isValidDetails });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
\`\`\``,
        hono: `## Hono Handler
\`\`\`typescript
import { Hono } from 'hono';
import { SelfBackendVerifier } from '@selfxyz/core';

const app = new Hono();

const verifier = new SelfBackendVerifier(
  'my-scope', 'https://my-app.com/verify', false,
  new Map([[1, true], [2, true]]),
  myConfigStorage, 'uuid'
);

app.post('/api/verify', async (c) => {
  const { attestationId, proof, pubSignals, userContextData } = await c.req.json();
  const result = await verifier.verify(attestationId, proof, pubSignals, userContextData);

  if (result.isValidDetails.isValid) {
    return c.json({ success: true, data: result.discloseOutput });
  }
  return c.json({ success: false }, 400);
});
\`\`\``,
        nextjs: `## Next.js API Route
\`\`\`typescript
// app/api/verify/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { SelfBackendVerifier } from '@selfxyz/core';

const verifier = new SelfBackendVerifier(
  'my-scope', 'https://my-app.com/verify', false,
  new Map([[1, true], [2, true]]),
  myConfigStorage, 'uuid'
);

export async function POST(req: NextRequest) {
  const { attestationId, proof, pubSignals, userContextData } = await req.json();
  const result = await verifier.verify(attestationId, proof, pubSignals, userContextData);

  if (result.isValidDetails.isValid) {
    return NextResponse.json({ success: true, data: result.discloseOutput });
  }
  return NextResponse.json({ success: false }, { status: 400 });
}
\`\`\``,
      };

      const example = frameworkExamples[fw] ?? frameworkExamples.express;

      const guide = `# Server-Side Proof Verification with @selfxyz/core

## Install
\`\`\`bash
npm install @selfxyz/core @selfxyz/common
\`\`\`

## Core Concepts

The \`SelfBackendVerifier\` validates ZK proofs submitted by users after they scan
their passport/ID in the Self app. It checks:

1. The proof is for an allowed document type (passport, ID card, etc.)
2. The scope and user context match your configuration
3. The merkle root exists in the on-chain registry (Celo)
4. The Groth16 proof verifies against the on-chain circuit verifier
5. Age, OFAC, and country restrictions match your config
6. The proof timestamp is within 24 hours

## IConfigStorage

You must implement this interface to store/retrieve verification configs:

\`\`\`typescript
interface IConfigStorage {
  getActionId(userIdentifier: string, userDefinedData: string): Promise<string | null>;
  getConfig(configId: string): Promise<VerificationConfig | null>;
}

interface VerificationConfig {
  minimumAge?: number;          // e.g., 18
  ofac?: boolean;               // require OFAC screening
  excludedCountries?: string[]; // ISO alpha-3 codes to block
}
\`\`\`

## VerificationResult

\`\`\`typescript
{
  attestationId: number,
  isValidDetails: {
    isValid: boolean,        // overall validity
    isMinimumAgeValid: boolean,
    isOfacValid: boolean,
  },
  forbiddenCountriesList: string[],
  discloseOutput: {
    issuingState: string,
    name: string,
    idNumber: string,
    nationality: string,
    dateOfBirth: string,
    gender: string,
    expiryDate: string,
    minimumAge: string,
    ofac: boolean[],
  },
  userData: {
    userIdentifier: string,
    userDefinedData: string,
  },
}
\`\`\`

## Error Handling

\`\`\`typescript
import { ConfigMismatchError, RegistryContractError } from '@selfxyz/core';

try {
  const result = await verifier.verify(...);
} catch (error) {
  if (error instanceof ConfigMismatchError) {
    // error.issues contains array of { type: ConfigMismatch, message: string }
    // Types: InvalidId, InvalidScope, InvalidRoot, InvalidTimestamp, etc.
  } else if (error instanceof RegistryContractError) {
    // On-chain registry not found or unreachable
  }
}
\`\`\`

${example}

## Hub Addresses
- Mainnet: \`0xe57F4773bd9c9d8b6Cd70431117d353298B9f5BF\` (Celo 42220)
- Testnet: \`0x16ECBA51e18a4a7e61fdC417f0d47AFEeDfbed74\` (Celo Sepolia 11142220)

Set \`mockPassport: true\` in the constructor to use testnet.`;

      return {
        messages: [
          {
            role: "user" as const,
            content: { type: "text" as const, text: guide },
          },
        ],
      };
    }
  );
}
