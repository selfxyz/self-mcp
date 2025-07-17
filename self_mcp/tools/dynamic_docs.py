"""Dynamic documentation fetching from Self protocol GitHub repository"""

from typing import Optional, Dict, Annotated
from pydantic import Field
from ..utils.github_client import get_docs_client


# Topic mapping to file paths in the self-docs repository
TOPIC_MAP = {
    # Getting started
    "quickstart": "use-self/quickstart.md",
    "overview": "README.md",
    "disclosures": "use-self/disclosures.md",
    "deeplinking": "use-self/use-deeplinking.md",
    "mock-passports": "use-self/using-mock-passports.md",

    # SDK Reference
    "backend-sdk": "sdk-reference/selfbackendverifier.md",
    "frontend-sdk": "sdk-reference/selfqrcodewrapper.md",
    "self-app-builder": "sdk-reference/selfappbuilder.md",

    # Contract Integration
    "contracts": "contract-integration/basic-integration.md",
    "deployed-contracts": "contract-integration/deployed-contracts.md",
    "airdrop-example": "contract-integration/airdrop-example.md",
    "happy-birthday-example": "contract-integration/happy-birthday-example.md",
    "passport-attributes": "contract-integration/utilize-passport-attributes.md",
    "frontend-configuration": "contract-integration/frontend-configuration.md",
}


async def fetch_self_docs(
    topic: Annotated[str, Field(
        description="Documentation topic to fetch. Options: " + ", ".join(TOPIC_MAP.keys())
    )],
    section: Annotated[Optional[str], Field(
        description="Specific section within the document (e.g., 'Installation', 'Configuration')"
    )] = None
) -> str:
    """
    Fetch latest Self protocol documentation from GitHub.
    
    This tool retrieves up-to-date documentation directly from the Self protocol
    documentation repository, ensuring you always have the latest information.
    
    Available topics:
    - quickstart: Getting started guide
    - backend-sdk: Backend SDK reference
    - frontend-sdk: Frontend QR code SDK reference
    - contracts: Smart contract integration
    - configuration: Verification configuration guide
    - testing: Mock passport testing
    - troubleshooting: Common issues and solutions
    """
    
    # Validate topic
    if topic not in TOPIC_MAP:
        available_topics = "\n".join([f"- {k}: {v}" for k, v in TOPIC_MAP.items()])
        return f"Unknown topic '{topic}'. Available topics:\n{available_topics}"
    
    # Get the file path
    file_path = TOPIC_MAP[topic]
    
    # Fetch from GitHub
    client = get_docs_client()
    content = await client.fetch_document(file_path)
    
    if content is None:
        return f"Failed to fetch documentation for topic '{topic}'. The document may have been moved or removed."
    
    # If section is specified, try to extract it
    if section:
        section_content = extract_section(content, section)
        if section_content:
            return f"# {topic.replace('-', ' ').title()} - {section}\n\n{section_content}"
        else:
            return f"Section '{section}' not found in {topic} documentation.\n\nHere's the full document:\n\n{content}"
    
    return f"# {topic.replace('-', ' ').title()}\n\n{content}"


def extract_section(content: str, section: str) -> Optional[str]:
    """Extract a specific section from markdown content"""
    lines = content.split('\n')
    section_lower = section.lower()
    
    # Find section start
    start_idx = None
    section_level = None
    
    for i, line in enumerate(lines):
        if line.startswith('#'):
            # Extract header level and text
            header = line.lstrip('#').strip()
            if header.lower() == section_lower or section_lower in header.lower():
                start_idx = i
                section_level = len(line) - len(line.lstrip('#'))
                break
    
    if start_idx is None:
        return None
    
    # Find section end (next header of same or higher level)
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        line = lines[i]
        if line.startswith('#'):
            current_level = len(line) - len(line.lstrip('#'))
            if current_level <= section_level:
                end_idx = i
                break
    
    # Extract section content
    section_lines = lines[start_idx:end_idx]
    
    # Remove trailing empty lines
    while section_lines and not section_lines[-1].strip():
        section_lines.pop()
    
    return '\n'.join(section_lines)


async def list_docs_topics() -> str:
    """
    List all available documentation topics and their descriptions.
    
    This tool shows you all the documentation topics you can fetch
    with the fetch_self_docs tool.
    """
    
    topics = []
    for topic, path in TOPIC_MAP.items():
        # Extract category from path
        category = path.split('/')[0].replace('-', ' ').title()
        topics.append(f"- **{topic}** ({category}): {path}")
    
    return "# Available Documentation Topics\n\n" + "\n".join(topics)


async def search_docs(
    query: Annotated[str, Field(description="Search query to find in documentation")],
    max_results: Annotated[int, Field(description="Maximum number of results to return")] = 5
) -> str:
    """
    Search through Self protocol documentation for specific terms.
    
    This tool searches across all documentation files to find
    relevant information about your query.
    """
    
    client = get_docs_client()
    results = []
    
    # Search through all known documents
    for topic, path in TOPIC_MAP.items():
        content = await client.fetch_document(path)
        if content and query.lower() in content.lower():
            # Find matching lines
            lines = content.split('\n')
            matches = []
            
            for i, line in enumerate(lines):
                if query.lower() in line.lower():
                    # Get context (2 lines before and after)
                    start = max(0, i - 2)
                    end = min(len(lines), i + 3)
                    context = '\n'.join(lines[start:end])
                    matches.append(context)
            
            if matches:
                results.append({
                    'topic': topic,
                    'path': path,
                    'matches': matches[:2]  # Limit matches per document
                })
        
        if len(results) >= max_results:
            break
    
    if not results:
        return f"No results found for '{query}' in the documentation."
    
    # Format results
    output = f"# Search Results for '{query}'\n\n"
    for result in results:
        output += f"## {result['topic'].replace('-', ' ').title()}\n"
        output += f"*File: {result['path']}*\n\n"
        for match in result['matches']:
            output += f"```\n{match}\n```\n\n"
    
    return output