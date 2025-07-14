"""Tool for explaining Self protocol integration"""

from typing import Literal
from ..utils.github_client import get_docs_client


async def explain_self_integration(
    use_case: Literal["airdrop", "age-verification", "humanity-check"]
) -> str:
    """
    Explain how to integrate Self for a specific use case with step-by-step guidance.
    
    Args:
        use_case: The integration scenario - 'airdrop', 'age-verification', or 'humanity-check'
        
    Returns:
        Detailed explanation with steps and code examples
    """
    client = get_docs_client()
    
    # Map use cases to documentation files
    use_case_map = {
        "airdrop": "use-cases/airdrop.md",
        "age-verification": "use-cases/age-verification.md",
        "humanity-check": "use-cases/humanity-check.md"
    }
    
    doc_path = use_case_map.get(use_case)
    if not doc_path:
        return f"Unknown use case: {use_case}. Available options: airdrop, age-verification, humanity-check"
    
    # Fetch the use case documentation
    content = await client.fetch_document(doc_path)
    
    if content:
        return f"# Self Protocol Integration: {use_case.replace('-', ' ').title()}\n\n{content}"
    
    # Fallback to basic guide
    return generate_basic_guide(use_case)


def generate_basic_guide(use_case: str) -> str:
    """Generate basic integration guide if docs unavailable"""
    
    if use_case == "airdrop":
        return """# Self Protocol Integration: Airdrop

## Overview
Use Self protocol to ensure fair airdrops by verifying unique humans while preserving privacy.

## Key Benefits
- **Sybil Resistance**: One person = one claim
- **Privacy Preserving**: No personal data exposed
- **Global Reach**: Works with passports worldwide
- **Bot Protection**: Only real humans can claim

## Implementation Steps

### 1. Smart Contract Setup
```solidity
contract SelfVerifiedAirdrop {
    IHub public hub;
    mapping(uint256 => bool) public claimed;
    uint256 public airdropAmount = 100 * 10**18;
    
    function claimAirdrop(
        uint256 scopeId,
        uint256 nullifier, 
        uint256 modulus,
        uint256[8] calldata proof
    ) external {
        require(!claimed[nullifier], "Already claimed");
        require(hub.verify(scopeId, nullifier, modulus, proof), "Invalid proof");
        
        claimed[nullifier] = true;
        IERC20(token).transfer(msg.sender, airdropAmount);
    }
}
```

### 2. Frontend Integration
```typescript
const selfApp = new SelfAppBuilder({
    appName: "Airdrop Claim",
    scope: "airdrop-2024",
    endpoint: "https://api.myapp.com/verify",
    userId: address, // User's wallet address
    disclosures: {
        // No age or country restrictions for airdrops
    }
}).build();
```

### 3. Nullifier Management
Store nullifiers to prevent double-claiming across sessions."""

    elif use_case == "age-verification":
        return """# Self Protocol Integration: Age Verification

## Overview
Verify users meet minimum age requirements without revealing their exact birthdate.

## Key Features
- **Privacy First**: Only reveals if user is old enough
- **Configurable**: Set any minimum age (10-100)
- **Compliant**: Meets regulatory requirements
- **User Friendly**: Simple QR code scan

## Implementation Steps

### 1. Frontend Configuration
```typescript
const selfApp = new SelfAppBuilder({
    appName: "Age Restricted App",
    scope: "age-verify-app",
    endpoint: "https://api.myapp.com/verify",
    userId: userId,
    disclosures: {
        minimumAge: 18,  // or 21 for alcohol
        name: true,      // Optional
        nationality: true // Optional
    }
}).build();
```

### 2. Backend Verification
```typescript
class AgeConfigStorage {
    async getConfig(configId) {
        return {
            olderThan: 18,  // Must match frontend
            excludedCountries: [], // Optional restrictions
            ofac: false     // OFAC check if needed
        };
    }
}

const verifier = new SelfBackendVerifier(
    "age-verify-app",
    "https://api.myapp.com/verify",
    false,
    allowedIds,
    new AgeConfigStorage(),
    UserIdType.UUID
);
```

### 3. Access Control
Grant access only to verified users who meet age requirements."""

    else:  # humanity-check
        return """# Self Protocol Integration: Humanity Check

## Overview
Verify users are real humans without collecting personal information.

## Use Cases
- **Bot Prevention**: Keep automated accounts out
- **Fair Voting**: One person, one vote
- **Gaming**: Prevent multi-accounting
- **Community Access**: Human-only spaces

## Implementation Steps

### 1. Simple Frontend
```typescript
const selfApp = new SelfAppBuilder({
    appName: "Human Only App",
    scope: "humanity-check",
    endpoint: "https://api.myapp.com/verify",
    userId: generateUserId(),
    disclosures: {
        // No specific requirements
        // Just prove you're human
    }
}).build();
```

### 2. Minimal Backend
```typescript
// Just verify the proof is valid
const result = await verifier.verify(
    attestationId,
    proof,
    pubSignals,
    userContextData
);

if (result.isValidDetails.isValid) {
    // User is verified human
    grantAccess(userId);
}
```

### 3. Session Management
Track verified humans without storing personal data."""