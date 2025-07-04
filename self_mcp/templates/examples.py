"""Complete example implementations for Self protocol"""

EXAMPLES = {
    "airdrop": """# Complete Airdrop Example (V2)

## Smart Contract (V2)
```solidity
pragma solidity ^0.8.0;
import "@selfxyz/contracts/contracts/abstract/SelfVerificationRoot.sol";
import "@selfxyz/contracts/contracts/constants/AttestationId.sol";
import "@selfxyz/contracts/contracts/interfaces/ISelfVerificationRoot.sol";

contract PassportAirdropV2 is SelfVerificationRoot {
    mapping(uint256 => bool) public claimed;
    uint256 public constant AIRDROP_AMOUNT = 100 * 10**18;
    bytes32 public configId;
    
    constructor(
        address _hub, // V2 Hub: 0xe57F4773bd9c9d8b6Cd70431117d353298B9f5BF
        uint256 _scope
    ) SelfVerificationRoot(_hub, _scope) {
        configId = 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef;
    }
    
    function getConfigId(
        bytes32 destinationChainId,
        bytes32 userIdentifier,
        bytes memory userDefinedData
    ) public view override returns (bytes32) {
        return configId;
    }
    
    function claim(SelfStructs.SelfProof memory proof, bytes memory userData) external {
        verifySelfProof(proof, userData);
        require(!claimed[proof.nullifier], "Already claimed");
        require(
            proof.attestationId == AttestationId.E_PASSPORT || 
            proof.attestationId == AttestationId.EU_ID_CARD,
            "Must be passport or EU ID"
        );
        
        claimed[proof.nullifier] = true;
        payable(msg.sender).transfer(AIRDROP_AMOUNT);
    }
    
    // V2 Hook for custom logic
    function customVerificationHook(
        ISelfVerificationRoot.GenericDiscloseOutputV2 memory output,
        bytes memory userData
    ) internal virtual override {
        // Optional: Different amounts for different document types
        // EU ID: 2x bonus, Passport: 1.5x bonus
    }
}
```

## Frontend Integration (V2)
```typescript
import { SelfAppBuilder } from '@selfxyz/qrcode';
import { v4 as uuidv4 } from 'uuid';

const airdropQR = new SelfAppBuilder({
  appName: 'Token Airdrop',
  scope: 'airdrop-2024',
  endpoint: '/api/verify-and-claim',
  userId: uuidv4(),
  version: 2, // V2 protocol
  userDefinedData: Buffer.from(JSON.stringify({
    action: 'airdrop_claim',
    amount: '100'
  })).toString('hex').padEnd(128, '0'),
  disclosures: {
    minimumAge: 18,
    excludedCountries: ['IRN', 'PRK', 'CUB'], // Sanctions compliance
    ofac: true
  }
}).build();
```

## Backend Verification (V2)
```typescript
import { 
  SelfBackendVerifier, 
  AllIds, 
  UserIdType,
  DefaultConfigStore 
} from '@selfxyz/core';

class AirdropConfigStorage {
  async getConfig(configId: string) {
    return {
      olderThan: 18,
      excludedCountries: ['IRN', 'PRK', 'CUB'],
      ofac: true
    };
  }
  
  async getActionId(userIdentifier: string, userDefinedData: string) {
    return 'airdrop_config';
  }
}

const verifier = new SelfBackendVerifier(
  'airdrop-2024',
  'https://myapi.com/verify-and-claim',
  false, // Production mode
  AllIds, // Accept all document types
  new AirdropConfigStorage(),
  UserIdType.UUID
);

app.post('/api/verify-and-claim', async (req, res) => {
  const { attestationId, proof, pubSignals, userContextData } = req.body;
  const result = await verifier.verify(attestationId, proof, pubSignals, userContextData);
  
  if (result.isValidDetails.isValid) {
    // Store nullifier to prevent double claims
    await db.nullifiers.create({ 
      nullifier: result.discloseOutput.nullifier,
      userIdentifier: result.userData.userIdentifier,
      attestationId: result.discloseOutput.attestationId,
      claimedAt: new Date()
    });
    
    // Trigger on-chain claim or off-chain distribution
    res.json({ 
      success: true, 
      txHash: '...',
      verificationId: result.discloseOutput.nullifier 
    });
  }
});
```
""",
    "age-gate": """# Age Verification Example (V2)

## Frontend Implementation (V2)
```typescript
import { SelfAppBuilder } from '@selfxyz/qrcode';
import { v4 as uuidv4 } from 'uuid';

const ageVerificationQR = new SelfAppBuilder({
  appName: 'Adult Content Platform',
  scope: 'age-verification-app',
  endpoint: '/api/verify-age',
  userId: uuidv4(),
  version: 2, // V2 protocol
  userDefinedData: Buffer.from(JSON.stringify({
    action: 'age_verification',
    required_age: 21,
    platform: 'adult_content'
  })).toString('hex').padEnd(128, '0'),
  disclosures: {
    minimumAge: 21, // Must match backend exactly
    nationality: false, // Don't reveal nationality for privacy
    name: false // Don't reveal name for privacy
  }
}).build();
```

## Backend Implementation (V2)
```typescript
import { 
  SelfBackendVerifier, 
  AllIds, 
  UserIdType,
  IConfigStorage 
} from '@selfxyz/core';

class AgeVerificationConfigStorage implements IConfigStorage {
  async getConfig(configId: string) {
    return {
      olderThan: 21, // Must match frontend minimumAge
      excludedCountries: [], // Optional for age-only checks
      ofac: false // Optional for age-only checks
    };
  }
  
  async getActionId(userIdentifier: string, userDefinedData: string) {
    const context = JSON.parse(userDefinedData);
    return `age_verification_${context.required_age}`;
  }
}

const verifier = new SelfBackendVerifier(
  'age-verification-app',
  'https://myapi.com/verify-age',
  false, // Production mode
  AllIds, // Accept all document types
  new AgeVerificationConfigStorage(),
  UserIdType.UUID
);

app.post('/api/verify-age', async (req, res) => {
  const { attestationId, proof, pubSignals, userContextData } = req.body;
  const result = await verifier.verify(attestationId, proof, pubSignals, userContextData);
  
  if (result.isValidDetails.isValid && result.isValidDetails.isOlderThanValid) {
    // Create session
    req.session.ageVerified = true;
    req.session.userId = result.userData.userIdentifier;
    req.session.nullifier = result.discloseOutput.nullifier;
    req.session.documentType = result.discloseOutput.attestationId;
    
    res.json({ 
      verified: true,
      ageProof: result.discloseOutput.olderThan,
      documentType: result.discloseOutput.attestationId === 1 ? 'passport' : 'eu_id'
    });
  } else {
    res.status(400).json({ 
      verified: false,
      error: 'Age verification failed',
      details: result.isValidDetails
    });
  }
});
```

## Smart Contract for Age-Gated Actions (V2)
```solidity
pragma solidity ^0.8.0;
import "@selfxyz/contracts/contracts/abstract/SelfVerificationRoot.sol";

contract AgeGatedPlatform is SelfVerificationRoot {
    mapping(uint256 => bool) public verifiedUsers;
    mapping(uint256 => uint256) public userAges;
    bytes32 public configId;
    
    constructor(address _hub, uint256 _scope) SelfVerificationRoot(_hub, _scope) {
        configId = 0x...; // Your config ID for 21+ requirement
    }
    
    function getConfigId(...) public view override returns (bytes32) {
        return configId;
    }
    
    function verifyAge(SelfStructs.SelfProof memory proof, bytes memory userData) external {
        verifySelfProof(proof, userData);
        require(!verifiedUsers[proof.nullifier], "Already verified");
        
        verifiedUsers[proof.nullifier] = true;
    }
    
    function customVerificationHook(
        ISelfVerificationRoot.GenericDiscloseOutputV2 memory output,
        bytes memory userData
    ) internal virtual override {
        // Store age proof result
        userAges[output.nullifier] = output.olderThan;
        require(output.olderThan >= 21, "Must be 21 or older");
    }
    
    modifier onlyAgeVerified(uint256 nullifier) {
        require(verifiedUsers[nullifier] && userAges[nullifier] >= 21, "Age verification required");
        _;
    }
    
    function accessAdultContent(uint256 nullifier) external onlyAgeVerified(nullifier) {
        // Age-restricted functionality
    }
}
```
"""
}