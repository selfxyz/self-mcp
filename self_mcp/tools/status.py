"""Tool for checking Self protocol status"""

from typing import Literal
from ..utils.networks import CELO_NETWORKS


async def check_self_status(
    network: Literal["celo-mainnet", "celo-testnet"] = "celo-mainnet"
) -> str:
    """Check Self protocol deployment status and contract addresses"""
    
    # Map input to our network keys
    network_key = "mainnet" if network == "celo-mainnet" else "testnet"
    config = CELO_NETWORKS[network_key]
    contracts = config["contracts"]
    
    return f"""## Self Protocol Status - {config['name']}

### Network Configuration
- RPC Endpoint: `{config['rpc']}`
- Chain ID: `{config['chainId']}`
- Block Explorer: {config['explorer']}
- API Endpoint: `{config['api']}`

### Core Contracts
- IdentityVerificationHub: `{contracts['hub']}`
- IdentityRegistry: `{contracts['registry']}`

### Integration Steps
1. Use RPC endpoint in your backend verifier
2. Reference these contract addresses for on-chain verification
3. Check explorer for transaction details

### SDK Versions
- @selfxyz/core: Latest (npm)
- @selfxyz/qrcode: Latest (npm)
- @selfxyz/contracts: Latest (npm)

### Network Details
- Network: {config['name']}
- Chain ID: {config['chainId']}
- Currency: CELO
"""