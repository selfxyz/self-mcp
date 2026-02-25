const NETWORKS = {
    mainnet: {
        rpcUrl: "https://forno.celo.org",
    },
    testnet: {
        rpcUrl: "https://forno.celo-sepolia.celo-testnet.org",
    },
};
export function loadConfig() {
    const raw = process.env.SELF_NETWORK ?? "mainnet";
    if (raw !== "mainnet" && raw !== "testnet") {
        throw new Error(`Invalid SELF_NETWORK: "${raw}". Must be "mainnet" or "testnet".`);
    }
    const network = raw;
    const rpcUrl = process.env.SELF_RPC_URL ?? NETWORKS[network].rpcUrl;
    return { network, rpcUrl };
}
//# sourceMappingURL=config.js.map