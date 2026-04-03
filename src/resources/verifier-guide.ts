import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { ServerConfig } from "../config.js";

const CONTENT = `# Custom Verifier Guide — Building On-Chain Verifiers with SelfVerificationRoot

## 1. SelfVerificationRoot Base Contract

SelfVerificationRoot is the abstract contract you extend to build custom on-chain verifier contracts. It handles proof validation, scope binding, and attestation routing so you can focus on your business logic.

### Constructor

\`\`\`solidity
constructor(address identityVerificationHubV2Address, string memory scopeSeed)
\`\`\`

- \`identityVerificationHubV2Address\` — address of the deployed IdentityVerificationHub V2 contract.
- \`scopeSeed\` — an arbitrary string used (together with your contract's address) to derive a unique scope via Poseidon hash. This scope binds proofs to your specific verifier, preventing proof reuse across different contracts.

The scope is auto-calculated internally as \`PoseidonT3.hash([address(this), scopeSeed])\`. You do not compute it yourself.

### Methods to Override

You must override exactly two methods:

#### getConfigId

\`\`\`solidity
function getConfigId(
    bytes32 destinationChainId,
    bytes32 userIdentifier,
    bytes memory userDefinedData
) internal view virtual returns (bytes32);
\`\`\`

Return the verification config ID that the hub should use when validating this proof. The config ID determines which disclosures are required (age check, OFAC, nationality, etc.). You can return different config IDs based on the chain, user, or custom data passed in.

#### customVerificationHook

\`\`\`solidity
function customVerificationHook(
    GenericDiscloseOutputV2 memory output,
    bytes memory userData
) internal virtual;
\`\`\`

This is where your business logic goes. It is called after the hub has successfully validated the proof. The \`output\` struct contains all disclosed fields from the proof, and \`userData\` is the opaque context data passed by the caller.

---

## 2. GenericDiscloseOutputV2 Struct

The output struct passed to your \`customVerificationHook\` contains the following fields:

\`\`\`solidity
struct GenericDiscloseOutputV2 {
    bytes32 attestationId;         // Which document type (see AttestationId constants)
    uint256 userIdentifier;        // Derived user ID; cast to address via address(uint160())
    uint256 nullifier;             // Unique per proof — use to prevent double-spending
    uint256[4] forbiddenCountriesListPacked; // Packed country check results
    string issuingState;           // Country that issued the document (ISO 3166-1 alpha-3)
    string[] name;                 // Full name as array of parts
    string idNumber;               // Document number
    string nationality;            // Nationality (ISO 3166-1 alpha-3)
    string dateOfBirth;            // Format "DD-MM-YY"
    string gender;                 // Gender as recorded on document
    string expiryDate;             // Document expiry date
    uint256 olderThan;             // Age verification result (0 if not requested)
    bool[3] ofac;                  // [passportNoOfac, nameAndDobOfac, nameAndYobOfac]
}
\`\`\`

### Field Notes

- \`attestationId\` — identifies the document type. Compare against the AttestationId constants below.
- \`userIdentifier\` — a uint256 derived from the proof. To get the user's wallet address, cast it: \`address(uint160(output.userIdentifier))\`.
- \`nullifier\` — unique per proof submission. Store these in a mapping to prevent the same proof from being used twice.
- \`olderThan\` — contains the age threshold if an age check was configured (e.g. 18, 21). Zero if no age check was requested.
- \`ofac\` — three booleans indicating OFAC sanctions screening results against different data combinations.
- \`dateOfBirth\` — format is "DD-MM-YY" (two-digit year).

---

## 3. Data Flow

The end-to-end verification flow works as follows:

1. **Caller submits proof** — An external caller (user or relayer) calls \`verifySelfProof(proofPayload, userContextData)\` on your contract.
2. **Internal extraction** — Your contract (via SelfVerificationRoot) extracts the \`attestationId\` from the proof payload, builds the \`hubData\` struct including your contract's scope, and calls \`hub.verify()\` on the IdentityVerificationHub V2.
3. **Hub validates** — The hub validates the ZK proof against the correct circuit verifier, checks the scope binding, and on success calls \`onVerificationSuccess()\` back on your contract.
4. **Your hook executes** — The \`onVerificationSuccess()\` callback decodes the proof output into a \`GenericDiscloseOutputV2\` struct and calls your \`customVerificationHook()\` with the output and the original userData.

This is an async callback pattern: you initiate verification, and the hub calls you back on success. Your business logic in \`customVerificationHook()\` only runs if the proof is valid.

---

## 4. AttestationId Constants

Use these constants to identify the document type in the proof output:

\`\`\`solidity
bytes32 constant E_PASSPORT  = bytes32(uint256(1));
bytes32 constant EU_ID_CARD  = bytes32(uint256(2));
bytes32 constant AADHAAR     = bytes32(uint256(3));
bytes32 constant KYC         = bytes32(uint256(4));
\`\`\`

In your \`customVerificationHook\`, you can switch on \`output.attestationId\` to handle different document types differently, or require a specific type:

\`\`\`solidity
require(
    output.attestationId == E_PASSPORT || output.attestationId == EU_ID_CARD,
    "Unsupported document type"
);
\`\`\`

---

## 5. Example: HappyBirthday Contract

Here is a realistic example showing the full pattern. This contract sends a USDC birthday gift to users who prove it is their birthday:

\`\`\`solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {SelfVerificationRoot} from "./SelfVerificationRoot.sol";
import {GenericDiscloseOutputV2} from "./GenericDiscloseOutputV2.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract HappyBirthday is SelfVerificationRoot {
    bytes32 public immutable verificationConfigId;
    IERC20 public immutable usdc;
    uint256 public giftAmount;

    // Track nullifiers to prevent double-spending
    mapping(uint256 => bool) public nullifierUsed;

    constructor(
        address hubAddress,
        bytes32 _verificationConfigId,
        address _usdc,
        uint256 _giftAmount
    ) SelfVerificationRoot(hubAddress, "HappyBirthday") {
        verificationConfigId = _verificationConfigId;
        usdc = IERC20(_usdc);
        giftAmount = _giftAmount;
    }

    /// @notice Return the verification config ID for all proofs
    function getConfigId(
        bytes32, // destinationChainId
        bytes32, // userIdentifier
        bytes memory // userDefinedData
    ) internal view override returns (bytes32) {
        return verificationConfigId;
    }

    /// @notice Business logic: check birthday window, prevent double-spend, transfer USDC
    function customVerificationHook(
        GenericDiscloseOutputV2 memory output,
        bytes memory // userData
    ) internal override {
        // 1. Prevent double-spending: each nullifier can only be used once
        require(!nullifierUsed[output.nullifier], "Proof already used");
        nullifierUsed[output.nullifier] = true;

        // 2. Check that today is the user's birthday (compare day and month)
        //    dateOfBirth format is "DD-MM-YY"
        bytes memory dob = bytes(output.dateOfBirth);
        (uint256 day, uint256 month) = _parseDayMonth(dob);
        (uint256 currentDay, uint256 currentMonth) = _getCurrentDayMonth();
        require(day == currentDay && month == currentMonth, "Not your birthday");

        // 3. Extract the recipient address from userIdentifier
        address recipient = address(uint160(output.userIdentifier));

        // 4. Transfer the birthday gift
        require(usdc.transfer(recipient, giftAmount), "Transfer failed");
    }

    // ... helper functions for date parsing omitted for brevity
}
\`\`\`

### Key Patterns in This Example

- **Store verificationConfigId** — Set once in the constructor, returned by \`getConfigId()\`.
- **Nullifier tracking** — A \`mapping(uint256 => bool)\` prevents the same proof from being reused.
- **Extract recipient** — \`address(uint160(output.userIdentifier))\` converts the user identifier to an Ethereum address.
- **Business logic in hook** — All application-specific checks (birthday window, balance checks, etc.) go in \`customVerificationHook()\`.

---

## 6. Integration Checklist

When building your custom verifier:

- [ ] **Inherit SelfVerificationRoot** — Pass the IdentityVerificationHub V2 address and a unique scope seed string to the constructor.
- [ ] **Override getConfigId** — Return the verification config ID that matches your required disclosures. You can use different config IDs for different scenarios.
- [ ] **Override customVerificationHook** — Implement your business logic. This is only called after the proof has been validated by the hub.
- [ ] **Store nullifiers** — Maintain a \`mapping(uint256 => bool)\` and check/set it in your hook to prevent double-spending. This is critical for any contract that transfers value.
- [ ] **Handle multiple attestation IDs** — Decide which document types you accept (E_PASSPORT, EU_ID_CARD, AADHAAR, KYC). Either require a specific type or handle each appropriately.
- [ ] **Extract recipient correctly** — Use \`address(uint160(output.userIdentifier))\` to convert the user identifier to an address. Do not cast directly from uint256 — you must go through uint160 first.
- [ ] **Test on testnet first** — Deploy and test on Celo Sepolia (chain ID 11142220) before deploying to Celo Mainnet (chain ID 42220).
- [ ] **Set appropriate gas limits** — See Celo-specific gotchas below.

---

## 7. Celo-Specific Gotchas

### Stale ERC1967 Storage During Gas Estimation

Celo nodes can return stale proxy storage during \`eth_estimateGas\`, causing gas estimation to fail or produce incorrect results. Always use an explicit gas limit:

\`\`\`typescript
const tx = await contract.verifySelfProof(proofPayload, userData, {
    gasLimit: 200000,
});
\`\`\`

### OpenZeppelin Upgrades Manifest

The OZ Upgrades plugin stores deployment state in \`.openzeppelin/\` manifest files. These can become stale if you redeploy contracts or switch networks. If you encounter manifest-related errors, back up and delete the \`.openzeppelin/\` directory before redeploying.

### RPC Provider Reliability

Use Alchemy RPC endpoints for reliable deployments on Celo. The default \`drpc.org\` endpoints can be unreliable for deployment transactions. Configure your Hardhat/Foundry RPC URL accordingly.

### Aadhaar Registry Initialize Bug

If deploying an Aadhaar-related registry, there is a known bug where the hub address is not set during \`initialize()\`. After deployment, call \`updateHub(hubAddress)\` separately to set the correct hub address.

---

## 8. PoseidonT3 Addresses

The scope calculation in SelfVerificationRoot uses the PoseidonT3 hash function. The predeployed PoseidonT3 library addresses are:

| Network          | Address                                      |
|------------------|----------------------------------------------|
| Celo Mainnet     | \`0xF134707a4C4a3a76b8410fC0294d620A7c341581\` |
| Celo Sepolia     | \`0x0a782f7F9f8Aac6E0bacAF3cD4aA292C3275C6f2\` |

You generally do not need to interact with PoseidonT3 directly — SelfVerificationRoot handles scope calculation internally. These addresses are provided for reference if you need to debug scope values or compute them off-chain.

To compute a scope off-chain (e.g. for testing):

\`\`\`typescript
import { poseidon2 } from "poseidon-lite";

const scope = poseidon2([contractAddress, scopeSeedHash]);
\`\`\`
`;

export function registerVerifierGuide(
  server: McpServer,
  config: ServerConfig,
): void {
  server.resource(
    "verifier-guide",
    "self://contracts/verifier-guide",
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          mimeType: "text/plain" as const,
          text: CONTENT,
        },
      ],
    }),
  );
}
