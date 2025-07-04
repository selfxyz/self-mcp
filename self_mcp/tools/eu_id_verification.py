"""Tool for EU ID Card verification support"""

from typing import Literal
from fastmcp import Context


async def generate_eu_id_verification(
    component: Literal["frontend", "backend", "smart-contract"],
    language: Literal["typescript", "javascript", "solidity"] = "typescript",
    ctx: Context = None
) -> str:
    """
    Generate code for EU ID card verification (Self V2 feature).
    
    Args:
        component: Which part to generate - 'frontend', 'backend', or 'smart-contract'
        language: Programming language - 'typescript', 'javascript', or 'solidity'
        ctx: FastMCP context for logging
        
    Returns:
        Complete code example for EU ID card verification
    """
    
    if ctx:
        await ctx.info(f"Generating EU ID card verification code for {component} in {language}")
    
    if component == "frontend":
        if language == "javascript":
            return """import { SelfAppBuilder } from '@selfxyz/qrcode';

// EU ID Card verification setup
const selfApp = new SelfAppBuilder({
  appName: 'My EU ID App',
  scope: 'eu-id-verification',
  endpoint: '/api/verify-eu-id',
  disclosures: {
    // EU ID specific fields
    nationality: true,
    documentType: 'eu_id', // Specify EU ID card
    minimumAge: 18,
    // EU ID cards support additional fields
    firstName: true,
    lastName: true,
    dateOfBirth: true,
  },
  // Important: Specify document type
  supportedDocuments: ['eu_id', 'passport'] // Allow both
}).build();

// Add to your HTML
document.getElementById('qr-container').appendChild(selfApp);"""
        
        else:  # TypeScript
            return """import { SelfAppBuilder, DocumentType } from '@selfxyz/qrcode';

// EU ID Card verification with TypeScript
interface EUIDVerificationConfig {
  documentType: DocumentType.EU_ID | DocumentType.PASSPORT;
  requiredFields: string[];
}

const config: EUIDVerificationConfig = {
  documentType: DocumentType.EU_ID,
  requiredFields: ['nationality', 'firstName', 'lastName']
};

const selfApp = new SelfAppBuilder({
  appName: 'My EU ID App',
  scope: 'eu-id-verification',
  endpoint: '/api/verify-eu-id',
  disclosures: {
    // EU ID specific disclosures
    nationality: true,
    documentType: config.documentType,
    minimumAge: 18,
    firstName: true,
    lastName: true,
    dateOfBirth: true,
  },
  // Specify supported document types
  supportedDocuments: [DocumentType.EU_ID, DocumentType.PASSPORT],
  // EU ID specific options
  verificationOptions: {
    allowMultipleDocumentTypes: true,
    preferredDocumentType: DocumentType.EU_ID
  }
}).build();

// React component
export function EUIDVerification() {
  return (
    <div>
      <h2>Verify with EU ID Card or Passport</h2>
      {selfApp}
    </div>
  );
}"""
    
    elif component == "backend":
        if language == "javascript":
            return """const { SelfBackendVerifier, DocumentType } = require('@selfxyz/core');

// Initialize verifier for EU ID cards
const verifier = new SelfBackendVerifier(
  'https://forno.celo.org',
  'eu-id-verification'
);

// Configure for EU ID verification
verifier.setDocumentType(DocumentType.EU_ID);
verifier.setMinimumAge(18);

// EU ID specific validation
app.post('/api/verify-eu-id', async (req, res) => {
  try {
    const { proof, publicSignals } = req.body;
    
    // Verify the proof
    const result = await verifier.verify(proof, publicSignals);
    
    // Check document type
    const documentType = result.credentialSubject.document_type;
    const isEUID = documentType === DocumentType.EU_ID;
    
    if (result.isValid) {
      // EU ID cards provide additional data
      const userData = {
        verified: true,
        documentType: isEUID ? 'EU_ID' : 'PASSPORT',
        nullifier: result.nullifier,
        // EU ID specific fields
        firstName: result.credentialSubject.first_name,
        lastName: result.credentialSubject.last_name,
        nationality: result.credentialSubject.nationality,
        dateOfBirth: result.credentialSubject.date_of_birth,
        // Apply bonus for EU ID (if needed)
        verificationBonus: isEUID ? 1.5 : 1.0
      };
      
      res.json({ success: true, data: userData });
    } else {
      res.status(400).json({ 
        success: false, 
        errors: result.isValidDetails 
      });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});"""
        
        else:  # TypeScript
            return """import { 
  SelfBackendVerifier, 
  DocumentType, 
  VerificationResult,
  EUIDCredentialSubject 
} from '@selfxyz/core';

// Initialize verifier with EU ID support
const verifier = new SelfBackendVerifier(
  'https://forno.celo.org',
  'eu-id-verification'
);

// Configure for EU ID cards
verifier.setDocumentType(DocumentType.EU_ID);
verifier.setMinimumAge(18);

interface EUIDVerificationResult extends VerificationResult {
  credentialSubject: EUIDCredentialSubject;
}

// Express endpoint with TypeScript
app.post('/api/verify-eu-id', async (req, res) => {
  try {
    const { proof, publicSignals } = req.body;
    
    // Verify with proper typing
    const result = await verifier.verify(proof, publicSignals) as EUIDVerificationResult;
    
    // Check document type
    const isEUID = result.credentialSubject.document_type === DocumentType.EU_ID;
    
    if (result.isValid) {
      // Type-safe access to EU ID fields
      const verifiedUser = {
        verified: true,
        documentType: isEUID ? 'EU_ID' : 'PASSPORT',
        nullifier: result.nullifier,
        // EU ID specific fields with proper typing
        personalInfo: {
          firstName: result.credentialSubject.first_name,
          lastName: result.credentialSubject.last_name,
          dateOfBirth: result.credentialSubject.date_of_birth,
          nationality: result.credentialSubject.nationality,
          documentNumber: result.credentialSubject.document_number
        },
        // Different attestation ID for EU ID
        attestationId: isEUID ? 3 : 1, // 3 for EU ID, 1 for passport
        // Apply verification bonus
        multiplier: isEUID ? 1.5 : 1.0
      };
      
      // Store nullifier to prevent reuse
      await storeNullifier(result.nullifier, verifiedUser);
      
      res.json({ success: true, data: verifiedUser });
    } else {
      res.status(400).json({ 
        success: false, 
        errors: result.isValidDetails,
        documentType: result.credentialSubject.document_type 
      });
    }
  } catch (error) {
    console.error('EU ID verification error:', error);
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});"""
    
    else:  # smart-contract
        return """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@selfxyz/contracts/contracts/abstract/SelfVerificationRoot.sol";

/**
 * @title EUIDVerificationContract
 * @dev Contract supporting both EU ID cards and passports with different bonuses
 */
contract EUIDVerificationContract is SelfVerificationRoot {
    // Attestation IDs
    uint256 constant PASSPORT_ATTESTATION_ID = 1;
    uint256 constant EU_ID_ATTESTATION_ID = 3;
    
    // Document type bonuses
    uint256 constant PASSPORT_MULTIPLIER = 100; // 1x = 100%
    uint256 constant EU_ID_MULTIPLIER = 150;    // 1.5x = 150%
    
    // Track verified users with their document types
    mapping(address => uint256) public userDocumentType;
    mapping(uint256 => bool) public nullifierUsed;
    
    // Events
    event UserVerifiedWithEUID(
        address indexed user, 
        uint256 documentType, 
        uint256 multiplier
    );
    
    constructor(address _hubAddress) SelfVerificationRoot(_hubAddress) {}
    
    /**
     * @dev Verify user with EU ID card or passport
     * @param proof The Self proof containing verification data
     */
    function verifyWithDocument(
        SelfProof memory proof
    ) public {
        // 1. Verify the proof
        verifySelfProof(proof);
        
        // 2. Check nullifier hasn't been used
        require(!nullifierUsed[proof.nullifier], "Proof already used");
        nullifierUsed[proof.nullifier] = true;
        
        // 3. Validate scope
        require(
            proof.scope == keccak256("eu-id-verification"), 
            "Invalid scope"
        );
        
        // 4. Determine document type and multiplier
        uint256 multiplier;
        if (proof.attestationId == EU_ID_ATTESTATION_ID) {
            // EU ID card - higher bonus
            multiplier = EU_ID_MULTIPLIER;
            userDocumentType[msg.sender] = EU_ID_ATTESTATION_ID;
        } else if (proof.attestationId == PASSPORT_ATTESTATION_ID) {
            // Passport - standard bonus
            multiplier = PASSPORT_MULTIPLIER;
            userDocumentType[msg.sender] = PASSPORT_ATTESTATION_ID;
        } else {
            revert("Unsupported document type");
        }
        
        // 5. Apply verification logic with multiplier
        _applyVerificationBenefit(msg.sender, multiplier);
        
        emit UserVerifiedWithEUID(
            msg.sender, 
            proof.attestationId, 
            multiplier
        );
    }
    
    /**
     * @dev Apply benefits based on document type multiplier
     * @param user The verified user address
     * @param multiplier The bonus multiplier (100 = 1x, 150 = 1.5x)
     */
    function _applyVerificationBenefit(
        address user, 
        uint256 multiplier
    ) internal {
        // Example: Grant tokens with multiplier
        uint256 baseAmount = 1000 * 10**18; // 1000 tokens
        uint256 bonusAmount = (baseAmount * multiplier) / 100;
        
        // Your logic here: mint tokens, grant access, etc.
        // Example: token.mint(user, bonusAmount);
    }
    
    /**
     * @dev Check if user verified with EU ID
     * @param user The user address to check
     * @return bool True if verified with EU ID
     */
    function hasEUIDVerification(address user) public view returns (bool) {
        return userDocumentType[user] == EU_ID_ATTESTATION_ID;
    }
    
    /**
     * @dev Get user's verification multiplier
     * @param user The user address
     * @return uint256 The multiplier percentage
     */
    function getUserMultiplier(address user) public view returns (uint256) {
        uint256 docType = userDocumentType[user];
        if (docType == EU_ID_ATTESTATION_ID) {
            return EU_ID_MULTIPLIER;
        } else if (docType == PASSPORT_ATTESTATION_ID) {
            return PASSPORT_MULTIPLIER;
        }
        return 0; // Not verified
    }
}"""
    
    return f"Unsupported component: {component}"