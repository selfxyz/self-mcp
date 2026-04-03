export interface ServerConfig {
  network: "mainnet" | "testnet";
  rpcUrl: string;
}

const NETWORKS = {
  mainnet: {
    rpcUrl: "https://forno.celo.org",
  },
  testnet: {
    rpcUrl: "https://forno.celo-sepolia.celo-testnet.org",
  },
} as const;

export function loadConfig(): ServerConfig {
  const raw = process.env.SELF_NETWORK ?? "mainnet";
  if (raw !== "mainnet" && raw !== "testnet") {
    throw new Error(
      `Invalid SELF_NETWORK: "${raw}". Must be "mainnet" or "testnet".`
    );
  }
  const network = raw;
  const rpcUrl = process.env.SELF_RPC_URL ?? NETWORKS[network].rpcUrl;
  return { network, rpcUrl };
}
