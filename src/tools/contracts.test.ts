import { describe, it, expect, vi } from "vitest";

vi.mock("ethers", () => ({
  ethers: {
    JsonRpcProvider: vi.fn(),
    Contract: vi.fn(),
  },
}));

describe("contract tools", () => {
  it("module exports registerContractTools", async () => {
    const mod = await import("./contracts.js");
    expect(typeof mod.registerContractTools).toBe("function");
  });
});
