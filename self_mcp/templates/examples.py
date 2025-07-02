"""Complete example implementations for Self protocol"""

EXAMPLES = {
    "airdrop": """# Complete Airdrop Example

## Smart Contract
```solidity
pragma solidity ^0.8.0;
import "@selfxyz/contracts/contracts/abstract/SelfVerificationRoot.sol";

contract PassportAirdrop is SelfVerificationRoot {
    mapping(uint256 => bool) public claimed;
    uint256 public constant AIRDROP_AMOUNT = 100 * 10**18;
    
    constructor(address _hub) SelfVerificationRoot(_hub) {}
    
    function claim(SelfProof memory proof) external {
        verifySelfProof(proof);
        require(!claimed[proof.nullifier], "Already claimed");
        require(proof.attestationId == 1, "Must be passport");
        
        claimed[proof.nullifier] = true;
        payable(msg.sender).transfer(AIRDROP_AMOUNT);
    }
}
```

## Frontend Integration
```typescript
import { SelfAppBuilder } from '@selfxyz/qrcode';

const airdropQR = new SelfAppBuilder({
  appName: 'Token Airdrop',
  scope: 'airdrop-2024',
  endpoint: '/api/verify-and-claim',
  disclosures: {
    // Only need to verify humanity
  }
}).build();
```

## Backend Verification
```typescript
import { SelfBackendVerifier } from '@selfxyz/core';

const verifier = new SelfBackendVerifier(
  process.env.CELO_RPC,
  'airdrop-2024'
);

app.post('/api/verify-and-claim', async (req, res) => {
  const { proof, publicSignals } = req.body;
  const result = await verifier.verify(proof, publicSignals);
  
  if (result.isValid) {
    // Store nullifier to prevent double claims
    await db.nullifiers.create({ 
      nullifier: result.nullifier,
      claimedAt: new Date()
    });
    
    // Trigger on-chain claim or off-chain distribution
    res.json({ success: true, txHash: '...' });
  }
});
```
""",
    "age-gate": """# Age Verification Example

## Implementation
```typescript
// Frontend
const ageVerificationQR = new SelfAppBuilder({
  appName: 'Adult Content Platform',
  scope: 'age-verification-app',
  endpoint: '/api/verify-age',
  disclosures: {
    minimumAge: 21 // Required age
  }
}).build();

// Backend
const verifier = new SelfBackendVerifier(rpcUrl, 'age-verification-app');
verifier.setMinimumAge(21);

app.post('/api/verify-age', async (req, res) => {
  const result = await verifier.verify(proof, publicSignals);
  
  if (result.isValid && result.credentialSubject.older_than >= 21) {
    // Create session
    req.session.ageVerified = true;
    req.session.userId = result.userId;
    res.json({ verified: true });
  }
});
```
"""
}