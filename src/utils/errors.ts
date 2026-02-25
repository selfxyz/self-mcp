export class McpToolError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "McpToolError";
  }
}

export function wrapToolError(error: unknown): string {
  if (error instanceof Error) return error.message;
  return String(error);
}
