"""Self MCP Server - Clean architecture implementation"""

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

# Core tools
from .tools import (
    explain_self_integration,
    generate_verification_code,
    debug_verification_error,
    check_self_status,
    generate_verification_config,
    explain_sdk_setup,
    generate_eu_id_verification,
)

# Documentation tools
from .tools.dynamic_docs import (
    fetch_self_docs,
    list_docs_topics,
    search_docs,
)

# Contract interaction tools
from .tools.contract_interaction import (
    generate_scope_hash,
    generate_config_id,
    read_hub_config,
    list_country_codes,
    guide_to_tools,
)

# Resources and prompts
from .resources import (
    get_contract_addresses,
    get_example_code,
    get_best_practices,
)

from .prompts import (
    design_verification_flow,
    troubleshoot_integration,
)

# Create an MCP server
mcp = FastMCP("Self-MCP")

# Register tools with annotations for better LLM understanding
mcp.tool(
    annotations=ToolAnnotations(
        title="Use this first to understand Self protocol integration",
        readOnlyHint=True
    )
)(explain_self_integration)

mcp.tool(
    annotations=ToolAnnotations(
        title="Generate ready-to-use code after understanding the integration",
        readOnlyHint=True
    )
)(generate_verification_code)

mcp.tool(
    annotations=ToolAnnotations(
        title="Debug Self verification errors with solutions",
        readOnlyHint=True
    )
)(debug_verification_error)

mcp.tool(
    annotations=ToolAnnotations(
        title="Check Self protocol network status and contracts",
        readOnlyHint=True
    )
)(check_self_status)

mcp.tool(
    annotations=ToolAnnotations(
        title="Generate complete verification configuration",
        readOnlyHint=True
    )
)(generate_verification_config)

mcp.tool(
    annotations=ToolAnnotations(
        title="Explain Self SDK setup requirements (IConfigStorage, UserIdType, etc.)",
        readOnlyHint=True
    )
)(explain_sdk_setup)

mcp.tool(
    annotations=ToolAnnotations(
        title="Generate EU ID card verification code (V2 feature)",
        readOnlyHint=True
    )
)(generate_eu_id_verification)

# Register dynamic documentation tools
mcp.tool(
    annotations=ToolAnnotations(
        title="Fetch latest Self protocol documentation from GitHub",
        readOnlyHint=True
    )
)(fetch_self_docs)

mcp.tool(
    annotations=ToolAnnotations(
        title="List all available documentation topics",
        readOnlyHint=True
    )
)(list_docs_topics)

mcp.tool(
    annotations=ToolAnnotations(
        title="Search through Self protocol documentation",
        readOnlyHint=True
    )
)(search_docs)

# Register contract interaction tools
mcp.tool(
    annotations=ToolAnnotations(
        title="Generate scope hash for Self verification (like tools.self.xyz)",
        readOnlyHint=True
    )
)(generate_scope_hash)

mcp.tool(
    annotations=ToolAnnotations(
        title="Generate a configuration ID for Self protocol verification",
        readOnlyHint=True
    )
)(generate_config_id)

mcp.tool(
    annotations=ToolAnnotations(
        title="Read configuration from Self protocol Hub contract",
        readOnlyHint=True
    )
)(read_hub_config)

mcp.tool(
    annotations=ToolAnnotations(
        title="Guide users to appropriate tools.self.xyz features",
        readOnlyHint=True
    )
)(guide_to_tools)

mcp.tool(
    annotations=ToolAnnotations(
        title="List available country codes for Self protocol exclusions",
        readOnlyHint=True
    )
)(list_country_codes)

# Register resources
mcp.resource("self://contracts/addresses")(get_contract_addresses)
mcp.resource("self://examples/{example_type}")(get_example_code)
mcp.resource("self://docs/best-practices")(get_best_practices)

# Register prompts
mcp.prompt("design-verification-flow")(design_verification_flow)
mcp.prompt("troubleshoot-integration")(troubleshoot_integration)


def run():
    """Run the MCP server"""
    mcp.run()


if __name__ == "__main__":
    run()