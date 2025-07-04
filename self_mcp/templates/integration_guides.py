"""Integration guides for different Self protocol use cases"""

USE_CASE_GUIDES = {
    "airdrop": """
# Self Integration for Airdrop Protection

## Overview
Protect your token airdrop from bots and sybil attacks by requiring users to prove their humanity using government-issued IDs.

## Integration Steps

1. **Frontend - Add QR Code**:
   - Install: `npm install @selfxyz/qrcode`
   - Display QR code for users to scan with Self app
   - Set verification endpoint to your backend
   - Configure scope to match backend exactly

2. **Backend - Verify Proofs**:
   - Install: `npm install @selfxyz/core`
   - Create endpoint to receive and verify proofs
   - Important: Backend setup requires:
     - IConfigStorage implementation for caching
     - AttestationId.E_PASSPORT in allowedIds
     - UserIdType (ADDRESS or UUID)
   - Check attestation_id = 1 for passport
   - Store nullifier to prevent double claims

3. **Smart Contract (Optional)**:
   - Extend SelfVerificationRoot contract
   - Implement on-chain verification for fully decentralized airdrops
   - Check nullifiers on-chain to prevent reuse

## Key Considerations:
- Each passport can only claim once (nullifier prevents reuse)
- Users maintain privacy - only humanity is proven
- No personal data is revealed
""",
    "age-verification": """
# Self Integration for Age Verification

## Overview
Verify users are above a certain age without revealing their exact birthdate or other personal information.

## Integration Steps

1. **Frontend - QR Code Setup**:
   - Configure minimum age in disclosures (e.g., 18, 21)
   - Display QR code with your app branding
   - Handle success/failure callbacks

2. **Backend - Age Check**:
   - Use `setMinimumAge()` in verifier
   - Age must be between 10-100 years
   - Verify proof includes age attestation

3. **Privacy Features**:
   - Only "older than X" is revealed, not exact age
   - No other personal data exposed
   - Proof is cryptographically secure

## Common Use Cases:
- Adult content platforms
- Age-restricted product sales
- Regulatory compliance
- Event access control
""",
    "humanity-check": """
# Self Integration for Humanity Verification

## Overview
Verify users are real humans (not bots) by checking they possess a valid government-issued ID.

## Integration Steps

1. **Frontend - Simple Integration**:
   - Minimal configuration needed
   - Just check attestation_id = 1 (passport)
   - No specific attributes required

2. **Backend - Humanity Verification**:
   - Verify proof validity
   - Check attestation_id equals 1
   - Optionally store userId for sessions

3. **Use Cases**:
   - Social media verification
   - Anti-bot protection
   - Quadratic funding
   - DAO participation

## Benefits:
- Strongest sybil resistance
- Privacy-preserving
- Government-level identity assurance
- No KYC data storage needed
"""
}