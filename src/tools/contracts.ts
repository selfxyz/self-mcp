import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { ethers } from "ethers";
import type { ServerConfig } from "../config.js";
import { formatSuccess, formatError } from "../utils/format.js";
import { wrapToolError } from "../utils/errors.js";

const ADDRESSES: Record<
  string,
  {
    hub: string;
    hubImpl: string;
    registryPassport: string;
    registryKyc: string;
    registryAadhaar?: string;
    poseidonT3: string;
    verifierGcpJwt: string;
    pcr0Manager?: string;
    securityMultisig?: string;
    operationsMultisig?: string;
    rpcUrl: string;
  }
> = {
  mainnet: {
    hub: "0xe57F4773bd9c9d8b6Cd70431117d353298B9f5BF",
    hubImpl: "0xa267e58B2d6BA9fc07Af06471423AFb56e4e82B3",
    registryPassport: "0xd603Fa8C8f4694E8DD1DcE1f27C0C3fc91e32Ac4",
    registryKyc: "0x9cABdeBC3aF136efD69EB881e02118AC612c63b9",
    registryAadhaar: "0x70D543432782D460C96753b52c2aC2797f26924B",
    poseidonT3: "0xF134707a4C4a3a76b8410fC0294d620A7c341581",
    verifierGcpJwt: "0x87785cC7E9Bc70f87E6F454235214bDEc853C044",
    securityMultisig: "0x738f0bb37FD3b6C4Cdf8eb6FcdFaAA0CA208CB4A",
    operationsMultisig: "0x067b18e09A10Fa03d027c1D60A098CEbbE5637f0",
    rpcUrl: "https://forno.celo.org",
  },
  testnet: {
    hub: "0x16ECBA51e18a4a7e61fdC417f0d47AFEeDfbed74",
    hubImpl: "0x48985ec4f71cBC8f387c5C77143110018560c7eD",
    registryPassport: "0x1651ec77c3dC5997eC05f3EE6C2B0b904b516d1d",
    registryKyc: "0x90e907E4AaB6e9bcFB94997Af4A097e8CAadBdf3",
    poseidonT3: "0x0a782f7F9f8Aac6E0bacAF3cD4aA292C3275C6f2",
    pcr0Manager: "0xf2810D5E9938816D42F0Ae69D33F013a23C0aED2",
    verifierGcpJwt: "0x13ee8CEa15a262D81a245b37889F7b4bEd015f4c",
    rpcUrl: "https://forno.celo-sepolia.celo-testnet.org",
  },
};

const HUB_ABI = [
  "function registry(bytes32 attestationId) view returns (address)",
  "function discloseVerifier(bytes32 attestationId) view returns (address)",
];

const REGISTRY_ABI = [
  "function checkIdentityCommitmentRoot(uint256 root) view returns (bool)",
  "function getIdentityCommitmentMerkleRoot() view returns (uint256)",
  "function getPassportNoOfacRoot() view returns (uint256)",
  "function getNameAndDobOfacRoot() view returns (uint256)",
  "function getNameAndYobOfacRoot() view returns (uint256)",
];

export function registerContractTools(
  server: McpServer,
  config: ServerConfig
): void {
  server.tool(
    "self_get_contract_addresses",
    "Get all deployed Self Protocol contract addresses for a given network",
    { network: z.enum(["mainnet", "testnet"]).optional() },
    async ({ network }) => {
      const net = network ?? config.network;
      const addrs = ADDRESSES[net];
      if (!addrs) return formatError(`Unknown network: ${net}`);
      return formatSuccess({
        network: net,
        chainId: net === "mainnet" ? 42220 : 11142220,
        contracts: addrs,
      });
    }
  );

  server.tool(
    "self_check_verification",
    "Check if a merkle root is valid in a Self Protocol identity registry",
    {
      attestationId: z
        .number()
        .describe("1=passport, 2=ID card, 3=aadhaar, 4=kyc"),
      merkleRoot: z.string().describe("Merkle root to check (decimal or hex)"),
      network: z.enum(["mainnet", "testnet"]).optional(),
    },
    async ({ attestationId, merkleRoot, network }) => {
      const net = network ?? config.network;
      const addrs = ADDRESSES[net];
      if (!addrs) return formatError(`Unknown network: ${net}`);

      try {
        const provider = new ethers.JsonRpcProvider(addrs.rpcUrl);
        const hub = new ethers.Contract(addrs.hub, HUB_ABI, provider);
        const attId =
          "0x" + attestationId.toString(16).padStart(64, "0");
        const registryAddress: string = await hub.registry(attId);

        if (
          registryAddress === "0x0000000000000000000000000000000000000000"
        ) {
          return formatError(
            `No registry found for attestationId ${attestationId} on ${net}`
          );
        }

        const registry = new ethers.Contract(
          registryAddress,
          REGISTRY_ABI,
          provider
        );
        const valid: boolean =
          await registry.checkIdentityCommitmentRoot(merkleRoot);

        return formatSuccess({
          network: net,
          attestationId,
          registryAddress,
          merkleRoot,
          valid,
        });
      } catch (error) {
        return formatError(wrapToolError(error));
      }
    }
  );

  server.tool(
    "self_get_registry_info",
    "Query identity registry state (merkle root, OFAC roots) for a document type",
    {
      attestationId: z
        .number()
        .describe("1=passport, 2=ID card, 3=aadhaar, 4=kyc"),
      network: z.enum(["mainnet", "testnet"]).optional(),
    },
    async ({ attestationId, network }) => {
      const net = network ?? config.network;
      const addrs = ADDRESSES[net];
      if (!addrs) return formatError(`Unknown network: ${net}`);

      try {
        const provider = new ethers.JsonRpcProvider(addrs.rpcUrl);
        const hub = new ethers.Contract(addrs.hub, HUB_ABI, provider);
        const attId =
          "0x" + attestationId.toString(16).padStart(64, "0");
        const registryAddress: string = await hub.registry(attId);

        if (
          registryAddress === "0x0000000000000000000000000000000000000000"
        ) {
          return formatError(
            `No registry found for attestationId ${attestationId} on ${net}`
          );
        }

        const registry = new ethers.Contract(
          registryAddress,
          REGISTRY_ABI,
          provider
        );

        const [merkleRoot, passportNoOfacRoot, nameAndDobOfacRoot, nameAndYobOfacRoot] =
          await Promise.all([
            registry.getIdentityCommitmentMerkleRoot(),
            registry.getPassportNoOfacRoot().catch(() => null),
            registry.getNameAndDobOfacRoot().catch(() => null),
            registry.getNameAndYobOfacRoot().catch(() => null),
          ]);

        return formatSuccess({
          network: net,
          attestationId,
          registryAddress,
          merkleRoot: merkleRoot.toString(),
          ofacRoots: {
            passportNo: passportNoOfacRoot?.toString() ?? null,
            nameAndDob: nameAndDobOfacRoot?.toString() ?? null,
            nameAndYob: nameAndYobOfacRoot?.toString() ?? null,
          },
        });
      } catch (error) {
        return formatError(wrapToolError(error));
      }
    }
  );
}
