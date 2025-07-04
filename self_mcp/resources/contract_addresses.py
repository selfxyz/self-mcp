"""Resource for Self protocol contract addresses"""


async def get_contract_addresses() -> str:
    """Get deployed Self protocol contract addresses"""
    return """# Self Protocol Contract Addresses (V2)

## Celo Mainnet (Real Passports)
- IdentityVerificationHub: 0xe57F4773bd9c9d8b6Cd70431117d353298B9f5BF
- IdentityRegistry: 0x37F5CB8cB1f6B00aa768D8aA99F1A9289802A968
- VerifyAll: 0xe6D61680A6ED381bb5A0dB5cF4E9Cc933cF43915

## Celo Testnet (Mock Passports)
- IdentityVerificationHub: 0x68c931C9a534D37aa78094877F46fE46a49F1A51
- IdentityRegistry: 0x37F5CB8cB1f6B00aa768D8aA99F1A9289802A968
- VerifyAll: 0xe6D61680A6ED381bb5A0dB5cF4E9Cc933cF43915

## V2 Features
- Multi-document support (Passports + EU ID Cards)
- Enhanced verification with IConfigStorage
- Context-aware verification via userDefinedData
- AttestationId-based routing (1=Passport, 2=EU ID Card)

## SDK Packages (V2)
- Frontend: @selfxyz/qrcode
- Backend: @selfxyz/core
- Contracts: @selfxyz/contracts
"""