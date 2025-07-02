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
            "hub": "Not deployed",
            "registry": "Not deployed",
            "verifyAll": "Not deployed"
        }
    }
}

# Default RPC URLs for quick access
CELO_MAINNET_RPC = CELO_NETWORKS["mainnet"]["rpc"]
CELO_TESTNET_RPC = CELO_NETWORKS["testnet"]["rpc"]