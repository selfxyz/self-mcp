"""Prompt for designing Self verification flows"""


async def design_verification_flow(
    use_case: str,
    requirements: str
) -> str:
    """Help design a custom Self verification flow"""
    return f"""I'll help you design a Self verification flow for {use_case}.

Requirements: {requirements}

Let's consider:
1. What attributes need to be verified?
2. Should verification happen on-chain or off-chain?
3. How will you prevent sybil attacks?
4. What's the user journey?

Please provide more details about your specific needs."""