export class McpToolError extends Error {
    constructor(message) {
        super(message);
        this.name = "McpToolError";
    }
}
export function wrapToolError(error) {
    if (error instanceof Error)
        return error.message;
    return String(error);
}
//# sourceMappingURL=errors.js.map