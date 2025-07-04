"""Tools for Self MCP server"""

from .integration import explain_self_integration
from .code_generation import generate_verification_code
from .debugging import debug_verification_error
from .status import check_self_status
from .config_generation import generate_verification_config
from .sdk_setup import explain_sdk_setup
from .eu_id_verification import generate_eu_id_verification

__all__ = [
    "explain_self_integration",
    "generate_verification_code", 
    "debug_verification_error",
    "check_self_status",
    "generate_verification_config",
    "explain_sdk_setup",
    "generate_eu_id_verification"
]