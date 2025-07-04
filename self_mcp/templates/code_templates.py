"""Code templates for Self protocol components based on official documentation"""

CODE_TEMPLATES = {
    "frontend-qr": {
        "typescript": """'use client';

import React, { useState, useEffect } from 'react';
import SelfQRcodeWrapper, { SelfAppBuilder } from '@selfxyz/qrcode';
import { v4 as uuidv4 } from 'uuid';

// Self QR code component for {component_context}
function VerificationQR() {
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    // Generate user ID when component mounts
    setUserId(uuidv4());
  }, []);

  if (!userId) return null;

  // Create SelfApp configuration
  const selfApp = new SelfAppBuilder({
    appName: "My Application",
    scope: "my-application-scope",
    endpoint: "https://myapp.com/api/verify",
    userId,
    version: 2, // V2 protocol
    userDefinedData: Buffer.from(JSON.stringify({
      action: 'verification',
      timestamp: Date.now()
    })).toString('hex').padEnd(128, '0'),
    disclosures: {
      minimumAge: 18,
      excludedCountries: ['IRN', 'PRK'],
      ofac: true,
      name: true,
      nationality: true
    }
  }).build();

  return (
    <div className="verification-container">
      <h1>Verify Your Identity</h1>
      <p>Scan this QR code with the Self app to verify your identity</p>
      
      <SelfQRcodeWrapper
        selfApp={selfApp}
        onSuccess={() => {
          console.log("Verification successful!");
          // Handle successful verification
        }}
        size={350}
      />
      
      <p className="text-sm text-gray-500">
        User ID: {userId.substring(0, 8)}...
      </p>
    </div>
  );
}

export default VerificationQR;""",
        "javascript": """import React, { useState, useEffect } from 'react';
import SelfQRcodeWrapper, { SelfAppBuilder } from '@selfxyz/qrcode';
import { v4 as uuidv4 } from 'uuid';

// Self QR code component for {component_context}
function VerificationQR() {
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    // Generate user ID when component mounts
    setUserId(uuidv4());
  }, []);

  if (!userId) return null;

  // Create SelfApp configuration
  const selfApp = new SelfAppBuilder({
    appName: "My Application",
    scope: "my-application-scope",
    endpoint: "https://myapp.com/api/verify",
    userId,
    version: 2, // V2 protocol
    userDefinedData: Buffer.from(JSON.stringify({
      action: 'verification',
      timestamp: Date.now()
    })).toString('hex').padEnd(128, '0'),
    disclosures: {
      minimumAge: 18,
      excludedCountries: ['IRN', 'PRK'],
      ofac: true,
      name: true,
      nationality: true
    }
  }).build();

  return (
    React.createElement('div', { className: 'verification-container' },
      React.createElement('h1', null, 'Verify Your Identity'),
      React.createElement('p', null, 'Scan this QR code with the Self app to verify your identity'),
      React.createElement(SelfQRcodeWrapper, {
        selfApp: selfApp,
        onSuccess: () => {
          console.log('Verification successful!');
          // Handle successful verification
        },
        size: 350
      }),
      React.createElement('p', { className: 'text-sm text-gray-500' },
        'User ID: ' + userId.substring(0, 8) + '...'
      )
    )
  );
}

export default VerificationQR;"""
    },
    "backend-verify": {
        "typescript": """import { NextApiRequest, NextApiResponse } from 'next';
import { 
  SelfBackendVerifier, 
  AttestationId, 
  UserIdType,
  IConfigStorage,
  ConfigMismatchError 
} from '@selfxyz/core';

// Configuration storage implementation
class ConfigStorage implements IConfigStorage {
  async getConfig(configId: string) {
    return {
      olderThan: 18,
      excludedCountries: ['IRN', 'PRK'],
      ofac: true
    };
  }
  
  async getActionId(userIdentifier: string, userDefinedData: string) {
    return 'default_config';
  }
}

// Initialize verifier once
const allowedIds = new Map();
allowedIds.set(1, true); // Accept passports
allowedIds.set(2, true); // Accept EU ID cards

const selfBackendVerifier = new SelfBackendVerifier(
  'my-application-scope',
  'https://myapp.com/api/verify',
  false,
  allowedIds,
  new ConfigStorage(),
  UserIdType.UUID
);

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    try {
      const { attestationId, proof, pubSignals, userContextData } = req.body;

      if (!attestationId || !proof || !pubSignals || !userContextData) {
        return res.status(400).json({ message: 'Missing required fields' });
      }

      // Verify the proof
      const result = await selfBackendVerifier.verify(
        attestationId,
        proof,
        pubSignals,
        userContextData
      );
      
      if (result.isValidDetails.isValid) {
        // Return successful verification response
        return res.status(200).json({
          status: 'success',
          result: true,
          credentialSubject: result.discloseOutput
        });
      } else {
        // Return failed verification response
        return res.status(400).json({
          status: 'error',
          result: false,
          message: 'Verification failed',
          details: result.isValidDetails
        });
      }
    } catch (error) {
      if (error instanceof ConfigMismatchError) {
        return res.status(400).json({
          status: 'error',
          result: false,
          message: 'Configuration mismatch',
          issues: error.issues
        });
      }
      
      console.error('Error verifying proof:', error);
      return res.status(500).json({
        status: 'error',
        result: false,
        message: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  } else {
    return res.status(405).json({ message: 'Method not allowed' });
  }
}""",
        "javascript": """import { 
  SelfBackendVerifier, 
  AttestationId, 
  UserIdType,
  ConfigMismatchError 
} from '@selfxyz/core';

// Configuration storage implementation
class SimpleConfigStorage {
  async getConfig(configId) {
    return {
      olderThan: 18,
      excludedCountries: ['IRN', 'PRK'],
      ofac: true
    };
  }
  
  async getActionId(userIdentifier, userDefinedData) {
    return 'default_config';
  }
}

// Define which attestation types to accept
const allowedIds = new Map();
allowedIds.set(1, true); // 1 = passport
allowedIds.set(2, true); // 2 = EU ID card

// Create configuration storage
const configStorage = new SimpleConfigStorage();

// Initialize the verifier
const selfBackendVerifier = new SelfBackendVerifier(
  "my-app-scope",
  "https://myapp.com/api/verify",
  false,
  allowedIds,
  configStorage,
  UserIdType.UUID
);

// Express.js endpoint example
export async function POST(request) {
  try {
    const { attestationId, proof, pubSignals, userContextData } = await request.json();
    
    const result = await selfBackendVerifier.verify(
      attestationId,
      proof,
      pubSignals,
      userContextData
    );
    
    if (result.isValidDetails.isValid) {
      console.log('Verification successful');
      console.log('User ID:', result.userData.userIdentifier);
      
      return Response.json({
        verified: true,
        userIdentifier: result.userData.userIdentifier,
        nationality: result.discloseOutput.nationality,
        ageVerified: result.isValidDetails.isOlderThanValid
      });
    } else {
      return Response.json({ verified: false }, { status: 400 });
    }
  } catch (error) {
    if (error.name === 'ConfigMismatchError') {
      console.error('Configuration mismatch:', error.issues);
      return Response.json({ error: 'Configuration mismatch' }, { status: 400 });
    }
    
    console.error('Verification error:', error);
    return Response.json({ error: error.message }, { status: 500 });
  }
}"""
    },
    "smart-contract": {
        "solidity": """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {SelfVerificationRoot} from "@selfxyz/contracts/contracts/abstract/SelfVerificationRoot.sol";
import {ISelfVerificationRoot} from "@selfxyz/contracts/contracts/interfaces/ISelfVerificationRoot.sol";
import {SelfStructs} from "@selfxyz/contracts/contracts/libraries/SelfStructs.sol";
import {AttestationId} from "@selfxyz/contracts/contracts/constants/AttestationId.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

// V2 Contract for {component_context}
contract ExampleV2 is SelfVerificationRoot, Ownable {
    // Your app-specific configuration ID
    bytes32 public configId;
    
    // Track verified users
    mapping(address => bool) public verifiedUsers;
    
    // Store verification details (optional)
    mapping(uint256 => ISelfVerificationRoot.GenericDiscloseOutputV2) public verificationDetails;
    
    // Events
    event UserVerified(
        address indexed user,
        uint256 indexed nullifier,
        bytes32 indexed attestationId,
        uint256 userIdentifier
    );
    
    constructor(
        address _identityVerificationHubV2, // V2 Hub address
        uint256 _scope // Application-specific scope identifier
    ) 
        SelfVerificationRoot(_identityVerificationHubV2, _scope)
        Ownable(msg.sender)
    {
        // Initialize with empty configId - set it using tools.self.xyz
    }

    // Required: Override to provide configId for verification
    function getConfigId(
        bytes32 destinationChainId,
        bytes32 userIdentifier, 
        bytes memory userDefinedData // Custom data from QR code
    ) public view override returns (bytes32) {
        // Return your app's configuration ID
        return configId;
    }
    
    // Set configuration ID (only owner)
    function setConfigId(bytes32 _configId) external onlyOwner {
        configId = _configId;
    }

    // Override to handle successful verification
    function customVerificationHook(
        ISelfVerificationRoot.GenericDiscloseOutputV2 memory output,
        bytes memory userData
    ) internal virtual override {
        // Your custom business logic here
        // Example: Store verified user data, mint NFT, transfer tokens, etc.
        
        // Store verification details for later use
        verificationDetails[output.nullifier] = output;
        
        // Mark user as verified
        verifiedUsers[msg.sender] = true;
        
        // Emit event
        emit UserVerified(
            msg.sender,
            output.nullifier,
            output.attestationId,
            output.userIdentifier
        );
        
        // Access verified data:
        // output.userIdentifier - user's unique identifier
        // output.name - verified name
        // output.nationality - verified nationality
        // output.dateOfBirth - verified birth date
        // output.olderThan - age verification result
        // output.ofac - OFAC check results
        
        // Example: Simple verification check
        require(bytes(output.nationality).length > 0, "Nationality required");
    }
    
    // Check if user is verified
    function isUserVerified(address user) public view returns (bool) {
        return verifiedUsers[user];
    }
    
    // Get verification details by nullifier
    function getVerificationDetails(uint256 nullifier) 
        public 
        view 
        returns (ISelfVerificationRoot.GenericDiscloseOutputV2 memory) 
    {
        return verificationDetails[nullifier];
    }
}"""
    }
}