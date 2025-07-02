# server.py
from mcp.server.fastmcp import FastMCP
from typing import Literal

# Create an MCP server
mcp = FastMCP("Self-MCP")

# Entry point for running as module
def main():
    import asyncio
    asyncio.run(mcp.run())

# Use case explanations
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

2. **Backend - Verify Proofs**:
   - Install: `npm install @selfxyz/core`
   - Create endpoint to receive and verify proofs
   - Check humanity (attestation_id = 1)
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

# Code templates
CODE_TEMPLATES = {
    "frontend-qr": {
        "typescript": """import { SelfAppBuilder } from '@selfxyz/qrcode';

// Initialize Self QR code for {component_context}
const selfApp = new SelfAppBuilder({
  appName: 'My Application',
  scope: 'my-app-unique-scope', // Must match backend exactly
  endpoint: 'https://myapi.com/api/verify', // Your verification endpoint
  disclosures: {
    // Configure what to verify
    minimumAge: 18, // Optional: age verification
    nationality: true, // Optional: reveal nationality
    excludedCountries: ['IRN', 'PRK'], // Optional: exclude countries
    ofac: true, // Optional: OFAC check
  },
  // Optional: Add your logo
  logoBase64: 'data:image/png;base64,...',
  // Optional: User identifier
  userId: 'user-123'
}).build();

// React component example
export function VerificationQR() {
  return (
    <div>
      <h2>Verify with Self</h2>
      {selfApp}
    </div>
  );
}""",
        "javascript": """import { SelfAppBuilder } from '@selfxyz/qrcode';

// Initialize Self QR code for {component_context}
const selfApp = new SelfAppBuilder({
  appName: 'My Application',
  scope: 'my-app-unique-scope', // Must match backend exactly
  endpoint: 'https://myapi.com/api/verify', // Your verification endpoint
  disclosures: {
    // Configure what to verify
    minimumAge: 18, // Optional: age verification
    nationality: true, // Optional: reveal nationality
  }
}).build();

// Add to your HTML
document.getElementById('qr-container').appendChild(selfApp);"""
    },
    "backend-verify": {
        "typescript": """import { SelfBackendVerifier, getUserIdentifier } from '@selfxyz/core';

// Initialize verifier for {component_context}
const verifier = new SelfBackendVerifier(
  'https://forno.celo.org', // Celo RPC URL
  'my-app-unique-scope' // Must match frontend exactly
);

// Configure verification requirements
verifier.setMinimumAge(18); // If age verification needed
verifier.excludeCountries('IRN', 'PRK'); // If country restrictions needed
verifier.enableNameAndDobOfacCheck(); // If OFAC check needed

// Express.js endpoint example
app.post('/api/verify', async (req, res) => {
  try {
    const { proof, publicSignals } = req.body;
    
    // Extract user ID from proof
    const userId = await getUserIdentifier(publicSignals);
    
    // Verify the proof
    const result = await verifier.verify(proof, publicSignals);
    
    if (result.isValid) {
      // Success! User is verified
      // Store nullifier to prevent reuse: result.nullifier
      // Access disclosed data: result.credentialSubject
      
      res.json({
        success: true,
        userId,
        nullifier: result.nullifier,
        // Only return what you need
        age: result.credentialSubject.older_than,
        nationality: result.credentialSubject.nationality
      });
    } else {
      // Verification failed
      res.status(400).json({
        success: false,
        errors: result.isValidDetails
      });
    }
  } catch (error) {
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});""",
        "javascript": """const { SelfBackendVerifier, getUserIdentifier } = require('@selfxyz/core');

// Initialize verifier for {component_context}
const verifier = new SelfBackendVerifier(
  'https://forno.celo.org', // Celo RPC URL
  'my-app-unique-scope' // Must match frontend exactly
);

// Configure verification requirements
verifier.setMinimumAge(18); // If age verification needed

// Express.js endpoint example
app.post('/api/verify', async (req, res) => {
  try {
    const { proof, publicSignals } = req.body;
    
    // Verify the proof
    const result = await verifier.verify(proof, publicSignals);
    
    if (result.isValid) {
      res.json({ success: true });
    } else {
      res.status(400).json({ success: false });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});"""
    },
    "smart-contract": {
        "solidity": """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@selfxyz/contracts/contracts/abstract/SelfVerificationRoot.sol";

// Example contract for {component_context}
contract MyVerifiedApp is SelfVerificationRoot {
    // Track who has already verified (prevent double actions)
    mapping(uint256 => bool) public nullifierUsed;
    
    // Example: Track verified users
    mapping(address => bool) public verifiedUsers;
    
    constructor(address _hubAddress) SelfVerificationRoot(_hubAddress) {}
    
    function verifyAndExecute(
        SelfProof memory proof
    ) public {
        // 1. Verify the Self proof
        verifySelfProof(proof);
        
        // 2. Check nullifier hasn't been used
        require(!nullifierUsed[proof.nullifier], "Proof already used");
        nullifierUsed[proof.nullifier] = true;
        
        // 3. Validate requirements
        require(proof.scope == keccak256("my-app-unique-scope"), "Invalid scope");
        require(proof.attestationId == 1, "Must be passport"); // 1 = passport
        
        // 4. Optional: Check age
        require(proof.olderThan >= 18, "Must be 18 or older");
        
        // 5. Execute your logic
        verifiedUsers[msg.sender] = true;
        
        // Example: Mint NFT, allow access, distribute tokens, etc.
    }
    
    // Optional: Check if countries are excluded
    function verifyWithCountryCheck(
        SelfProof memory proof,
        uint256[] memory excludedCountries
    ) public {
        verifySelfProof(proof);
        
        // Check country not in excluded list
        for (uint i = 0; i < excludedCountries.length; i++) {
            require(
                proof.revealedData_packed[1] != excludedCountries[i], 
                "Country not allowed"
            );
        }
        
        // Continue with your logic...
    }
}"""
    }
}

# Common error solutions
ERROR_SOLUTIONS = {
    "scope": {
        "problem": "Scope mismatch between frontend and backend",
        "solution": """
The 'scope' parameter must match EXACTLY between frontend and backend:

**Frontend (QR code):**
```typescript
new SelfAppBuilder({
  scope: 'my-app-v1', // This exact string
  ...
})
```

**Backend (verifier):**
```typescript
new SelfBackendVerifier(
  rpcUrl,
  'my-app-v1' // Must be identical
)
```

Common mistakes:
- Extra spaces or typos
- Different versions (v1 vs v2)
- Using URLs as scope (use simple strings instead)
""",
        "related": ["Invalid scope", "Scope validation failed"]
    },
    "proof": {
        "problem": "Invalid or malformed proof data",
        "solution": """
Ensure proof data is properly transmitted:

1. **Check request body parsing:**
```typescript
app.use(express.json()); // Required for JSON parsing
```

2. **Verify proof structure:**
```typescript
const { proof, publicSignals } = req.body;
// Both must be present and properly formatted
```

3. **Common issues:**
- Missing JSON middleware
- Proof data corrupted in transit
- Using GET instead of POST
- CORS blocking the request
""",
        "related": ["Invalid proof", "Proof verification failed", "Malformed proof"]
    },
    "age": {
        "problem": "Age verification configuration error",
        "solution": """
Age verification requirements:

1. **Valid age range: 10-100 years**
```typescript
verifier.setMinimumAge(18); //  Valid
verifier.setMinimumAge(5);  //  Too low
verifier.setMinimumAge(150); //  Too high
```

2. **Frontend must request age disclosure:**
```typescript
disclosures: {
  minimumAge: 18 // Must be set in QR code
}
```

3. **Check proof includes age:**
```typescript
result.credentialSubject.older_than // Should have value
```
""",
        "related": ["Invalid age", "minimumAge must be between", "Age verification failed"]
    },
    "nullifier": {
        "problem": "Nullifier already used or invalid",
        "solution": """
Nullifiers prevent proof reuse. Each passport generates unique nullifiers per scope.

**Implement nullifier checking:**
```typescript
// Store nullifiers (database, Redis, or on-chain)
const usedNullifiers = new Set();

// Check before accepting proof
if (usedNullifiers.has(result.nullifier)) {
  return res.status(400).json({ 
    error: "Proof already used" 
  });
}

// Store after successful verification
usedNullifiers.add(result.nullifier);
```

**For smart contracts:**
```solidity
mapping(uint256 => bool) public nullifierUsed;
require(!nullifierUsed[proof.nullifier], "Already used");
nullifierUsed[proof.nullifier] = true;
```
""",
        "related": ["Nullifier already used", "Duplicate proof", "Proof reuse"]
    },
    "network": {
        "problem": "RPC or network connection issues",
        "solution": """
Self uses Celo blockchain. Ensure proper RPC configuration:

**Recommended RPC endpoints:**
```typescript
// Mainnet
'https://forno.celo.org'

// Testnet (Alfajores)
'https://alfajores-forno.celo-testnet.org'
```

**Check connectivity:**
```bash
curl https://forno.celo.org -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

**Common issues:**
- Firewall blocking RPC
- Using Ethereum RPC instead of Celo
- Rate limiting on free tier
""",
        "related": ["Network error", "RPC", "Connection failed", "Celo"]
    }
}


@mcp.tool()
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
    if use_case not in USE_CASE_GUIDES:
        return f"Unknown use case: {use_case}. Available options: airdrop, age-verification, humanity-check"
    
    return USE_CASE_GUIDES[use_case]


@mcp.tool()
async def generate_verification_code(
    component: Literal["frontend-qr", "backend-verify", "smart-contract"],
    language: Literal["typescript", "javascript", "solidity"] = "typescript"
) -> str:
    """
    Generate ready-to-use Self verification code for different components.
    
    Args:
        component: Which part to generate - 'frontend-qr', 'backend-verify', or 'smart-contract'
        language: Programming language - 'typescript', 'javascript', or 'solidity'
        
    Returns:
        Complete, working code example with comments
    """
    # Validate inputs
    if component not in CODE_TEMPLATES:
        return f"Unknown component: {component}. Available: frontend-qr, backend-verify, smart-contract"
    
    # Handle language compatibility
    if component == "smart-contract" and language != "solidity":
        language = "solidity"  # Force solidity for smart contracts
    elif component != "smart-contract" and language == "solidity":
        language = "typescript"  # Default to typescript for non-contracts
    
    # Check if template exists for language
    if language not in CODE_TEMPLATES[component]:
        available = list(CODE_TEMPLATES[component].keys())
        return f"Language '{language}' not available for {component}. Available: {', '.join(available)}"
    
    # Get template and add context
    template = CODE_TEMPLATES[component][language]
    context_map = {
        "frontend-qr": "Self verification QR code",
        "backend-verify": "Self proof verification", 
        "smart-contract": "on-chain Self verification"
    }
    
    return template.replace("{component_context}", context_map[component])


@mcp.tool() 
async def debug_verification_error(
    error_message: str,
    context: Literal["", "scope-mismatch", "proof-invalid", "age-verification", "nullifier-reuse", "network-error"] = ""
) -> str:
    """
    Diagnose Self verification errors and provide solutions.
    
    Args:
        error_message: The error message you're encountering
        context: Optional hint about the error type
        
    Returns:
        Detailed explanation of the problem and how to fix it
    """
    error_lower = error_message.lower()
    
    # Try to match error to known solutions
    matched_solution = None
    
    # Direct context match
    if context:
        context_map = {
            "scope-mismatch": "scope",
            "proof-invalid": "proof", 
            "age-verification": "age",
            "nullifier-reuse": "nullifier",
            "network-error": "network"
        }
        if context in context_map:
            matched_solution = ERROR_SOLUTIONS[context_map[context]]
    
    # If no context or no match, search error message
    if not matched_solution:
        for key, solution in ERROR_SOLUTIONS.items():
            # Check main problem keywords
            if key in error_lower:
                matched_solution = solution
                break
            # Check related keywords
            for related in solution.get("related", []):
                if related.lower() in error_lower:
                    matched_solution = solution
                    break
            if matched_solution:
                break
    
    # Build response
    if matched_solution:
        response = f"## Error: {matched_solution['problem']}\n\n"
        response += f"**Your error:** `{error_message}`\n\n"
        response += matched_solution['solution']
    else:
        # Generic debugging steps
        response = f"## Debugging Self Verification Error\n\n"
        response += f"**Your error:** `{error_message}`\n\n"
        response += """
This error isn't in our common issues database. Here's a general debugging approach:

1. **Check Basic Setup:**
   - Ensure @selfxyz/qrcode is installed on frontend
   - Ensure @selfxyz/core is installed on backend
   - Verify Celo RPC URL is accessible

2. **Verify Configuration Match:**
   - Frontend scope === Backend scope (exact match)
   - Same disclosures requested and verified

3. **Inspect Network Traffic:**
   - Check browser DevTools for request/response
   - Ensure proof and publicSignals are sent
   - Verify endpoint URL is correct

4. **Enable Debug Logging:**
   ```typescript
   console.log('Proof:', proof);
   console.log('PublicSignals:', publicSignals);
   console.log('Verification result:', result);
   ```

5. **Common Issues to Check:**
   - CORS configuration on backend
   - JSON body parsing middleware
   - Correct HTTP method (POST)
   - Valid RPC connection to Celo

If the issue persists, please check:
- Self documentation: https://docs.self.xyz
- GitHub issues: https://github.com/selfxyz/self/issues
"""
    
    return response