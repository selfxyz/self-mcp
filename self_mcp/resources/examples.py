"""Resource for Self protocol example code"""

from ..templates import EXAMPLES


async def get_example_code(example_type: str) -> str:
    """Get complete example implementations"""
    return EXAMPLES.get(example_type, "Example not found. Available: airdrop, age-gate")