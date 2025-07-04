"""Self MCP Server - Clean architecture implementation"""

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

# Import all tools
from .tools import (
    explain_self_integration,
    generate_verification_code,
    debug_verification_error,
    check_self_status,
    generate_verification_config,
    explain_sdk_setup,
    generate_eu_id_verification
)

# Import all resources
from .resources import (
    get_contract_addresses,
    get_example_code,
    get_best_practices
)

# Import all prompts
from .prompts import (
    design_verification_flow,
    troubleshoot_integration
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