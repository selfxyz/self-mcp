"""Tool for generating Self protocol integration code"""

from typing import Literal
from fastmcp import Context
from ..templates import CODE_TEMPLATES


async def generate_verification_code(
    component: Literal["frontend-qr", "backend-verify", "smart-contract"],
    language: Literal["typescript", "javascript", "solidity"] = "typescript",
    ctx: Context = None
) -> str:
    """
    Generate ready-to-use Self verification code for different components.
    
    Args:
        component: Which part to generate - 'frontend-qr', 'backend-verify', or 'smart-contract'
        language: Programming language - 'typescript', 'javascript', or 'solidity'
        
    Returns:
        Complete, working code example with comments
    """
    # Validate inputs
    if component not in CODE_TEMPLATES:
        return f"Unknown component: {component}. Available: frontend-qr, backend-verify, smart-contract"
    
    # Handle language compatibility
    if component == "smart-contract" and language != "solidity":
        language = "solidity"  # Force solidity for smart contracts
    elif component != "smart-contract" and language == "solidity":
        language = "typescript"  # Default to typescript for non-contracts
    
    # Check if template exists for language
    if language not in CODE_TEMPLATES[component]:
        available = list(CODE_TEMPLATES[component].keys())
        return f"Language '{language}' not available for {component}. Available: {', '.join(available)}"
    
    # Get template and add context
    template = CODE_TEMPLATES[component][language]
    context_map = {
        "frontend-qr": "Self verification QR code",
        "backend-verify": "Self proof verification", 
        "smart-contract": "on-chain Self verification"
    }
    
    # Log to context if available (FastMCP 2.0 feature)
    if ctx:
        await ctx.info(f"Generated {component} code in {language}")
    
    return template.replace("{component_context}", context_map[component])