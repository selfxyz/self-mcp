import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { ServerConfig } from "../config.js";

const DOCUMENTS = `# Self Protocol — Supported Documents & Disclosure Attributes

## Document Types

| attestationId | Type        | Description                                      |
|---------------|-------------|--------------------------------------------------|
| 1             | E_PASSPORT  | Electronic passports with NFC chip (ICAO 9303)   |
| 2             | EU_ID_CARD  | EU biometric ID cards with NFC chip              |
| 3             | AADHAAR     | Indian Aadhaar cards                             |
| 4             | KYC         | KYC via SumSub (African markets initially)       |

## Supported Countries

195 countries are supported using ISO 3166-1 alpha-3 codes. The full list of country codes and their mappings is maintained in the @selfxyz/common package.

**Special case:** Germany uses 'D<<' in the passport MRZ (Machine Readable Zone) instead of the standard 'DEU' alpha-3 code. The SDK handles this mapping automatically.

## Disclosure Attributes (Passports & ID Cards — attestationId 1, 2)

These attributes can be selectively disclosed when using the \`vc_and_disclose\` circuit:

| Index | Attribute          | Description                                              |
|-------|--------------------|----------------------------------------------------------|
| 0     | issuing_state      | Country of issuance (ISO 3166-1 alpha-3)                 |
| 1     | name               | Full name as it appears on the document                  |
| 2     | passport_number    | Document number                                          |
| 3     | nationality        | Country of nationality (ISO 3166-1 alpha-3)              |
| 4     | date_of_birth      | Date of birth                                            |
| 5     | gender             | Gender (M/F)                                             |
| 6     | expiry_date        | Document expiry date                                     |
| 7     | older_than         | Age verification threshold (supported values: 0, 18, 21) |
| 8     | passport_no_ofac   | OFAC sanctions check on passport number + nationality    |
| 9     | name_and_dob_ofac  | OFAC sanctions check on name + date of birth             |
| 10    | name_and_yob_ofac  | OFAC sanctions check on name + year of birth             |

## KYC Fields (attestationId 4)

KYC verification uses SumSub and supports the following fields:

| Field         | Description               |
|---------------|---------------------------|
| country       | Country of issuance       |
| idType        | Type of ID document       |
| idNumber      | ID document number        |
| issuanceDate  | Date of issuance          |
| expiryDate    | Document expiry date      |
| fullName      | Full legal name           |
| DOB           | Date of birth             |
| photoHash     | Hash of the photo         |
| phoneNumber   | Phone number              |
| gender        | Gender                    |
| address       | Residential address       |

- 12 selector bits for selective disclosure of KYC fields
- Total serialization max: 299 bytes

## Constraints

- **MAX_FORBIDDEN_COUNTRIES_LIST_LENGTH = 40** — Maximum number of forbidden countries per verification config.
- **DEFAULT_MAJORITY = 18** — Default age threshold for majority verification.

## OFAC Tree Variants

OFAC (Office of Foreign Assets Control) sanctions checking uses merkle trees with different data combinations:

| Variant                  | Checks Against                     |
|--------------------------|------------------------------------|
| passport-no-nationality  | Passport number + nationality      |
| name-dob                 | Name + date of birth               |
| name-dob-id              | Name + date of birth (ID card)     |
| name-yob                 | Name + year of birth               |
| name-yob-id              | Name + year of birth (ID card)     |

- **OFAC_TREE_LEVELS = 64** — Depth of the OFAC merkle tree.

## Merkle Tree URLs

### Production
| Tree     | Passport URL                           | ID Card URL                               |
|----------|----------------------------------------|-------------------------------------------|
| DSC      | https://tree.self.xyz/dsc              | https://tree.self.xyz/dsc-id              |
| CSCA     | https://tree.self.xyz/csca             | https://tree.self.xyz/csca-id             |
| Identity | https://tree.self.xyz/identity         | https://tree.self.xyz/identity-id         |

### Staging
| Tree     | Passport URL                                   | ID Card URL                                       |
|----------|-------------------------------------------------|---------------------------------------------------|
| DSC      | https://tree.staging.self.xyz/dsc              | https://tree.staging.self.xyz/dsc-id              |
| CSCA     | https://tree.staging.self.xyz/csca             | https://tree.staging.self.xyz/csca-id             |
| Identity | https://tree.staging.self.xyz/identity         | https://tree.staging.self.xyz/identity-id         |
`;

export function registerDocuments(
  server: McpServer,
  _config: ServerConfig,
): void {
  server.resource("documents", "self://documents", async (uri) => ({
    contents: [
      { uri: uri.href, mimeType: "text/plain", text: DOCUMENTS },
    ],
  }));
}
