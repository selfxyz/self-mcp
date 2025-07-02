"""Self MCP Server - Clean architecture implementation"""

from mcp.server.fastmcp import FastMCP

# Import all tools
from .tools import (
    explain_self_integration,
    generate_verification_code,
    debug_verification_error,
    check_self_status,
    generate_verification_config
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

# Register tools
mcp.tool()(explain_self_integration)
mcp.tool()(generate_verification_code)
mcp.tool()(debug_verification_error)
mcp.tool()(check_self_status)
mcp.tool()(generate_verification_config)

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