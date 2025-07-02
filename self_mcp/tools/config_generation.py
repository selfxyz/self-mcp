"""Tool for generating Self protocol verification configurations"""

from typing import Dict, Any
import json


async def generate_verification_config(
    requirements: Dict[str, Any]
) -> str:
    """Generate a complete verification configuration based on requirements"""
    
    config = {
        "frontend": {
            "scope": f"{requirements.get('app_name', 'my-app').lower().replace(' ', '-')}-v1",
            "disclosures": {}
        },
        "backend": {
            "checks": []
        }
    }
    
    # Build configuration based on requirements
    if requirements.get("minimum_age"):
        config["frontend"]["disclosures"]["minimumAge"] = requirements["minimum_age"]
        config["backend"]["checks"].append(f"verifier.setMinimumAge({requirements['minimum_age']})")
    
    if requirements.get("nationality_check"):
        config["frontend"]["disclosures"]["nationality"] = True
        config["backend"]["checks"].append(f"verifier.setNationality('{requirements['nationality_check']}')")
    
    if requirements.get("exclude_countries"):
        countries = requirements["exclude_countries"]
        config["frontend"]["disclosures"]["excludedCountries"] = countries
        config["backend"]["checks"].append(f"verifier.excludeCountries({', '.join(f'"{c}"' for c in countries)})")
    
    if requirements.get("ofac_check"):
        config["frontend"]["disclosures"]["ofac"] = True
        config["backend"]["checks"].append("verifier.enableNameAndDobOfacCheck()")
    
    return f"""## Generated Self Verification Configuration

### Frontend Configuration
```typescript
const selfApp = new SelfAppBuilder({{
  appName: '{requirements.get('app_name', 'My Application')}',
  scope: '{config['frontend']['scope']}',
  endpoint: '{requirements.get('endpoint', '/api/verify')}',
  disclosures: {json.dumps(config['frontend']['disclosures'], indent=2).replace('"', '')}
}}).build();
```

### Backend Configuration
```typescript
const verifier = new SelfBackendVerifier(
  '{requirements.get('rpc_url', 'https://forno.celo.org')}',
  '{config['frontend']['scope']}'
);

{chr(10).join(config['backend']['checks'])}

app.post('{requirements.get('endpoint', '/api/verify')}', async (req, res) => {{
  const {{ proof, publicSignals }} = req.body;
  const result = await verifier.verify(proof, publicSignals);
  
  if (result.isValid) {{
    // Verification passed
    res.json({{
      success: true,
      userId: result.userId,
      nullifier: result.nullifier
    }});
  }} else {{
    res.status(400).json({{
      success: false,
      errors: result.isValidDetails
    }});
  }}
}});
```

### Important Notes
- Scope must match exactly between frontend and backend
- Store nullifiers to prevent proof reuse
- Only request necessary disclosures for privacy
"""