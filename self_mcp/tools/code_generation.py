"""Tool for generating Self protocol integration code"""

from typing import Literal, Optional
from fastmcp import Context
from ..utils.github_client import get_docs_client, GitHubDocsClient


def get_playground_client() -> GitHubDocsClient:
    """Get GitHub client for playground repository"""
    return GitHubDocsClient(repo="selfxyz/playground", cache_ttl_minutes=60)


async def generate_verification_code(
    component: Literal["frontend-qr", "backend-verify", "smart-contract"],
    language: Literal["typescript", "javascript", "solidity"] = "typescript",
    ctx: Context = None
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
    playground_client = get_playground_client()
    
    # Map components to documentation files and playground examples
    component_map = {
        "frontend-qr": {
            "docs": "use-self/quickstart.md",
            "playground": "app/components/Playground.tsx"  # Frontend playground component
        },
        "backend-verify": {
            "docs": "use-self/quickstart.md",
            "playground": "pages/api/verify.ts"  # Real verification implementation
        },
        "smart-contract": {
            "docs": "contract-integration/basic-integration.md",
            "playground": None  # No smart contract examples in playground
        }
    }
    
    
    # Handle language compatibility
    if component == "smart-contract" and language != "solidity":
        language = "solidity"  # Force solidity for smart contracts
    elif component != "smart-contract" and language == "solidity":
        language = "typescript"  # Default to typescript for non-contracts
    
    # Get component configuration
    component_config = component_map.get(component)
    if not component_config:
        return f"Unknown component: {component}. Available: frontend-qr, backend-verify, smart-contract"
    
    # Fetch documentation content
    docs_content = None
    if component_config["docs"]:
        docs_content = await client.fetch_document(component_config["docs"])
    
    # Fetch playground content for backend verification
    playground_content = None
    if component_config["playground"]:
        playground_content = await playground_client.fetch_document(component_config["playground"])
    
    # Combine content from multiple sources
    combined_content = []
    if docs_content:
        combined_content.append(f"# Documentation Source\n{docs_content}")
    if playground_content:
        combined_content.append(f"# Playground Implementation\n{playground_content}")
    
    if not combined_content:
        return f"Failed to fetch content for {component}. Please try again later."
    
    # Extract relevant code sections based on component
    code_example = extract_code_example("\n\n".join(combined_content), component, language)
    
    if not code_example:
        # Fallback to enhanced examples with playground patterns
        code_example = generate_enhanced_example(component, language, playground_content)
    
    # Log to context if available (FastMCP 2.0 feature)
    if ctx:
        await ctx.info(f"Generated {component} code in {language}")
    
    return code_example


def extract_code_example(content: str, component: str, language: str) -> str:
    """Extract code example from documentation content and playground implementations"""
    lines = content.split('\n')
    in_code_block = False
    code_lines = []
    found_relevant_section = False
    playground_section = False
    
    # Keywords to look for based on component
    section_keywords = {
        "frontend-qr": ["QRCodeGenerator", "SelfQRcode", "frontend", "QR code"],
        "backend-verify": ["SelfBackendVerifier", "verify", "backend", "export default", "async function", "req", "res"],
        "smart-contract": ["contract", "onchain", "solidity"]
    }
    
    # Check if we're in playground section
    for line in lines:
        if "Playground Implementation" in line:
            playground_section = True
            break
    
    # For playground components, prioritize playground examples
    if component in ["backend-verify", "frontend-qr"] and playground_section:
        return extract_playground_code(content, language)
    
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


def extract_playground_code(content: str, language: str) -> Optional[str]:
    """Extract code from playground implementation"""
    lines = content.split('\n')
    in_playground = False
    code_lines = []
    
    for line in lines:
        if "Playground Implementation" in line:
            in_playground = True
            continue
        
        if in_playground:
            # Skip markdown headers and empty lines at start
            if line.startswith('#') or (not code_lines and not line.strip()):
                continue
            
            # Stop at next major section
            if line.startswith('#') and "Documentation" in line:
                break
            
            code_lines.append(line)
    
    if code_lines:
        # Clean up the code
        cleaned_lines = []
        for line in code_lines:
            # Remove markdown formatting
            if line.startswith('```'):
                continue
            cleaned_lines.append(line)
        
        # Remove leading/trailing empty lines
        while cleaned_lines and not cleaned_lines[0].strip():
            cleaned_lines.pop(0)
        while cleaned_lines and not cleaned_lines[-1].strip():
            cleaned_lines.pop()
        
        if cleaned_lines:
            return '\n'.join(cleaned_lines)
    
    return None


def generate_enhanced_example(component: str, language: str, playground_content: Optional[str] = None) -> str:
    """Generate enhanced example incorporating playground patterns"""
    if component == "backend-verify" and playground_content:
        return generate_playground_inspired_backend(language, playground_content)
    elif component == "frontend-qr" and playground_content:
        return generate_playground_inspired_frontend(language, playground_content)
    else:
        return generate_basic_example(component, language)


def generate_playground_inspired_backend(language: str, playground_content: Optional[str]) -> str:
    """Generate backend verification code inspired by playground implementation"""
    return f"""// {language.upper()}: Self Backend Verification (Playground-Inspired)

import {{ SelfBackendVerifier, AttestationId, UserIdType }} from '@selfxyz/core';
import type {{ NextApiRequest, NextApiResponse }} from 'next';

// Configuration storage implementation (inspired by playground patterns)
class PlaygroundConfigStorage {{
  async getConfig(configId: string) {{
    // Return configuration based on your app's requirements
    return {{
      olderThan: 18,
      excludedCountries: ['IRN', 'PRK'],
      ofac: true,
      name: true,
      nationality: true
    }};
  }}
  
  async getActionId(userIdentifier: string, userDefinedData: any) {{
    // Generate action ID for tracking
    return `action_${{userIdentifier}}_${{Date.now()}}`;
  }}
}}

// Define allowed attestation types (from playground)
const allowedIds = new Map<number, boolean>();
allowedIds.set(1, true); // Passport
allowedIds.set(2, true); // EU ID Card

// Initialize verifier with playground-inspired configuration
const selfBackendVerifier = new SelfBackendVerifier(
  "my-app-scope", // Your app's scope
  "https://myapp.com/api/verify", // Your verification endpoint
  false, // Use real passports (set to true for testing)
  allowedIds,
  new PlaygroundConfigStorage(),
  UserIdType.UUID
);

// Main verification handler (playground pattern)
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {{
  if (req.method !== 'POST') {{
    return res.status(405).json({{ error: 'Method not allowed' }});
  }}

  try {{
    const {{ 
      attestationId, 
      proof, 
      pubSignals, 
      userContextData,
      nullifier 
    }} = req.body;

    // Validate required fields
    if (!attestationId || !proof || !pubSignals) {{
      return res.status(400).json({{ 
        error: 'Missing required fields: attestationId, proof, pubSignals' 
      }});
    }}

    // Verify the proof using Self backend verifier
    const result = await selfBackendVerifier.verify(
      attestationId,
      proof,
      pubSignals,
      userContextData
    );

    if (result.isValidDetails.isValid) {{
      // Store nullifier to prevent reuse (playground pattern)
      await storeNullifier(nullifier);
      
      // Return success response
      res.status(200).json({{
        status: 'success',
        userId: result.userData.userIdentifier,
        details: result.discloseOutput,
        timestamp: new Date().toISOString()
      }});
    }} else {{
      res.status(400).json({{
        status: 'error',
        message: 'Verification failed',
        details: result.isValidDetails
      }});
    }}
  }} catch (error) {{
    console.error('Verification error:', error);
    res.status(500).json({{
      error: 'Internal server error',
      message: error instanceof Error ? error.message : 'Unknown error'
    }});
  }}
}}

// Helper function to store nullifiers (prevent proof reuse)
async function storeNullifier(nullifier: string): Promise<void> {{
  // Implement your nullifier storage logic here
  // This prevents the same proof from being used multiple times
  console.log('Storing nullifier:', nullifier);
}}

// Optional: Add CORS headers for frontend integration
export const config = {{
  api: {{
    bodyParser: {{
      sizeLimit: '1mb',
    }},
  }},
}};"""


def generate_basic_example(component: str, language: str) -> str:
    """Generate basic example if extraction fails"""
    if component == "frontend-qr":
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
    
    elif component == "backend-verify":
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


async def fetch_playground_example(
    example_type: Literal["verify", "save-options", "verification-flow", "frontend-component", "app-structure"],
    ctx: Context = None
) -> str:
    """
    Fetch specific playground examples for learning implementation patterns.
    
    Args:
        example_type: Type of playground example to fetch
        - 'verify': Backend verification implementation
        - 'save-options': Options saving implementation  
        - 'verification-flow': Complete verification flow
        - 'frontend-component': Frontend playground component
        - 'app-structure': App directory structure
        
    Returns:
        Complete playground implementation code with comments
    """
    playground_client = get_playground_client()
    
    # Map example types to playground files
    example_map = {
        "verify": "pages/api/verify.ts",
        "save-options": "pages/api/saveOptions.ts", 
        "verification-flow": "pages/api/verify.ts",
        "frontend-component": "app/components/Playground.tsx",
        "app-structure": "app"
    }
    
    file_path = example_map.get(example_type)
    if not file_path:
        return f"Unknown example type: {example_type}. Available: {', '.join(example_map.keys())}"
    
    # Fetch the playground code
    content = await playground_client.fetch_document(file_path)
    if not content:
        return f"Failed to fetch playground example for {example_type}. Please try again later."
    
    # Log to context if available
    if ctx:
        await ctx.info(f"Fetched playground example: {example_type}")
    
    # Format the response with context
    return f"""# Self Playground Example: {example_type.replace('-', ' ').title()}

This is a real-world implementation from the Self Playground repository that demonstrates best practices for {example_type.replace('-', ' ')}.

**Source**: https://github.com/selfxyz/playground/blob/main/{file_path}

```typescript
{content}
```

## Key Implementation Notes

This playground example shows:
- Real-world error handling patterns
- Production-ready code structure  
- Best practices for Self protocol integration
- Proper TypeScript typing
- Next.js API route patterns

Use this as a reference for implementing similar functionality in your application."""


def generate_playground_inspired_frontend(language: str, playground_content: Optional[str]) -> str:
    """Generate frontend QR code inspired by playground implementation"""
    return f"""// {language.upper()}: Self Frontend QR Component (Playground-Inspired)

import React, {{ useState, useEffect }} from 'react';
import SelfQRcodeWrapper, {{ SelfAppBuilder }} from '@selfxyz/qrcode';
import {{ v4 as uuidv4 }} from 'uuid';

// Playground-inspired configuration
interface PlaygroundConfig {{
  appName: string;
  scope: string;
  endpoint: string;
  disclosures: {{
    minimumAge?: number;
    excludedCountries?: string[];
    ofac?: boolean;
    name?: boolean;
    nationality?: boolean;
  }};
}}

// Main playground component (inspired by playground implementation)
export default function PlaygroundComponent() {{
  const [userId, setUserId] = useState<string>('');
  const [config, setConfig] = useState<PlaygroundConfig>({{
    appName: "My Self App",
    scope: "my-app-scope",
    endpoint: "https://myapp.com/api/verify",
    disclosures: {{
      minimumAge: 18,
      excludedCountries: ['IRN', 'PRK'],
      ofac: true,
      name: true,
      nationality: true
    }}
  }});
  
  const [verificationStatus, setVerificationStatus] = useState<'idle' | 'verifying' | 'success' | 'error'>('idle');
  const [verificationResult, setVerificationResult] = useState<any>(null);

  // Generate user ID on component mount (playground pattern)
  useEffect(() => {{
    setUserId(uuidv4());
  }}, []);

  // Create Self app configuration (playground-inspired)
  const selfApp = new SelfAppBuilder({{
    appName: config.appName,
    scope: config.scope,
    endpoint: config.endpoint,
    userId,
    disclosures: config.disclosures
  }}).build();

  // Handle verification success (playground pattern)
  const handleVerificationSuccess = (result: any) => {{
    setVerificationStatus('success');
    setVerificationResult(result);
    console.log('Verification successful:', result);
  }};

  // Handle verification error (playground pattern)
  const handleVerificationError = (error: any) => {{
    setVerificationStatus('error');
    console.error('Verification failed:', error);
  }};

  // Handle verification start (playground pattern)
  const handleVerificationStart = () => {{
    setVerificationStatus('verifying');
    setVerificationResult(null);
  }};

  return (
    <div className="playground-container">
      <div className="playground-header">
        <h1>Self Protocol Playground</h1>
        <p>Test Self verification with real-world patterns</p>
      </div>

      <div className="playground-content">
        <div className="config-panel">
          <h3>Configuration</h3>
          <div className="config-item">
            <label>App Name:</label>
            <input
              type="text"
              value={{config.appName}}
              onChange={{e => setConfig(prev => ({{ ...prev, appName: e.target.value }}))}}
            />
          </div>
          <div className="config-item">
            <label>Scope:</label>
            <input
              type="text"
              value={{config.scope}}
              onChange={{e => setConfig(prev => ({{ ...prev, scope: e.target.value }}))}}
            />
          </div>
          <div className="config-item">
            <label>Endpoint:</label>
            <input
              type="text"
              value={{config.endpoint}}
              onChange={{e => setConfig(prev => ({{ ...prev, endpoint: e.target.value }}))}}
            />
          </div>
        </div>

        <div className="qr-section">
          <h3>Verification QR Code</h3>
          <div className="qr-container">
            <SelfQRcodeWrapper
              selfApp={{selfApp}}
              onSuccess={{handleVerificationSuccess}}
              onError={{handleVerificationError}}
              onStart={{handleVerificationStart}}
            />
          </div>
        </div>

        <div className="status-section">
          <h3>Verification Status</h3>
          <div className={{`status-indicator ${{verificationStatus}}`}}>
            {{verificationStatus === 'idle' && 'Ready to verify'}}
            {{verificationStatus === 'verifying' && 'Verifying...'}}
            {{verificationStatus === 'success' && 'Verification successful!'}}
            {{verificationStatus === 'error' && 'Verification failed'}}
          </div>
          
          {{verificationResult && (
            <div className="verification-result">
              <h4>Verification Result:</h4>
              <pre>{{JSON.stringify(verificationResult, null, 2)}}</pre>
            </div>
          )}}
        </div>
      </div>
    </div>
  );
}}"""
