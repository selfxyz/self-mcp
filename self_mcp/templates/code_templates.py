"""Code templates for Self protocol components"""

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