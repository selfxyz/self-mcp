"""Tool for explaining Self protocol integration"""

from typing import Literal
from ..templates import USE_CASE_GUIDES


async def explain_self_integration(
    use_case: Literal["airdrop", "age-verification", "humanity-check"]
) -> str:
    """
    Explain how to integrate Self for a specific use case with step-by-step guidance.
    
    Args:
        use_case: The integration scenario - 'airdrop', 'age-verification', or 'humanity-check'
        
    Returns:
        Detailed explanation with steps and code examples
    """
    if use_case not in USE_CASE_GUIDES:
        return f"Unknown use case: {use_case}. Available options: airdrop, age-verification, humanity-check"
    
    return USE_CASE_GUIDES[use_case]