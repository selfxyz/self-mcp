"""Prompt for troubleshooting Self integration issues"""


async def troubleshoot_integration(
    error_description: str,
    code_snippet: str = ""
) -> str:
    """Interactive troubleshooting for Self integration issues"""
    return f"""I'll help troubleshoot your Self integration issue.

Error: {error_description}

{f'Code: {code_snippet}' if code_snippet else ''}

Let me analyze this step by step:
1. First, let's verify your configuration
2. Check common issues
3. Test each component

Can you also provide:
- Your frontend scope value
- Backend scope value  
- Any console errors?"""