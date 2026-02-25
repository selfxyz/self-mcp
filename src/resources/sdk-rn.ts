import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { ServerConfig } from "../config.js";

const SDK_RN = `# @selfxyz/rn-sdk v0.0.1-alpha.1 — React Native SDK

## Overview

The React Native SDK provides a drop-in \`<SelfVerification>\` component that wraps a WebView containing the full Self verification UI. It handles NFC scanning, biometrics, camera, and secure storage through native bridge handlers — no network required for the UI itself, as the webview-app HTML/JS assets are bundled for on-device embedding.

## Main Component: SelfVerification

\`\`\`typescript
import { SelfVerification } from '@selfxyz/rn-sdk';

<SelfVerification
  request={verificationRequest}
  onSuccess={(result) => { /* handle success */ }}
  onFailure={(error) => { /* handle failure */ }}
  onCancel={() => { /* handle cancel */ }}
/>
\`\`\`

### SelfVerificationProps

\`\`\`typescript
interface SelfVerificationProps {
  request: VerificationRequest;    // The verification request configuration
  onSuccess: (result: VerificationResult) => void;
  onFailure: (error: Error) => void;
  onCancel: () => void;
}
\`\`\`

### VerificationResult

\`\`\`typescript
interface VerificationResult {
  success: boolean;
  userId?: string;
  verificationId?: string;
  proof?: object;
  claims?: object;
  error?: string;
}
\`\`\`

## MessageRouter

The \`MessageRouter\` class routes bridge messages between the embedded WebView and the native platform handlers. It receives messages from the webview-bridge protocol and dispatches them to the appropriate handler based on the message domain.

\`\`\`typescript
class MessageRouter {
  // Routes incoming BridgeRequest messages to the correct native handler
  // Returns BridgeResponse to be sent back to the WebView
}
\`\`\`

## Bridge Handlers

The SDK provides 5 native bridge handlers, each responsible for a specific domain of native functionality:

### 1. LifecycleHandler
Manages the verification flow lifecycle.
- **init** — Initialize the verification session
- **ready** — Signal that the WebView UI is ready
- **close** — Close the verification flow
- **error** — Report an error from the WebView
- **success** — Report successful verification with result data

### 2. BiometricHandler
Interfaces with device biometric authentication (Face ID, Touch ID, fingerprint).
- **authenticate** — Prompt the user for biometric authentication
- **isAvailable** — Check if biometrics are available on the device
- **getBiometryType** — Get the type of biometric sensor available

### 3. KeychainHandler
Manages secure credential storage via the device keychain.
- **get** — Retrieve a value from secure storage
- **set** — Store a value in secure storage
- **remove** — Remove a value from secure storage

### 4. NfcHandler
Interfaces with the device NFC reader for passport chip scanning.
- **scan** — Start an NFC scan session to read passport chip data
- **cancelScan** — Cancel an in-progress NFC scan
- **isSupported** — Check if the device supports NFC

### 5. CameraHandler
Interfaces with the device camera for MRZ (Machine Readable Zone) scanning.
- **scanMRZ** — Open the camera to scan the passport MRZ
- **isAvailable** — Check if the camera is available

## Peer Dependencies

The following peer dependencies must be installed in your React Native project:

\`\`\`json
{
  "react-native-webview": ">=13.0.0",
  "react-native-keychain": "^8.2.0",
  "react-native-nfc-manager": "^3.14.0",
  "react-native-biometrics": "^3.0.1",
  "react-native-fs": "^2.20.0"
}
\`\`\`

## Bundled Assets

The SDK includes bundled webview-app HTML/JS assets for on-device embedding. This means the verification UI loads locally without any network requests for the UI itself. The only network calls made are for proof verification against the Self backend.

## Integration Example

\`\`\`typescript
import React from 'react';
import { SelfVerification } from '@selfxyz/rn-sdk';
import { SelfAppBuilder } from '@selfxyz/common';

function VerifyScreen() {
  const selfApp = new SelfAppBuilder()
    .setAppName('My App')
    .setScope('my-app-scope')
    .setEndpoint('https://my-app.com/verify')
    .setUserId('user-uuid-here')
    .build();

  return (
    <SelfVerification
      request={selfApp}
      onSuccess={(result) => {
        console.log('Verified:', result.userId);
      }}
      onFailure={(error) => {
        console.error('Verification failed:', error);
      }}
      onCancel={() => {
        console.log('User cancelled');
      }}
    />
  );
}
\`\`\`
`;

export function registerSdkRn(
  server: McpServer,
  config: ServerConfig
): void {
  server.resource("sdk-rn", "self://sdk/react-native", async (uri) => ({
    contents: [
      {
        uri: uri.href,
        mimeType: "text/plain" as const,
        text: SDK_RN,
      },
    ],
  }));
}
