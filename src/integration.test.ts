import { describe, it, expect } from "vitest";
import { createServer } from "./server.js";
import { loadConfig } from "./config.js";

describe("createServer", () => {
  it("creates a server with config", () => {
    const { server, config } = createServer();
    expect(server).toBeDefined();
    expect(config).toBeDefined();
    expect(config.network).toBe("mainnet");
    expect(config.rpcUrl).toBe("https://forno.celo.org");
  });

  it("respects SELF_NETWORK env var", () => {
    process.env.SELF_NETWORK = "testnet";
    const { config } = createServer();
    expect(config.network).toBe("testnet");
    expect(config.rpcUrl).toContain("sepolia");
    delete process.env.SELF_NETWORK;
  });
});

describe("loadConfig", () => {
  it("throws on invalid SELF_NETWORK", () => {
    process.env.SELF_NETWORK = "staging";
    expect(() => loadConfig()).toThrow('Invalid SELF_NETWORK: "staging"');
    delete process.env.SELF_NETWORK;
  });
});
