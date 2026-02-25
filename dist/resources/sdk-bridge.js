const SDK_BRIDGE = `# @selfxyz/webview-bridge v0.0.1-alpha.1 — WebView Bridge Protocol

## Overview

The webview-bridge package defines the communication protocol between a host application (React Native or web) and the Self verification WebView. It provides the \`WebViewBridge\` class, typed message formats, and a domain-based method routing system. This is Bridge Protocol v1.

## Constants

\`\`\`typescript
const BRIDGE_PROTOCOL_VERSION = 1;
const DEFAULT_TIMEOUT_MS = 30000;  // 30 seconds
\`\`\`

## WebViewBridge Class

The main bridge interface for sending and receiving messages between the host app and the WebView.

\`\`\`typescript
class WebViewBridge {
  constructor(transport: BridgeTransport);

  // Send a request to a domain method and await the response
  request<T>(domain: string, method: string, params?: object): Promise<T>;

  // Listen for events from the other side
  on(domain: string, method: string, handler: (params: object) => void): void;

  // Remove an event listener
  off(domain: string, method: string, handler: (params: object) => void): void;

  // Destroy the bridge and clean up listeners
  destroy(): void;
}
\`\`\`

## Protocol Message Format

All messages follow this structure:

\`\`\`typescript
interface BridgeMessage {
  type: 'request' | 'response' | 'event';
  version: number;       // BRIDGE_PROTOCOL_VERSION (1)
  id: string;            // Unique message ID (UUID)
  domain: string;        // Target domain (e.g. 'nfc', 'biometrics')
  method: string;        // Method within the domain (e.g. 'scan', 'authenticate')
  params?: object;       // Method parameters
  timestamp: number;     // Unix timestamp in milliseconds
}
\`\`\`

### Message Types

\`\`\`typescript
// Request: sent from one side to invoke a method
interface BridgeRequest extends BridgeMessage {
  type: 'request';
}

// Response: sent back in reply to a request
interface BridgeResponse extends BridgeMessage {
  type: 'response';
  result?: object;       // Success result data
  error?: {
    code: string;
    message: string;
  };
}

// Event: fire-and-forget notification (no response expected)
interface BridgeEvent extends BridgeMessage {
  type: 'event';
}
\`\`\`

## Transport

The bridge uses different transports depending on the runtime environment:

- **React Native WebView:** \`window.ReactNativeWebView.postMessage(JSON.stringify(message))\`
- **Web (iframe):** \`window.parent.postMessage(message, '*')\`

## 10 Domains and Their Methods

### 1. nfc
NFC chip reading for passport/ID scanning.
- **scan** — Start an NFC scan session. Returns raw chip data (DG1, DG2, SOD, etc.)
- **cancelScan** — Cancel an in-progress NFC scan
- **isSupported** — Check if the device supports NFC. Returns \`{ supported: boolean }\`

### 2. biometrics
Device biometric authentication.
- **authenticate** — Prompt user for biometric auth (Face ID / Touch ID / fingerprint). Returns \`{ success: boolean }\`
- **isAvailable** — Check if biometrics are available. Returns \`{ available: boolean }\`
- **getBiometryType** — Get the biometry type. Returns \`{ type: 'FaceID' | 'TouchID' | 'Fingerprint' | 'None' }\`

### 3. secureStorage
Secure key-value storage via device keychain/keystore.
- **get** — Retrieve a stored value by key. Params: \`{ key: string }\`. Returns \`{ value: string | null }\`
- **set** — Store a key-value pair. Params: \`{ key: string, value: string }\`
- **remove** — Remove a stored value. Params: \`{ key: string }\`

### 4. camera
Camera access for MRZ scanning.
- **scanMRZ** — Open camera to scan passport MRZ. Returns parsed MRZ data
- **isAvailable** — Check camera availability. Returns \`{ available: boolean }\`

### 5. crypto
Cryptographic operations.
- **sign** — Sign data with a private key. Params: \`{ data: string, keyId: string }\`. Returns \`{ signature: string }\`
- **generateKey** — Generate a new key pair. Returns \`{ keyId: string }\`
- **getPublicKey** — Get the public key for a key ID. Params: \`{ keyId: string }\`. Returns \`{ publicKey: string }\`

### 6. haptic
Haptic feedback.
- **trigger** — Trigger a haptic feedback event. Params: \`{ type: 'success' | 'warning' | 'error' | 'light' | 'medium' | 'heavy' }\`

### 7. analytics
Event tracking and logging.
- **trackEvent** — Track a general analytics event. Params: \`{ name: string, properties?: object }\`
- **trackNfcEvent** — Track an NFC-specific event. Params: \`{ event: string, data?: object }\`
- **logNfcEvent** — Log an NFC event for debugging. Params: \`{ level: string, message: string }\`

### 8. lifecycle
Verification flow lifecycle management.
- **ready** — Signal that the WebView is ready to receive messages
- **dismiss** — Request the host to dismiss the WebView
- **setResult** — Set the verification result. Params: \`{ success: boolean, data?: object, error?: string }\`

### 9. documents
Document catalog management.
- **loadCatalog** — Load the full document catalog. Returns \`{ catalog: DocumentCatalog }\`
- **saveCatalog** — Save the document catalog. Params: \`{ catalog: DocumentCatalog }\`
- **loadById** — Load a specific document by ID. Params: \`{ id: string }\`. Returns \`{ document: object | null }\`
- **save** — Save a document. Params: \`{ document: object }\`
- **delete** — Delete a document. Params: \`{ id: string }\`

### 10. navigation
Navigation control within the WebView.
- **goBack** — Navigate back to the previous screen
- **goTo** — Navigate to a specific screen. Params: \`{ screen: string, params?: object }\`

## Usage Example

\`\`\`typescript
import { WebViewBridge } from '@selfxyz/webview-bridge';

// Inside the WebView
const bridge = new WebViewBridge(webViewTransport);

// Check NFC support
const { supported } = await bridge.request('nfc', 'isSupported');

// Start NFC scan
const chipData = await bridge.request('nfc', 'scan');

// Authenticate with biometrics
const { success } = await bridge.request('biometrics', 'authenticate');

// Store data securely
await bridge.request('secureStorage', 'set', { key: 'proof', value: proofJson });

// Signal completion
await bridge.request('lifecycle', 'setResult', {
  success: true,
  data: { proof, claims }
});
\`\`\`
`;
export function registerSdkBridge(server, config) {
    server.resource("sdk-bridge", "self://sdk/webview-bridge", async (uri) => ({
        contents: [
            {
                uri: uri.href,
                mimeType: "text/plain",
                text: SDK_BRIDGE,
            },
        ],
    }));
}
//# sourceMappingURL=sdk-bridge.js.map