"""Tool for generating Self protocol integration code"""

from typing import Literal, Optional
from fastmcp import Context

from ..utils.github_client import get_docs_client


async def generate_verification_code(
    component: Literal["frontend-qr", "backend-verify", "smart-contract"],
    language: Literal["typescript", "javascript", "solidity"] = "typescript",
    ctx: Optional[Context] = None,
) -> str:
    """
    Generate ready-to-use Self verification code for different components.
    
    Args:
        component: Which part to generate - 'frontend-qr', 'backend-verify', or 'smart-contract'
        language: Programming language - 'typescript', 'javascript', or 'solidity'
        
    Returns:
        Complete, working code example with comments
    """
    client = get_docs_client()
    
    # Map components to documentation files
    component_map = {
        "frontend-qr": "use-self/quickstart.md",
        "backend-verify": "use-self/quickstart.md", 
        "smart-contract": "contract-integration/basic-integration.md"
    }
    
    # Handle language compatibility
    if component == "smart-contract" and language != "solidity":
        language = "solidity"  # Force solidity for smart contracts
    elif component != "smart-contract" and language == "solidity":
        language = "typescript"  # Default to typescript for non-contracts
    
    # Fetch the documentation
    doc_path = component_map.get(component)
    if not doc_path:
        return f"Unknown component: {component}. Available: frontend-qr, backend-verify, smart-contract"
    
    content = await client.fetch_document(doc_path)
    if not content:
        return f"Failed to fetch documentation for {component}. Please try again later."
    
    # Extract relevant code sections based on component
    code_example = extract_code_example(content, component, language)
    
    if not code_example:
        # Fallback to basic examples
        code_example = generate_basic_example(component, language)
    
    # Log to context if available (FastMCP 2.0 feature)
    if ctx:
        await ctx.info(f"Generated {component} code in {language}")
    
    return code_example


def extract_code_example(content: str, component: str, language: str) -> str:
    """Extract code example from documentation content"""
    lines = content.split('\n')
    in_code_block = False
    code_lines = []
    found_relevant_section = False
    
    # Keywords to look for based on component
    section_keywords = {
        "frontend-qr": ["QRCodeGenerator", "SelfQRcode", "frontend", "QR code"],
        "backend-verify": ["SelfBackendVerifier", "verify", "backend"],
        "smart-contract": ["contract", "onchain", "solidity"]
    }
    
    for i, line in enumerate(lines):
        # Check if we're in a relevant section
        if any(keyword in line for keyword in section_keywords[component]):
            found_relevant_section = True
        
        # Look for code blocks
        if line.strip().startswith('```') and found_relevant_section:
            if not in_code_block:
                # Check if it's the right language
                lang_marker = line.strip().replace('```', '').lower()
                if lang_marker in [language, language[:2], 'js', 'ts'] or (component == "smart-contract" and lang_marker == "solidity"):
                    in_code_block = True
            else:
                # End of code block
                if code_lines:
                    return '\n'.join(code_lines)
                in_code_block = False
                code_lines = []
        elif in_code_block:
            code_lines.append(line)
    
    return None


def generate_basic_example(component: str, language: str) -> str:
    """Generate basic example if extraction fails"""
    if component == "frontend-qr":
        return _generate_frontend_example(language)
    elif component == "backend-verify":
        return _generate_backend_example(language)
    else:  # smart-contract
        return _generate_smart_contract_example()


def _generate_frontend_example(language: str) -> str:
    """Generate frontend QR code example"""
    return f"""// {language.upper()}: Self Verification QR Code Component

import SelfQRcodeWrapper, {{ SelfAppBuilder }} from '@selfxyz/qrcode';
import {{ v4 as uuidv4 }} from 'uuid';

// Create Self app configuration
const userId = uuidv4();
const selfApp = new SelfAppBuilder({{
  appName: "My Application",
  scope: "my-app-scope",
  endpoint: "https://myapp.com/api/verify",
  userId,
  disclosures: {{
    minimumAge: 18,
    excludedCountries: ['IRN', 'PRK'],
    ofac: true,
    name: true,
    nationality: true
  }}
}}).build();

// Render QR code component
function VerificationComponent() {{
  return (
    <SelfQRcodeWrapper
      selfApp={{selfApp}}
      onSuccess={{() => {{
        console.log('Verification successful!');
      }}}}
    />
  );
}}

export default VerificationComponent;"""


def _generate_backend_example(language: str) -> str:
    """Generate backend verification example"""
    return f"""// {language.upper()}: Self Backend Verification

import {{ SelfBackendVerifier, AttestationId, UserIdType }} from '@selfxyz/core';

// Configuration storage implementation
class SimpleConfigStorage {{
  async getConfig(configId) {{
    return {{
      olderThan: 18,
      excludedCountries: ['IRN', 'PRK'],
      ofac: true
    }};
  }}
  
  async getActionId(userIdentifier, userDefinedData) {{
    return 'default_config';
  }}
}}

// Define allowed attestation types
const allowedIds = new Map();
allowedIds.set(1, true); // Passport
allowedIds.set(2, true); // EU ID Card

// Initialize verifier
const selfBackendVerifier = new SelfBackendVerifier(
  "my-app-scope",
  "https://myapp.com/api/verify",
  false, // Use real passports
  allowedIds,
  new SimpleConfigStorage(),
  UserIdType.UUID
);

// Verify proof
async function verifyProof(req, res) {{
  const {{ attestationId, proof, pubSignals, userContextData }} = req.body;
  
  try {{
    const result = await selfBackendVerifier.verify(
      attestationId,
      proof,
      pubSignals,
      userContextData
    );
    
    if (result.isValidDetails.isValid) {{
      res.json({{
        status: 'success',
        userId: result.userData.userIdentifier,
        details: result.discloseOutput
      }});
    }} else {{
      res.status(400).json({{
        status: 'error',
        message: 'Verification failed'
      }});
    }}
  }} catch (error) {{
    res.status(500).json({{ error: error.message }});
  }}
}}"""


def _generate_smart_contract_example() -> str:
    """Generate smart contract example"""
    return """// SOLIDITY: On-chain Self Verification

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

interface IHub {
    function humanID(address human) external view returns (bool);
    function verify(
        uint256 scopeId,
        uint256 nullifier,
        uint256 modulus,
        uint256[8] calldata proof
    ) external returns (bool);
}

contract SelfVerifiedApp is Ownable {
    IHub public immutable hub;
    mapping(address => bool) public verifiedUsers;
    
    event UserVerified(address indexed user, uint256 timestamp);
    
    constructor(address _hub) {
        hub = IHub(_hub);
    }
    
    function verifyAndAccess(
        uint256 scopeId,
        uint256 nullifier,
        uint256 modulus,
        uint256[8] calldata proof
    ) external {
        // Verify proof through hub
        require(
            hub.verify(scopeId, nullifier, modulus, proof),
            "Invalid proof"
        );
        
        // Check if user has humanID
        require(hub.humanID(msg.sender), "No humanID");
        
        // Mark user as verified
        verifiedUsers[msg.sender] = true;
        emit UserVerified(msg.sender, block.timestamp);
    }
    
    modifier onlyVerified() {
        require(verifiedUsers[msg.sender], "Not verified");
        _;
    }
    
    // Your app logic here
    function accessProtectedFunction() external onlyVerified {
        // Only verified users can access
    }
}"""