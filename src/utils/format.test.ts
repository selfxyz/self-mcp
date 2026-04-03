import { describe, it, expect } from "vitest";
import { formatSuccess, formatError, formatResource } from "./format.js";

describe("formatSuccess", () => {
  it("wraps string data", () => {
    const result = formatSuccess("hello");
    expect(result.content[0].text).toBe("hello");
  });

  it("serializes objects to JSON", () => {
    const result = formatSuccess({ key: "value" });
    expect(JSON.parse(result.content[0].text)).toEqual({ key: "value" });
  });
});

describe("formatError", () => {
  it("prefixes with Error:", () => {
    const result = formatError("bad input");
    expect(result.content[0].text).toBe("Error: bad input");
    expect(result.isError).toBe(true);
  });
});

describe("formatResource", () => {
  it("trims whitespace", () => {
    expect(formatResource("  content  ")).toBe("content");
  });
});
