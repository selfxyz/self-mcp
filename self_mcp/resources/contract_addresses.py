"""Resource for Self protocol contract addresses"""


async def get_contract_addresses() -> str:
    """Get deployed Self protocol contract addresses"""
    return """# Self Protocol Contract Addresses (Celo Mainnet)

## Core Contracts
- IdentityVerificationHub: 0x77117D60eaB7C044e785D68edB6C7E0e134970Ea
- IdentityRegistry: 0x37F5CB8cB1f6B00aa768D8aA99F1A9289802A968
- VerifyAll: 0xe6D61680A6ED381bb5A0dB5cF4E9Cc933cF43915

## Verifier Contracts
- Verifier_vc_and_disclose: 0x44d314c2F9b3690735808d26d17dFCc9F906A9B4
- Verifier_register_sha256_sha256_sha256_rsa_65537_4096: 0xE80537B3399bd405e40136D08e24c250397c09F1
- Verifier_dsc_sha256_rsa_65537_4096: 0x711e655c43410fB985c4EDB48E9bCBdDb770368d

## SDK Packages
- Frontend: @selfxyz/qrcode
- Backend: @selfxyz/core
- Contracts: @selfxyz/contracts
"""