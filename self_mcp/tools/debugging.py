"""Tool for debugging Self protocol verification errors"""

from typing import Literal, Optional

from ..utils.github_client import get_docs_client


async def debug_verification_error(
    error_message: str,
    context: Literal[
        "", "scope-mismatch", "proof-invalid", "age-verification", 
        "nullifier-reuse", "network-error", "config-mismatch"
    ] = "",
) -> str:
    """
    Diagnose Self verification errors and provide solutions.
    
    Args:
        error_message: The error message you're encountering
        context: Optional hint about the error type
        
    Returns:
        Detailed explanation of the problem and how to fix it
    """
    client = get_docs_client()
    error_lower = error_message.lower()
    
    # Try to fetch troubleshooting docs
    troubleshooting = await client.fetch_document("support/troubleshooting.md")
    
    if troubleshooting:
        # Search for the error in docs
        solution = find_error_solution(troubleshooting, error_message, context)
        if solution:
            return solution
    
    # Fallback to basic error analysis
    return analyze_error_fallback(error_message, context)


def find_error_solution(content: str, error_message: str, context: str) -> str:
    """Find error solution in troubleshooting documentation"""
    lines = content.split('\n')
    error_lower = error_message.lower()
    
    # Keywords to search for based on error/context
    search_terms = []
    if context:
        search_terms.append(context.replace('-', ' '))
    
    # Extract keywords from error message
    error_keywords = {
        "scope": ["scope", "mismatch"],
        "proof": ["proof", "invalid", "verification failed"],
        "age": ["age", "older", "minimum age"],
        "nullifier": ["nullifier", "reuse", "duplicate"],
        "network": ["network", "connection", "timeout"],
        "config": ["config", "mismatch", "configuration"]
    }
    
    for key, keywords in error_keywords.items():
        if any(kw in error_lower for kw in keywords):
            search_terms.extend(keywords)
    
    # Find relevant sections
    relevant_sections = []
    current_section = []
    section_relevance = 0
    
    for line in lines:
        if line.startswith('#'):
            # New section
            if current_section and section_relevance > 0:
                relevant_sections.append(('\n'.join(current_section), section_relevance))
            current_section = [line]
            section_relevance = sum(1 for term in search_terms if term in line.lower())
        else:
            current_section.append(line)
            if any(term in line.lower() for term in search_terms):
                section_relevance += 1
    
    # Add last section
    if current_section and section_relevance > 0:
        relevant_sections.append(('\n'.join(current_section), section_relevance))
    
    # Sort by relevance and return top section
    if relevant_sections:
        relevant_sections.sort(key=lambda x: x[1], reverse=True)
        return f"# Error Analysis\n\nError: {error_message}\n\n{relevant_sections[0][0]}"
    
    return None


def analyze_error_fallback(error_message: str, context: str) -> str:
    """Provide basic error analysis when docs aren't available"""
    error_lower = error_message.lower()
    
    # Common error patterns and solutions
    if "scope" in error_lower or context == "scope-mismatch":
        return """# Scope Mismatch Error

**Problem**: The scope used in frontend doesn't match the backend scope.

**Solution**:
1. Ensure both frontend and backend use the exact same scope string
2. Scope should be <= 25 characters, alphanumeric only
3. Common pattern: "appname-environment" (e.g., "myapp-prod")

**Example Fix**:
```typescript
// Frontend
const selfApp = new SelfAppBuilder({
  scope: "myapp-prod", // Must match backend exactly
  ...
}).build();

// Backend
const verifier = new SelfBackendVerifier(
  "myapp-prod", // Same scope as frontend
  ...
);
```"""
    
    elif "proof" in error_lower or "invalid" in error_lower or context == "proof-invalid":
        return """# Invalid Proof Error

**Problem**: The zero-knowledge proof verification failed.

**Common Causes**:
1. Proof expired (older than 30 minutes)
2. Network mismatch (testnet proof on mainnet)
3. Mock passport used in production
4. Corrupted proof data during transmission

**Solutions**:
- Ensure proof is fresh (< 30 minutes old)
- Match network environments
- Use `isMock: false` for production
- Check JSON parsing of proof data"""
    
    elif "age" in error_lower or context == "age-verification":
        return """# Age Verification Error

**Problem**: User doesn't meet age requirements.

**Valid Age Range**: 10-100 years
- Minimum: 10 years old
- Maximum: 100 years old

**Solution**:
```typescript
// Frontend disclosures
disclosures: {
  minimumAge: 18, // Must be between 10-100
  ...
}

// Backend configuration
async getConfig(configId) {
  return {
    olderThan: 18, // Must match frontend
    ...
  };
}
```"""
    
    elif "nullifier" in error_lower or context == "nullifier-reuse":
        return """# Nullifier Reuse Error

**Problem**: This proof has already been used.

**Explanation**: Nullifiers prevent proof reuse. Each proof can only be used once per scope.

**Solutions**:
1. User needs to generate a new proof
2. For testing, use different scopes
3. Implement proper nullifier storage:

```typescript
// Store nullifiers to prevent reuse
const usedNullifiers = new Set();

function verifyProof(proof, nullifier) {
  if (usedNullifiers.has(nullifier)) {
    throw new Error("Proof already used");
  }
  // Verify proof...
  usedNullifiers.add(nullifier);
}
```"""
    
    elif "network" in error_lower or "timeout" in error_lower or context == "network-error":
        return """# Network/Connection Error

**Problem**: Cannot connect to Self protocol services.

**Common Causes**:
1. Wrong RPC URL
2. Network congestion
3. Firewall blocking requests
4. Invalid endpoint URL

**Solutions**:
- Use correct RPC URLs:
  - Mainnet: https://forno.celo.org
  - Testnet: https://alfajores-forno.celo-testnet.org
- Ensure endpoint is publicly accessible
- Check firewall/proxy settings
- Add timeout handling"""
    
    elif "config" in error_lower or context == "config-mismatch":
        return """# Configuration Mismatch Error

**Problem**: Frontend and backend configurations don't match.

**Requirements**: The following must match exactly:
- `minimumAge` / `olderThan`
- `excludedCountries`
- `ofac` settings

**Example Fix**:
```typescript
// Frontend
disclosures: {
  minimumAge: 18,
  excludedCountries: ['IRN', 'PRK'],
  ofac: true
}

// Backend IConfigStorage
async getConfig(configId) {
  return {
    olderThan: 18,          // Must match minimumAge
    excludedCountries: ['IRN', 'PRK'], // Must match exactly
    ofac: true              // Must match
  };
}
```"""
    
    else:
        return f"""# Error Analysis

**Error Message**: {error_message}

**General Debugging Steps**:

1. **Check Console Logs**: Look for detailed error messages in browser and server logs

2. **Verify Configuration**:
   - Frontend and backend scopes match exactly
   - All verification requirements align
   - Network settings are correct

3. **Test with Mock Passports**:
   - Set `isMock: true` in development
   - Use test passports to isolate issues

4. **Common Issues**:
   - Expired proofs (> 30 minutes)
   - Network mismatches
   - Configuration differences
   - CORS errors on endpoints

5. **Get Help**:
   - Check Self protocol documentation
   - Join the Telegram community
   - Review example implementations

**Debug Checklist**:
- [ ] Scopes match exactly (frontend/backend)
- [ ] Using correct network (mainnet/testnet)
- [ ] Proof is fresh (< 30 minutes)
- [ ] Endpoint is publicly accessible
- [ ] Configurations are aligned
- [ ] Error logs checked on both sides"""