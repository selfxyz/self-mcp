"""Resource for Self protocol best practices"""

from ..utils.github_client import get_docs_client


async def get_best_practices() -> str:
    """Get Self protocol integration best practices"""
    client = get_docs_client()
    
    # Try to fetch best practices from docs
    content = await client.fetch_document("best-practices/README.md")
    if not content:
        # Try alternative paths
        content = await client.fetch_document("integration/best-practices.md")
    
    if content:
        return f"# Self Protocol Best Practices\n\n{content}"
    
    # Fallback to essential best practices
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
1. **Cache configurations** - Reduce repeated API calls
2. **Batch verifications** - Process multiple proofs efficiently
3. **Set appropriate timeouts** - Handle slow network conditions
4. **Implement retry logic** - Handle transient failures

## User Experience
1. **Clear instructions** - Explain why verification is needed
2. **Mobile-friendly QR codes** - Ensure proper sizing
3. **Progress indicators** - Show verification status
4. **Error messages** - Provide helpful troubleshooting

## Testing
1. **Use mock passports** - Set `isMock: true` in development
2. **Test edge cases** - Invalid proofs, expired proofs, network errors
3. **Multi-device testing** - Test QR scanning on various devices
4. **Load testing** - Ensure system handles concurrent verifications"""