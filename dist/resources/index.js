import { registerOverview } from "./overview.js";
import { registerContracts } from "./contracts.js";
import { registerSdkCore } from "./sdk-core.js";
import { registerVerifierGuide } from "./verifier-guide.js";
import { registerDocuments } from "./documents.js";
import { registerCircuits } from "./circuits.js";
import { registerCrossReference } from "./cross-reference.js";
import { registerSdkRn } from "./sdk-rn.js";
import { registerSdkMobile } from "./sdk-mobile.js";
import { registerSdkBridge } from "./sdk-bridge.js";
import { registerSdkKmp } from "./sdk-kmp.js";
import { registerSdkCommon } from "./sdk-common.js";
export function registerResources(server, config) {
    registerOverview(server, config);
    registerContracts(server, config);
    registerSdkCore(server, config);
    registerVerifierGuide(server, config);
    registerDocuments(server, config);
    registerCircuits(server, config);
    registerCrossReference(server, config);
    registerSdkRn(server, config);
    registerSdkMobile(server, config);
    registerSdkBridge(server, config);
    registerSdkKmp(server, config);
    registerSdkCommon(server, config);
}
//# sourceMappingURL=index.js.map