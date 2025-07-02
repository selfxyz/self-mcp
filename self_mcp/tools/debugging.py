"""Tool for debugging Self protocol verification errors"""

from typing import Literal
from ..templates import ERROR_SOLUTIONS


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