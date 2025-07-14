"""Resource for Self protocol example code"""

from ..utils.github_client import get_docs_client


async def get_example_code(example_type: str) -> str:
    """Get complete example implementations"""
    client = get_docs_client()
    
    # Map example types to documentation files
    example_map = {
        "airdrop": "use-cases/airdrop.md",
        "age-gate": "use-cases/age-verification.md"
    }
    
    doc_path = example_map.get(example_type)
    if not doc_path:
        return "Example not found. Available: airdrop, age-gate"
    
    content = await client.fetch_document(doc_path)
    if content:
        return f"# Example: {example_type.replace('-', ' ').title()}\n\n{content}"
    
    # Fallback
    return f"Failed to fetch example for {example_type}. Please check documentation."