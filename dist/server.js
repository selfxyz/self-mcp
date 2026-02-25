import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { loadConfig } from "./config.js";
import { registerResources } from "./resources/index.js";
import { registerContractTools } from "./tools/contracts.js";
import { registerPrompts } from "./prompts/index.js";
export function createServer() {
    const config = loadConfig();
    const server = new McpServer({ name: "self-protocol", version: "0.1.0" }, { capabilities: { logging: {} } });
    registerResources(server, config);
    registerContractTools(server, config);
    registerPrompts(server);
    return { server, config };
}
//# sourceMappingURL=server.js.map