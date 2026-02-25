const SDK_COMMON = `# @selfxyz/common v0.0.9 — Shared Utilities, Types, and Constants

## Overview

The common package provides 150+ exports covering crypto, circuits, passports, certificates, hashing, and contract utilities shared across all Self SDK packages. It is the foundation layer used by @selfxyz/core, @selfxyz/rn-sdk, @selfxyz/mobile-sdk-alpha, and @selfxyz/kmp-sdk.

## Constants

### Countries
195 ISO alpha-3 country codes available as typed constants.

\`\`\`typescript
import { countries } from '@selfxyz/common';
// countries: Country3LetterCode[] — e.g. 'USA', 'GBR', 'FRA', 'DEU', ...
\`\`\`

### Attestation IDs
\`\`\`typescript
const PASSPORT_ATTESTATION_ID = 1;
const ID_CARD_ATTESTATION_ID = 2;
const AADHAAR_ATTESTATION_ID = 3;
const KYC_ATTESTATION_ID = 4;
\`\`\`

### API URLs
Pre-configured API endpoint URLs for mainnet, testnet, and staging environments.

## SelfAppBuilder Class

The developer-facing request configuration builder. Used to construct verification requests across all client SDKs.

\`\`\`typescript
import { SelfAppBuilder } from '@selfxyz/common';

const selfApp = new SelfAppBuilder()
  .setAppName('My App')                    // Required: display name
  .setScope('my-app-scope')                // Required: unique scope identifier
  .setEndpoint('https://my-app.com/verify') // Required: verification callback URL
  .setUserId('user-uuid-here')             // Required: user identifier
  .setEndpointType('https')                // Optional: 'https' | 'celo' | 'staging_celo'
  .setUserIdType('uuid')                   // Optional: 'uuid' | 'hex'
  .setDevMode(false)                       // Optional: enable dev/test mode
  .setDisclosures({                        // Optional: configure required disclosures
    issuing_state: true,
    name: true,
    passport_number: false,
    nationality: true,
    date_of_birth: true,
    gender: false,
    expiry_date: false,
    ofac: true,
    excludedCountries: ['PRK', 'IRN'],
    minimumAge: 18,
  })
  .build();  // Returns SelfApp object
\`\`\`

### SelfAppDisclosureConfig

\`\`\`typescript
interface SelfAppDisclosureConfig {
  issuing_state?: boolean;         // Require disclosure of issuing state
  name?: boolean;                  // Require disclosure of full name
  passport_number?: boolean;       // Require disclosure of document number
  nationality?: boolean;           // Require disclosure of nationality
  date_of_birth?: boolean;         // Require disclosure of date of birth
  gender?: boolean;                // Require disclosure of gender
  expiry_date?: boolean;           // Require disclosure of document expiry
  ofac?: boolean;                  // Require OFAC sanctions screening
  excludedCountries?: string[];    // ISO alpha-3 codes of countries to reject
  minimumAge?: number;             // Minimum age threshold (e.g. 18, 21)
}
\`\`\`

### SelfApp

The output of \`SelfAppBuilder.build()\`:

\`\`\`typescript
interface SelfApp {
  appName: string;
  scope: string;
  endpoint: string;
  userId: string;
  endpointType: 'https' | 'celo' | 'staging_celo';
  userIdType: 'uuid' | 'hex';
  devMode: boolean;
  disclosures: SelfAppDisclosureConfig;
}
\`\`\`

### getUniversalLink()

Generates a deep link URL for opening the Self app with a pre-configured verification request.

\`\`\`typescript
import { getUniversalLink } from '@selfxyz/common';

const link = getUniversalLink(selfApp);
// Returns a URL like: https://self.xyz/verify?...
\`\`\`

## Circuit Utilities

Functions for generating circuit inputs for the three main ZK circuits:

### generateCircuitInputsRegister()
Generates inputs for the \`register\` circuit — proves document authenticity and registers a commitment.

\`\`\`typescript
import { generateCircuitInputsRegister } from '@selfxyz/common';

const inputs = generateCircuitInputsRegister(passportData, options);
\`\`\`

### generateCircuitInputsVCandDisclose()
Generates inputs for the \`vc_and_disclose\` circuit — proves selective disclosure claims against a registered commitment.

\`\`\`typescript
import { generateCircuitInputsVCandDisclose } from '@selfxyz/common';

const inputs = generateCircuitInputsVCandDisclose(commitment, disclosures, options);
\`\`\`

### generateCircuitInputsDSC()
Generates inputs for the \`dsc\` circuit — proves the Document Signing Certificate chain of trust.

\`\`\`typescript
import { generateCircuitInputsDSC } from '@selfxyz/common';

const inputs = generateCircuitInputsDSC(dscData, options);
\`\`\`

## Hash Utilities

Cryptographic hashing functions used across circuits and proofs:

\`\`\`typescript
import {
  customHasher,
  flexiblePoseidon,
  hash,
  packBytesAndPoseidon,
} from '@selfxyz/common';
\`\`\`

- **customHasher** — Configurable hasher for various circuit input requirements
- **flexiblePoseidon** — Poseidon hash with flexible input length
- **hash** — General-purpose hashing function
- **packBytesAndPoseidon** — Packs byte arrays and applies Poseidon hash

## Passport Utilities

Functions for parsing and working with passport data:

\`\`\`typescript
import {
  genMockIdDoc,
  initPassportDataParsing,
  parseDscCertificateData,
} from '@selfxyz/common';
\`\`\`

- **genMockIdDoc()** — Generate a mock identity document for testing
- **initPassportDataParsing()** — Initialize the passport data parsing pipeline
- **parseDscCertificateData()** — Parse a Document Signing Certificate (DSC) from raw certificate data

## KYC Utilities

Functions for KYC-specific circuit input generation:

\`\`\`typescript
import {
  generateKycDiscloseInput,
  generateKycRegisterInput,
} from '@selfxyz/common';
\`\`\`

- **generateKycDiscloseInput()** — Generate circuit inputs for KYC disclosure proofs
- **generateKycRegisterInput()** — Generate circuit inputs for KYC registration proofs

## Key Types

\`\`\`typescript
// Raw passport data from NFC chip
interface PassportData {
  dg1: Uint8Array;     // MRZ data
  dg2: Uint8Array;     // Photo data
  sod: Uint8Array;     // Security Object Document
  // ... additional data groups
}

// Parsed identity document
interface IDDocument {
  documentType: string;
  issuingState: string;
  name: string;
  documentNumber: string;
  nationality: string;
  dateOfBirth: string;
  gender: string;
  expiryDate: string;
}

// Document catalog for local storage
interface DocumentCatalog {
  documents: IDDocument[];
  lastUpdated: number;
}

// 3-letter country code type
type Country3LetterCode = 'AFG' | 'ALB' | 'DZA' | /* ... 195 total */ 'ZWE';
\`\`\`
`;
export function registerSdkCommon(server, config) {
    server.resource("sdk-common", "self://sdk/common", async (uri) => ({
        contents: [
            {
                uri: uri.href,
                mimeType: "text/plain",
                text: SDK_COMMON,
            },
        ],
    }));
}
//# sourceMappingURL=sdk-common.js.map