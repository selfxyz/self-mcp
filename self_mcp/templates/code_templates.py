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
        "typescript": """import { 
  SelfBackendVerifier, 
  AttestationId,
  UserIdType,
  IConfigStorage,
  castToUserIdentifier
} from '@selfxyz/core';

// Initialize config storage (required for Self SDK)
class SimpleConfigStorage implements IConfigStorage {
  private configs = new Map();
  
  async getConfig(configId: string) {
    return this.configs.get(configId);
  }
  
  async setConfig(configId: string, config: any) {
    this.configs.set(configId, config);
  }
}

// Initialize verifier for {component_context}
const configStorage = new SimpleConfigStorage();
const allowedIds = new Map([
  [AttestationId.E_PASSPORT, true], // Allow passport verification
  // [AttestationId.EU_ID_CARD, true], // Uncomment to allow EU ID cards
]);

const verifier = new SelfBackendVerifier(
  'my-app-unique-scope', // Must match frontend exactly
  'https://api.self.xyz/v1', // Self API endpoint
  false, // mockPassport: false for production
  allowedIds,
  configStorage,
  UserIdType.ADDRESS // or UserIdType.UUID
);

// Configure verification requirements
await verifier.setMinimumAge(18); // If age verification needed
await verifier.excludeCountries(['IRN', 'PRK']); // If country restrictions needed
await verifier.enableNameAndDobOfacCheck(); // If OFAC check needed

// Express.js endpoint example
app.post('/api/verify', async (req, res) => {
  try {
    const { attestationId, proof, publicSignals, userContextData } = req.body;
    
    // Convert public signals to proper format
    const pubSignals = publicSignals.map((s: string) => BigInt(s));
    
    // Verify the proof
    const result = await verifier.verify(
      attestationId,
      proof,
      pubSignals,
      userContextData || ''
    );
    
    if (result.isValid) {
      // Extract user identifier
      const userId = castToUserIdentifier(
        pubSignals,
        UserIdType.ADDRESS
      );
      
      // Success! User is verified
      res.json({
        success: true,
        userId,
        nullifier: result.nullifier,
        // Access disclosed data
        credentialSubject: result.credentialSubject
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
        "javascript": """const { 
  SelfBackendVerifier, 
  AttestationId,
  UserIdType,
  castToUserIdentifier
} = require('@selfxyz/core');

// Initialize config storage (required for Self SDK)
class SimpleConfigStorage {
  constructor() {
    this.configs = new Map();
  }
  
  async getConfig(configId) {
    return this.configs.get(configId);
  }
  
  async setConfig(configId, config) {
    this.configs.set(configId, config);
  }
}

// Initialize verifier for {component_context}
const configStorage = new SimpleConfigStorage();
const allowedIds = new Map([
  [AttestationId.E_PASSPORT, true], // Allow passport verification
]);

const verifier = new SelfBackendVerifier(
  'my-app-unique-scope', // Must match frontend exactly
  'https://api.self.xyz/v1', // Self API endpoint
  false, // mockPassport: false for production
  allowedIds,
  configStorage,
  UserIdType.ADDRESS // or UserIdType.UUID
);

// Configure verification requirements
async function setupVerifier() {
  await verifier.setMinimumAge(18);
  await verifier.excludeCountries(['IRN', 'PRK']);
}

// Express.js endpoint example
app.post('/api/verify', async (req, res) => {
  try {
    const { attestationId, proof, publicSignals, userContextData } = req.body;
    
    // Convert public signals to proper format
    const pubSignals = publicSignals.map(s => BigInt(s));
    
    // Verify the proof
    const result = await verifier.verify(
      attestationId,
      proof,
      pubSignals,
      userContextData || ''
    );
    
    if (result.isValid) {
      // Extract user identifier
      const userId = castToUserIdentifier(
        pubSignals,
        UserIdType.ADDRESS
      );
      
      res.json({ 
        success: true,
        userId,
        nullifier: result.nullifier
      });
    } else {
      res.status(400).json({ 
        success: false,
        errors: result.isValidDetails 
      });
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