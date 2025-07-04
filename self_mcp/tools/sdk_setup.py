"""Tool for explaining Self SDK setup requirements"""

from typing import Literal
from fastmcp import Context


async def explain_sdk_setup(
    topic: Literal["config-storage", "user-id-type", "attestation-ids", "full-setup"],
    ctx: Context = None
) -> str:
    """
    Explain Self SDK backend setup requirements and configuration.
    
    Args:
        topic: What to explain - 'config-storage', 'user-id-type', 'attestation-ids', or 'full-setup'
        ctx: FastMCP context for logging
        
    Returns:
        Detailed explanation with code examples
    """
    
    if ctx:
        await ctx.info(f"Explaining Self SDK setup for {topic}")
    
    if topic == "config-storage":
        return """# IConfigStorage Implementation

The Self SDK requires an IConfigStorage implementation to cache verification configurations.

## Why is it needed?
- Caches verification configs to avoid repeated blockchain calls
- Stores circuit verifier addresses
- Improves performance significantly

## Simple Implementation:
```typescript
import { IConfigStorage } from '@selfxyz/core';

class SimpleConfigStorage implements IConfigStorage {
  private configs = new Map<string, any>();
  
  async getConfig(configId: string): Promise<any> {
    return this.configs.get(configId);
  }
  
  async setConfig(configId: string, config: any): Promise<void> {
    this.configs.set(configId, config);
  }
}
```

## Production Implementation (with Redis):
```typescript
import { IConfigStorage } from '@selfxyz/core';
import Redis from 'ioredis';

class RedisConfigStorage implements IConfigStorage {
  private redis: Redis;
  
  constructor() {
    this.redis = new Redis({
      host: process.env.REDIS_HOST,
      port: parseInt(process.env.REDIS_PORT || '6379'),
    });
  }
  
  async getConfig(configId: string): Promise<any> {
    const data = await this.redis.get(`self:config:${configId}`);
    return data ? JSON.parse(data) : null;
  }
  
  async setConfig(configId: string, config: any): Promise<void> {
    await this.redis.set(
      `self:config:${configId}`,
      JSON.stringify(config),
      'EX',
      3600 // Cache for 1 hour
    );
  }
}
```

## Usage:
```typescript
const configStorage = new SimpleConfigStorage(); // or RedisConfigStorage
const verifier = new SelfBackendVerifier(
  'my-scope',
  'https://api.self.xyz/v1',
  false,
  allowedIds,
  configStorage, // Pass here
  UserIdType.ADDRESS
);
```"""
    
    elif topic == "user-id-type":
        return """# UserIdType Configuration

UserIdType determines how user identifiers are generated from verification proofs.

## Available Types:

### 1. UserIdType.ADDRESS (Default)
- Generates an Ethereum-style address from the proof
- Format: `0x1234...abcd` (20 bytes)
- Use when: You need wallet-like identifiers
- Best for: DeFi, airdrops, on-chain applications

```typescript
import { UserIdType } from '@selfxyz/core';

const verifier = new SelfBackendVerifier(
  'my-scope',
  'https://api.self.xyz/v1',
  false,
  allowedIds,
  configStorage,
  UserIdType.ADDRESS // Ethereum address format
);
```

### 2. UserIdType.UUID
- Generates a UUID v4 format identifier
- Format: `123e4567-e89b-12d3-a456-426614174000`
- Use when: You need standard database UUIDs
- Best for: Traditional web apps, databases

```typescript
const verifier = new SelfBackendVerifier(
  'my-scope',
  'https://api.self.xyz/v1',
  false,
  allowedIds,
  configStorage,
  UserIdType.UUID // UUID format
);
```

## Extracting User ID:
```typescript
import { castToUserIdentifier, UserIdType } from '@selfxyz/core';

// In your verification endpoint
const userId = castToUserIdentifier(
  publicSignals, // Array of bigints
  UserIdType.ADDRESS // Must match verifier config
);

// userId will be either:
// - "0x1234...abcd" for ADDRESS type
// - "123e4567-e89b-12d3-a456-426614174000" for UUID type
```

## Important Notes:
- UserIdType must be consistent between verifier setup and ID extraction
- The same passport always generates the same ID for the same scope
- Different scopes generate different IDs (privacy feature)"""
    
    elif topic == "attestation-ids":
        return """# AttestationId Configuration

AttestationIds define which document types your application accepts.

## Available AttestationIds:

```typescript
import { AttestationId } from '@selfxyz/core';

enum AttestationId {
  E_PASSPORT = 1,    // Electronic passports
  EU_ID_CARD = 3,    // EU identity cards (V2 feature)
}
```

## Configuration:
```typescript
// Accept only passports
const allowedIds = new Map([
  [AttestationId.E_PASSPORT, true]
]);

// Accept both passports and EU ID cards
const allowedIds = new Map([
  [AttestationId.E_PASSPORT, true],
  [AttestationId.EU_ID_CARD, true]
]);

// Pass to verifier
const verifier = new SelfBackendVerifier(
  'my-scope',
  'https://api.self.xyz/v1',
  false,
  allowedIds, // Document types to accept
  configStorage,
  UserIdType.ADDRESS
);
```

## In Verification:
```typescript
// The attestationId comes from the frontend
const { attestationId, proof, publicSignals } = req.body;

// Verify it's an allowed type
if (!allowedIds.has(attestationId)) {
  return res.status(400).json({ 
    error: 'Document type not supported' 
  });
}

// Pass to verify method
const result = await verifier.verify(
  attestationId, // 1 for passport, 3 for EU ID
  proof,
  publicSignals,
  userContextData
);
```

## Document Type Bonuses (Smart Contracts):
```solidity
// Different multipliers for different documents
uint256 constant PASSPORT_MULTIPLIER = 100; // 1x
uint256 constant EU_ID_MULTIPLIER = 150;    // 1.5x

if (proof.attestationId == 1) {
  // Passport verified
  multiplier = PASSPORT_MULTIPLIER;
} else if (proof.attestationId == 3) {
  // EU ID verified  
  multiplier = EU_ID_MULTIPLIER;
}
```"""
    
    else:  # full-setup
        return """# Complete Self SDK Backend Setup

Here's a complete setup guide for the Self SDK backend verifier:

```typescript
import { 
  SelfBackendVerifier,
  AttestationId,
  UserIdType,
  IConfigStorage,
  castToUserIdentifier
} from '@selfxyz/core';

// Step 1: Implement Config Storage
class SimpleConfigStorage implements IConfigStorage {
  private configs = new Map<string, any>();
  
  async getConfig(configId: string): Promise<any> {
    return this.configs.get(configId);
  }
  
  async setConfig(configId: string, config: any): Promise<void> {
    this.configs.set(configId, config);
  }
}

// Step 2: Initialize Verifier
async function initializeVerifier() {
  const configStorage = new SimpleConfigStorage();
  
  // Define allowed document types
  const allowedIds = new Map([
    [AttestationId.E_PASSPORT, true], // Allow passports
    // [AttestationId.EU_ID_CARD, true], // Uncomment for EU IDs
  ]);
  
  // Create verifier instance
  const verifier = new SelfBackendVerifier(
    'my-app-unique-scope',        // Must match frontend exactly
    'https://api.self.xyz/v1',    // Self API endpoint
    false,                        // mockPassport: false for production
    allowedIds,                   // Document types to accept
    configStorage,                // Config caching
    UserIdType.ADDRESS           // or UserIdType.UUID
  );
  
  // Configure verification requirements
  await verifier.setMinimumAge(18); // Optional
  await verifier.excludeCountries(['IRN', 'PRK']); // Optional
  await verifier.enableNameAndDobOfacCheck(); // Optional
  
  return verifier;
}

// Step 3: Create Verification Endpoint
app.post('/api/verify', async (req, res) => {
  try {
    const verifier = await initializeVerifier();
    
    // Extract request data
    const { 
      attestationId,    // 1 for passport, 3 for EU ID
      proof,           // ZK proof object
      publicSignals,   // Array of strings
      userContextData  // Optional context
    } = req.body;
    
    // Convert signals to BigInt
    const pubSignals = publicSignals.map((s: string) => BigInt(s));
    
    // Verify the proof
    const result = await verifier.verify(
      attestationId,
      proof,
      pubSignals,
      userContextData || ''
    );
    
    if (result.isValid) {
      // Extract user ID
      const userId = castToUserIdentifier(
        pubSignals,
        UserIdType.ADDRESS // Must match verifier config
      );
      
      // Store nullifier to prevent reuse
      await storeNullifier(result.nullifier);
      
      // Return success
      res.json({
        success: true,
        userId,
        nullifier: result.nullifier,
        // Only include disclosed data
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
    console.error('Verification error:', error);
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});

// Helper: Store nullifier (implement based on your database)
async function storeNullifier(nullifier: string): Promise<void> {
  // Example with Redis
  await redis.set(`nullifier:${nullifier}`, '1', 'NX');
  
  // Example with PostgreSQL
  // await db.query(
  //   'INSERT INTO nullifiers (value) VALUES ($1) ON CONFLICT DO NOTHING',
  //   [nullifier]
  // );
}
```

## Environment Variables:
```env
# Required
SELF_API_URL=https://api.self.xyz/v1

# Optional (for Redis config storage)
REDIS_HOST=localhost
REDIS_PORT=6379

# Optional (for production)
NODE_ENV=production
```

## Common Mistakes to Avoid:
1. ❌ Mismatched scope between frontend and backend
2. ❌ Not converting publicSignals to BigInt
3. ❌ Forgetting to implement IConfigStorage
4. ❌ Wrong UserIdType when extracting user ID
5. ❌ Not checking attestationId is allowed
6. ❌ Not storing nullifiers to prevent reuse"""
    
    return f"Unknown topic: {topic}"