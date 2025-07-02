"""Resource for Self protocol best practices"""


async def get_best_practices() -> str:
    """Get Self protocol integration best practices"""
    return """# Self Protocol Best Practices

## Security
1. **Never trust client-side verification alone** - Always verify proofs on backend
2. **Store nullifiers** - Prevent proof reuse by tracking nullifiers
3. **Use HTTPS** - Protect proof transmission
4. **Validate scope** - Ensure frontend and backend scopes match exactly

## Privacy
1. **Minimize data collection** - Only request necessary attributes
2. **Don't log personal data** - Avoid logging revealed attributes
3. **Use nullifiers as IDs** - Don't create mappings to real identities
4. **Clear sessions** - Remove verification data after use

## Performance
1. **Cache verification results** - Reduce RPC calls
2. **Batch verifications** - Process multiple proofs together
3. **Use WebSockets** - For real-time verification status
4. **Optimize RPC** - Use reliable Celo RPC endpoints

## User Experience
1. **Clear instructions** - Explain why passport verification is needed
2. **Fallback options** - Provide alternatives if verification fails
3. **Progress feedback** - Show verification status
4. **Error handling** - Friendly messages for common issues
"""