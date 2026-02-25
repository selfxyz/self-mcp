export function formatSuccess(data) {
    const text = typeof data === "string" ? data : JSON.stringify(data, null, 2);
    return { content: [{ type: "text", text }] };
}
export function formatError(message) {
    return { content: [{ type: "text", text: `Error: ${message}` }], isError: true };
}
export function formatResource(content) {
    return content.trim();
}
//# sourceMappingURL=format.js.map