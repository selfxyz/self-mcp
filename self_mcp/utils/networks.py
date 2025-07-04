"""Network configurations for Celo blockchain"""

CELO_NETWORKS = {
    "mainnet": {
        "name": "Celo Mainnet",
        "rpc": "https://forno.celo.org",
        "chainId": 42220,
        "explorer": "https://celoscan.io",
        "api": "https://api.celoscan.io/api",
        "currency": "CELO",
        "contracts": {
            "hub": "0x77117D60eaB7C044e785D68edB6C7E0e134970Ea",
            "registry": "0x37F5CB8cB1f6B00aa768D8aA99F1A9289802A968",
            "verifyAll": "0xe6D61680A6ED381bb5A0dB5cF4E9Cc933cF43915"
        }
    },
    "testnet": {
        "name": "Celo Alfajores Testnet", 
        "rpc": "https://alfajores-forno.celo-testnet.org",
        "chainId": 44787,
        "explorer": "https://alfajores.celoscan.io",
        "api": "https://api-alfajores.celoscan.io/api",
        "currency": "CELO",
        "contracts": {
            "hub": "0x68c931C9a534D37aa78094877F46fE46a49F1A51",  # Staging hub
            "registry": "0xE1A05bbee7D8DF2ee2A81dEE8FB22e07B07D1084",  # Staging registry
            "registryIdCard": "0xF77Be82318F11392Efb5F1062D954911d6086537",  # ID card registry
            "customVerifier": "0xC95e53bB0d26295c5814F4cE1d72fB4c2df0Fd4f",
            "testContract": "0x9633b661082BaB295Ff4883bc47E175e06afB5Bf"  # TestSelfVerificationRoot
        }
    }
}

# Default RPC URLs for quick access
CELO_MAINNET_RPC = CELO_NETWORKS["mainnet"]["rpc"]
CELO_TESTNET_RPC = CELO_NETWORKS["testnet"]["rpc"]