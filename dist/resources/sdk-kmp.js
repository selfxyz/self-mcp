const SDK_KMP = `# @selfxyz/kmp-sdk v0.0.1-alpha — Kotlin Multiplatform SDK

## Overview

The Kotlin Multiplatform (KMP) SDK enables native Android and iOS integrations from shared Kotlin code. It uses the same bridge protocol as the React Native SDK and provides native handlers for NFC, camera, biometrics, keychain, and lifecycle management. The SDK builds to AAR (Android) and XCFramework (iOS) artifacts via Gradle.

## Main API

\`\`\`kotlin
SelfSdk.configure(config).launch(request, callback)
\`\`\`

### SelfSdkConfig

\`\`\`kotlin
data class SelfSdkConfig(
    val endpoint: String = "https://api.self.xyz",  // API endpoint
    val debug: Boolean = false                       // Enable debug logging
)
\`\`\`

### VerificationRequest

\`\`\`kotlin
data class VerificationRequest(
    val userId: String? = null,       // Optional user identifier
    val scope: String? = null,        // Verification scope
    val disclosures: List<Disclosure> // List of requested disclosures
)
\`\`\`

### SelfSdkCallback

\`\`\`kotlin
interface SelfSdkCallback {
    fun onSuccess(result: VerificationResult)
    fun onFailure(error: SelfSdkError)
    fun onCancelled()
}
\`\`\`

### VerificationResult

\`\`\`kotlin
data class VerificationResult(
    val success: Boolean,
    val userId: String?,
    val verificationId: String?,
    val proof: JsonObject?,
    val claims: JsonObject?,
    val error: String?
)
\`\`\`

### SelfSdkError

\`\`\`kotlin
data class SelfSdkError(
    val code: String,
    val message: String,
    val cause: Throwable? = null
)
\`\`\`

## 5 Native Handlers

The KMP SDK provides 5 native handlers that implement the bridge protocol domains:

### 1. NFC Handler
Reads passport/ID NFC chips using platform-native NFC APIs.
- Android: Uses \`android.nfc.NfcAdapter\` and \`IsoDep\` tag technology
- iOS: Uses Core NFC framework (in progress)

### 2. Camera Handler
Captures MRZ data from passport/ID documents using the device camera.
- Android: Uses CameraX API
- iOS: Uses AVFoundation (in progress)

### 3. Biometrics Handler
Provides biometric authentication prompts.
- Android: Uses AndroidX Biometric library
- iOS: Uses Local Authentication framework (in progress)

### 4. Keychain Handler
Manages secure credential storage.
- Android: Uses Android Keystore system
- iOS: Uses iOS Keychain Services (in progress)

### 5. Lifecycle Handler
Manages the verification flow lifecycle (init, ready, close, error, success).

## Bridge Protocol

The KMP SDK uses the same bridge protocol (v1) as the React Native SDK. Messages are exchanged between the native layer and an embedded WebView using the standard \`BridgeRequest\`, \`BridgeResponse\`, and \`BridgeEvent\` message types. See \`self://sdk/webview-bridge\` for the full protocol specification.

## Build Artifacts

The SDK is built with Gradle and produces:
- **Android:** AAR (Android Archive) — drop-in dependency for Android projects
- **iOS:** XCFramework — universal framework for iOS projects

\`\`\`kotlin
// build.gradle.kts
kotlin {
    androidTarget()
    iosX64()
    iosArm64()
    iosSimulatorArm64()
}
\`\`\`

## Platform Status

- **Android:** Fully implemented. All 5 native handlers are functional.
- **iOS:** In progress via pull request. Core architecture is in place; native handler implementations are being finalized.

## Integration Example (Android)

\`\`\`kotlin
import xyz.self.sdk.SelfSdk
import xyz.self.sdk.SelfSdkConfig
import xyz.self.sdk.VerificationRequest
import xyz.self.sdk.SelfSdkCallback
import xyz.self.sdk.VerificationResult
import xyz.self.sdk.SelfSdkError

class VerifyActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val config = SelfSdkConfig(
            endpoint = "https://api.self.xyz",
            debug = true
        )

        val request = VerificationRequest(
            userId = "user-uuid",
            scope = "my-app-scope",
            disclosures = listOf(/* disclosure config */)
        )

        SelfSdk.configure(config).launch(request, object : SelfSdkCallback {
            override fun onSuccess(result: VerificationResult) {
                // Handle successful verification
                Log.d("Self", "Verified: \${result.userId}")
            }

            override fun onFailure(error: SelfSdkError) {
                // Handle failure
                Log.e("Self", "Failed: \${error.message}")
            }

            override fun onCancelled() {
                // Handle user cancellation
                Log.d("Self", "User cancelled")
            }
        })
    }
}
\`\`\`
`;
export function registerSdkKmp(server, config) {
    server.resource("sdk-kmp", "self://sdk/kmp", async (uri) => ({
        contents: [
            {
                uri: uri.href,
                mimeType: "text/plain",
                text: SDK_KMP,
            },
        ],
    }));
}
//# sourceMappingURL=sdk-kmp.js.map