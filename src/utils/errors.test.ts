import { describe, it, expect } from "vitest";
import { McpToolError, wrapToolError } from "./errors.js";

describe("McpToolError", () => {
  it("has correct name", () => {
    const err = new McpToolError("test");
    expect(err.name).toBe("McpToolError");
    expect(err.message).toBe("test");
  });
});

describe("wrapToolError", () => {
  it("extracts message from Error", () => {
    expect(wrapToolError(new Error("fail"))).toBe("fail");
  });

  it("stringifies non-Error values", () => {
    expect(wrapToolError(42)).toBe("42");
  });
});
