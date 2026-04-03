const SDK_MOBILE = `# @selfxyz/mobile-sdk-alpha v0.0.1-alpha.1 — Cross-Platform Mobile SDK

## Overview

The mobile SDK alpha is the cross-platform core powering Self's mobile integrations. It provides a factory-based architecture with pluggable adapters for crypto, NFC, storage, networking, and more. It uses XState for deterministic flow orchestration and Zustand for state management. With 162+ exports, it covers flows, components, hooks, adapters, and utilities.

## Main API: createSelfClient()

The primary SDK factory function. Returns a \`SelfClient\` instance configured with the provided adapters and config.

\`\`\`typescript
import { createSelfClient } from '@selfxyz/mobile-sdk-alpha';

const client = createSelfClient({
  adapters: { /* adapter implementations */ },
  config: { /* SDK configuration */ },
});
\`\`\`

## React Integration

### SelfClientProvider

React context provider for injecting the SelfClient into the component tree.

\`\`\`typescript
import { SelfClientProvider } from '@selfxyz/mobile-sdk-alpha';

<SelfClientProvider client={client}>
  <App />
</SelfClientProvider>
\`\`\`

### useSelfClient()

React hook to access the SelfClient from context.

\`\`\`typescript
import { useSelfClient } from '@selfxyz/mobile-sdk-alpha';

function MyComponent() {
  const client = useSelfClient();
  // Use client to initiate flows, read state, etc.
}
\`\`\`

## Adapter Interfaces

The SDK uses a pluggable adapter pattern. Each adapter interface defines the contract for a specific native capability:

### CryptoAdapter
Cryptographic operations — signing, key generation, public key retrieval.

### NFCScannerAdapter
NFC chip reading — start scan, cancel scan, check support.

### DocumentsAdapter
Document storage — load catalog, save catalog, load by ID, save, delete.

### NetworkAdapter
Network requests — HTTP calls to the Self backend and other services.

### AuthAdapter
Authentication — biometric prompts, availability checks.

### StorageAdapter
Secure key-value storage — get, set, remove entries.

### LoggerAdapter
Logging — configurable log output for debugging and analytics.

## Browser-Specific Adapters

Pre-built adapters for browser/web environments:

\`\`\`typescript
import {
  createIndexedDBDocumentsAdapter,
  createWebCryptoAdapter,
  createWebAnalyticsAdapter,
  createNoOpHapticAdapter,
} from '@selfxyz/mobile-sdk-alpha';
\`\`\`

- **createIndexedDBDocumentsAdapter()** — Uses IndexedDB for document storage in the browser.
- **createWebCryptoAdapter()** — Uses the Web Crypto API for cryptographic operations.
- **createWebAnalyticsAdapter()** — Browser analytics adapter.
- **createNoOpHapticAdapter()** — No-op haptic feedback adapter (haptics not available in browsers).

## React Native Adapters

A convenience factory that auto-configures all native adapters for React Native:

\`\`\`typescript
import { createReactNativeAdapters } from '@selfxyz/mobile-sdk-alpha';

const adapters = createReactNativeAdapters({
  // Options for configuring native modules
});
\`\`\`

This automatically wires up NFC, biometrics, keychain, camera, filesystem, and other native capabilities using the corresponding React Native libraries.

## Two Main Flows

### 1. Onboarding Flow
The onboarding flow takes a user through identity document verification:
1. **Document Selection** — User selects their document type (passport, ID card, etc.)
2. **NFC Scan** — User scans the NFC chip on their document
3. **Proof Generation** — ZK proof is generated locally on the device

### 2. Disclosing Flow
The disclosing flow allows a user to share previously verified credentials:
- Selective disclosure of identity claims based on the verifier's request
- Uses previously generated proofs without re-scanning the document

## State Management

### XState Proving Machine
The SDK uses an XState state machine for deterministic orchestration of the proving flow. This ensures predictable state transitions and makes it easy to handle edge cases (NFC failures, user cancellation, timeout, etc.).

### Zustand Stores
Zustand is used for reactive state management across the SDK. Components and hooks subscribe to store slices for efficient re-rendering.

## Key Types

\`\`\`typescript
// Adapter bundle type
interface Adapters {
  crypto: CryptoAdapter;
  nfcScanner: NFCScannerAdapter;
  documents: DocumentsAdapter;
  network: NetworkAdapter;
  auth: AuthAdapter;
  storage: StorageAdapter;
  logger: LoggerAdapter;
}

// SDK configuration
interface Config {
  endpoint: string;
  debug?: boolean;
}

// Verification request from a verifier
interface VerificationRequest {
  userId?: string;
  scope?: string;
  disclosures: Disclosure[];
}

// The main client instance
interface SelfClient {
  startOnboarding(request: VerificationRequest): void;
  startDisclosing(request: VerificationRequest): void;
  getState(): SDKState;
  subscribe(listener: (event: SDKEvent) => void): () => void;
}

// Events emitted by the SDK
type SDKEvent =
  | { type: 'onboarding.started' }
  | { type: 'onboarding.documentSelected'; documentType: string }
  | { type: 'onboarding.nfcScanComplete' }
  | { type: 'onboarding.proofGenerated'; proof: object }
  | { type: 'onboarding.complete'; result: object }
  | { type: 'onboarding.error'; error: Error }
  | { type: 'disclosing.started' }
  | { type: 'disclosing.complete'; result: object }
  | { type: 'disclosing.error'; error: Error };

// Error categories for structured error handling
enum SdkErrorCategory {
  NFC = 'nfc',
  BIOMETRICS = 'biometrics',
  CRYPTO = 'crypto',
  NETWORK = 'network',
  STORAGE = 'storage',
  PROOF = 'proof',
  UNKNOWN = 'unknown',
}
\`\`\`
`;
export function registerSdkMobile(server, config) {
    server.resource("sdk-mobile", "self://sdk/mobile-alpha", async (uri) => ({
        contents: [
            {
                uri: uri.href,
                mimeType: "text/plain",
                text: SDK_MOBILE,
            },
        ],
    }));
}
//# sourceMappingURL=sdk-mobile.js.map