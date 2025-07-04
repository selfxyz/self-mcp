"""Integration guides for different Self protocol use cases"""

USE_CASE_GUIDES = {
    "airdrop": """
# Self Integration for Airdrop Protection (V2)

## Overview
Protect your token airdrop from bots and sybil attacks by requiring users to prove their humanity using government-issued IDs with zero-knowledge proofs.

## Integration Steps

1. **Frontend - Add QR Code (V2)**:
   - Install: `npm install @selfxyz/qrcode @selfxyz/core uuid`
   - Use SelfAppBuilder with V2 configuration:
     ```typescript
     const selfApp = new SelfAppBuilder({
       appName: "My Airdrop",
       scope: "airdrop-v2",
       endpoint: "https://myapi.com/verify",
       userId: uuidv4(),
       version: 2,
       userDefinedData: Buffer.from(JSON.stringify({
         action: "airdrop_claim",
         amount: "100"
       })).toString('hex').padEnd(128, '0'),
       disclosures: {
         minimumAge: 18, // Must match backend config
         excludedCountries: ['IRN', 'PRK'], // Sanctions compliance
         ofac: true
       }
     }).build();
     ```

2. **Backend - Verify Proofs (V2)**:
   - Install: `npm install @selfxyz/core`
   - Implement IConfigStorage for verification requirements
   - Use new SelfBackendVerifier constructor:
     ```typescript
     const verifier = new SelfBackendVerifier(
       'airdrop-v2',
       'https://myapi.com/verify',
       false, // Production mode
       AllIds, // Accept all document types
       configStorage,
       UserIdType.UUID
     );
     ```
   - Verify with: `verifier.verify(attestationId, proof, pubSignals, userContextData)`
   - Store nullifiers to prevent double claims

3. **Smart Contract (V2)**:
   - Use V2 contracts: `@selfxyz/contracts`
   - Extend SelfVerificationRoot with V2 patterns
   - Implement getConfigId() for verification configuration
   - Use V2 Hub address: `0xe57F4773bd9c9d8b6Cd70431117d353298B9f5BF` (Celo Mainnet)
   - Use V2 Testnet Hub: `0x68c931C9a534D37aa78094877F46fE46a49F1A51` (Celo Testnet)

## Key V2 Features:
- **Dynamic Configuration**: Different rules based on claim amount via IConfigStorage
- **Attestation ID Support**: Accepts passports (1) and EU ID cards (2)
- **Enhanced Privacy**: userDefinedData for context-aware verification (256 bytes)
- **Better Error Handling**: ConfigMismatchError for debugging
- **Nullifier Tracking**: Prevents multiple claims per document
- **GenericDiscloseOutputV2**: Enhanced output structure with all passport fields
- **Multi-Document Routing**: Automatic handling based on document type

## Configuration Matching:
⚠️ **Critical**: Frontend disclosures MUST exactly match backend configuration
- Use Configuration Tools: https://tools.self.xyz/
- Test with both mainnet (real) and testnet (mock) environments
""",
    "age-verification": """
# Self Integration for Age Verification (V2)

## Overview
Verify users are above a certain age without revealing their exact birthdate or other personal information using zero-knowledge proofs.

## Integration Steps

1. **Frontend - QR Code Setup (V2)**:
   - Configure with V2 builder pattern:
     ```typescript
     const selfApp = new SelfAppBuilder({
       appName: "Age Gate",
       scope: "age-check-v2",
       endpoint: "https://myapi.com/verify",
       userId: uuidv4(),
       version: 2,
       userDefinedData: Buffer.from(JSON.stringify({
         action: "age_verification",
         required_age: 21
       })).toString('hex').padEnd(128, '0'),
       disclosures: {
         minimumAge: 21, // Must match backend exactly
         nationality: false, // Don't request nationality
         name: false // Don't request name
       }
     }).build();
     ```

2. **Backend - Age Check (V2)**:
   - Implement configuration storage:
     ```typescript
     class AgeConfigStorage {
       async getConfig(configId) {
         return {
           olderThan: 21, // Must match frontend minimumAge
           excludedCountries: [], // Optional
           ofac: false // Optional for age-only checks
         };
       }
     }
     ```
   - Use SelfBackendVerifier with V2 constructor
   - Check `result.isValidDetails.isOlderThanValid` for age verification
   - Access age proof: `result.discloseOutput.olderThan`

3. **Privacy Features (Enhanced in V2)**:
   - Only "older than X" is cryptographically proven
   - No exact age, birthdate, or other data revealed
   - Support for multiple document types (passport + EU ID)
   - Context-aware verification based on userDefinedData

## Common Use Cases:
- Adult content platforms (18+/21+)
- Age-restricted product sales
- Regulatory compliance (COPPA, GDPR)
- Event access control
- Gaming platforms with age restrictions

## V2 Improvements:
- **Better Error Handling**: Specific age validation errors
- **Multiple Document Types**: Accept both passports and EU ID cards
- **Dynamic Age Requirements**: Different ages based on context
- **Enhanced Security**: Improved proof validation
""",
    "humanity-check": """
# Self Integration for Humanity Verification (V2)

## Overview
Verify users are real humans (not bots) by checking they possess a valid government-issued ID using zero-knowledge proofs.

## Integration Steps

1. **Frontend - Simple Integration (V2)**:
   - Minimal configuration for basic humanity check:
     ```typescript
     const selfApp = new SelfAppBuilder({
       appName: "Humanity Check",
       scope: "humanity-v2",
       endpoint: "https://myapi.com/verify",
       userId: uuidv4(),
       version: 2,
       userDefinedData: Buffer.from(JSON.stringify({
         action: "humanity_check",
         platform: "social_media"
       })).toString('hex').padEnd(128, '0'),
       disclosures: {
         // Minimal disclosure - just prove document validity
         minimumAge: 10, // Very low threshold
         nationality: false,
         name: false
       }
     }).build();
     ```

2. **Backend - Humanity Verification (V2)**:
   - Accept multiple document types:
     ```typescript
     const allowedIds = new Map();
     allowedIds.set(1, true); // Electronic passports
     allowedIds.set(2, true); // EU ID cards
     ```
   - Verify proof validity with minimal config:
     ```typescript
     const result = await verifier.verify(
       attestationId, proof, pubSignals, userContextData
     );
     // Check result.isValidDetails.isValid for humanity proof
     ```
   - Store nullifiers to prevent bot farms with same documents

3. **Use Cases**:
   - Social media verification (Twitter/X blue check alternative)
   - Anti-bot protection for platforms
   - Quadratic funding participation
   - DAO governance participation
   - Gaming anti-cheat systems
   - Comment system verification

## V2 Benefits:
- **Strongest Sybil Resistance**: Government-level document validation
- **Privacy-Preserving**: No personal data revealed, just humanity proof
- **Multiple Document Support**: Passports + EU ID cards
- **Global Coverage**: Works with 170+ countries' documents
- **No KYC Storage**: Zero personal data stored
- **Bot-Proof**: One verification per physical document

## Implementation Notes:
- Use minimal disclosures for maximum privacy
- Store nullifiers to prevent multiple accounts per document
- Consider rate limiting to prevent abuse
- Handle both attestation types (passport=1, EU ID=2)
"""
}