const CIRCUITS = `# Self Protocol — ZK Circuits Reference

## Circuit Types

| Circuit            | Purpose                                                                  |
|--------------------|--------------------------------------------------------------------------|
| dsc                | Document Signing Certificate verification — proves DSC chain of trust    |
| register           | Passport/ID registration — proves document authenticity & registers commitment |
| vc_and_disclose    | Verifiable credential disclosure — selective attribute reveal from a registered commitment |

## Register Circuits

52 variants covering combinations of hash functions and signature algorithms from real-world identity documents:

### Hash Functions
- SHA1
- SHA224
- SHA256
- SHA384
- SHA512

### Signature Algorithms
- **RSA** — Key sizes 2048-4096 bit, public exponents 65537 or 3
- **ECDSA** — Curves: secp256r1, secp384r1, secp521r1, brainpoolP224r1, brainpoolP256r1, brainpoolP384r1, brainpoolP512r1
- **RSA-PSS** — Probabilistic Signature Scheme variant of RSA

Each register circuit variant handles a specific (hash, signature algorithm, key size/curve) combination found in real passports and ID cards.

## DSC Circuits

20 variants covering similar algorithm combinations as the register circuits, but for verifying the Document Signing Certificate itself against the CSCA (Country Signing Certificate Authority) root.

## Proof Structure (Groth16)

All circuits produce Groth16 proofs with the following structure:

\`\`\`
{
  a: uint256[2],         // G1 point (proof element A)
  b: uint256[2][2],      // G2 point (proof element B)
  c: uint256[2],         // G1 point (proof element C)
  pubSignals: uint256[]  // Public signals (length varies by circuit)
}
\`\`\`

## Public Signals Layout (vc_and_disclose — passport, 21 signals)

| Index | Signal                        | Description                                       |
|-------|-------------------------------|---------------------------------------------------|
| 0     | scope                         | Application-specific scope identifier              |
| 1     | nullifier                     | Unique nullifier to prevent double-use             |
| 2     | user_id                       | User identifier bound to the proof                 |
| 3     | attestation_id                | Document type (1=passport, 2=ID card, etc.)        |
| 4     | merkle_root                   | Identity commitment merkle tree root               |
| 5     | current_date                  | Current date encoded in the proof                  |
| 6-14  | revealed_data_packed          | Packed revealed attribute data (9 field elements)  |
| 15    | older_than                    | Age threshold proven (0, 18, or 21)                |
| 16    | ofac_result                   | OFAC passport-no-nationality check result          |
| 17    | ofac_name_dob_result          | OFAC name + DOB check result                       |
| 18    | ofac_name_yob_result          | OFAC name + YOB check result                       |
| 19-20 | forbidden_countries_packed    | Packed forbidden countries list (2 field elements) |

## Key Constants

| Constant               | Value | Description                                         |
|------------------------|-------|-----------------------------------------------------|
| COMMITMENT_TREE_DEPTH  | 33    | Depth of the identity commitment merkle tree         |
| CSCA_TREE_DEPTH        | 12    | Depth of the CSCA (country signing CA) merkle tree   |
| DSC_TREE_DEPTH         | 21    | Depth of the DSC (document signing cert) merkle tree |
| OFAC_TREE_LEVELS       | 64    | Depth of the OFAC sanctions merkle tree              |
| MAX_DATAHASHES_LEN     | 320   | Maximum length of data hashes in bytes               |

## Additional Circuits

### Noir Circuits (noir/crates/dg1/)
- DG1 hash verification — verifies the hash of Data Group 1 (MRZ information)
- DG2 hash verification — verifies the hash of Data Group 2 (facial image)

### OFAC Name Checking Circuits
| Circuit              | Description                                      |
|----------------------|--------------------------------------------------|
| ofac_name            | Checks name against OFAC sanctions list          |
| ofac_name_dob        | Checks name + date of birth against OFAC list    |
| ofac_passport_number | Checks passport number against OFAC list         |

### GCP JWT Verifier Circuit
- Verifies Google Cloud Platform JWT tokens for Confidential Space attestation
- Used for trusted execution environment (TEE) verification
`;
export function registerCircuits(server, _config) {
    server.resource("circuits", "self://circuits", async (uri) => ({
        contents: [
            { uri: uri.href, mimeType: "text/plain", text: CIRCUITS },
        ],
    }));
}
//# sourceMappingURL=circuits.js.map