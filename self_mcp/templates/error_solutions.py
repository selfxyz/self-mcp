"""Common error solutions for Self protocol integration"""

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
verifier.setMinimumAge(18); // ✓ Valid
verifier.setMinimumAge(5);  // ✗ Too low
verifier.setMinimumAge(150); // ✗ Too high
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
    }
}