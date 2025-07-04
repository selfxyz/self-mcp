"""Common error solutions for Self protocol integration"""

ERROR_SOLUTIONS = {
    "scope": {
        "problem": "Scope mismatch between frontend and backend",
        "solution": """
The 'scope' parameter must match EXACTLY between frontend and backend (V2):

**Frontend (QR code):**
```typescript
new SelfAppBuilder({
  scope: 'my-app-v2', // This exact string
  version: 2, // V2 protocol
  ...
})
```

**Backend (verifier V2):**
```typescript
new SelfBackendVerifier(
  'my-app-v2', // Must be identical to frontend scope
  'https://myapi.com/verify', // Endpoint URL
  false, // Production mode
  allowedIds, // Allowed document types
  configStorage, // V2 IConfigStorage implementation
  UserIdType.UUID // User identifier type
)
```

Common mistakes:
- Extra spaces or typos
- Different versions (v1 vs v2)
- Using URLs as scope (use simple strings instead)
- Wrong constructor parameter order in V2
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
Age verification requirements (V2):

1. **Frontend disclosures must match backend config:**
```typescript
// Frontend
new SelfAppBuilder({
  disclosures: {
    minimumAge: 18 // Must match backend exactly
  }
})

// Backend IConfigStorage
async getConfig(configId: string) {
  return {
    olderThan: 18, // Must match frontend minimumAge
    excludedCountries: [],
    ofac: false
  };
}
```

2. **Valid age range: 10-100 years**
```typescript
olderThan: 18, // ✓ Valid
olderThan: 5,  // ✗ Too low  
olderThan: 150 // ✗ Too high
```

3. **Check V2 age verification result:**
```typescript
if (result.isValidDetails.isValid && result.isValidDetails.isOlderThanValid) {
  // Age verification passed
  const ageProof = result.discloseOutput.olderThan; // Actual age proof
}
```

4. **Common V2 configuration errors:**
- Frontend minimumAge ≠ backend olderThan
- Missing IConfigStorage implementation
- ConfigMismatchError due to disclosure mismatch
""",
        "related": ["Invalid age", "minimumAge must be between", "Age verification failed", "ConfigMismatchError"]
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
// Celo Mainnet
'https://forno.celo.org'
// Chain ID: 42220

// Celo Alfajores Testnet
'https://alfajores-forno.celo-testnet.org'
// Chain ID: 44787
```

**Check connectivity:**
```bash
# Mainnet
curl https://forno.celo.org -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

# Testnet
curl https://alfajores-forno.celo-testnet.org -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

**Common issues:**
- Firewall blocking RPC
- Using Ethereum RPC instead of Celo
- Rate limiting on free tier
""",
        "related": ["Network error", "RPC", "Connection failed", "Celo"]
    },
    "config": {
        "problem": "V2 Configuration mismatch between frontend and backend",
        "solution": """
V2 introduces ConfigMismatchError when frontend disclosures don't match backend configuration:

**Frontend disclosures must exactly match backend IConfigStorage:**

```typescript
// Frontend
new SelfAppBuilder({
  disclosures: {
    minimumAge: 18,
    excludedCountries: ['IRN', 'PRK'],
    ofac: true,
    nationality: true,
    name: false
  }
})

// Backend IConfigStorage - MUST MATCH
class MyConfigStorage implements IConfigStorage {
  async getConfig(configId: string) {
    return {
      olderThan: 18, // = minimumAge
      excludedCountries: ['IRN', 'PRK'], // = excludedCountries
      ofac: true, // = ofac
      // nationality: true (implied by frontend request)
      // name: false (not requested in frontend)
    };
  }
}
```

**Common mismatches:**
- Different age requirements (minimumAge ≠ olderThan)
- Different excluded countries arrays
- Different OFAC settings (true vs false)
- Requesting fields in frontend but not configuring in backend
- Missing IConfigStorage implementation

**Debug ConfigMismatchError:**
```typescript
try {
  const result = await verifier.verify(attestationId, proof, pubSignals, userContextData);
} catch (error) {
  if (error instanceof ConfigMismatchError) {
    console.log('Configuration issues:', error.issues);
    // Fix frontend disclosures or backend config based on error.issues
  }
}
```

**Use Configuration Tools:**
- Visit https://tools.self.xyz/ to generate matching configurations
- Ensure both frontend and backend use the same config ID
""",
        "related": ["ConfigMismatchError", "Configuration mismatch", "Disclosure mismatch", "IConfigStorage"]
    }
}