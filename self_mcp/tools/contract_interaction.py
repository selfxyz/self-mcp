"""Tools for interacting with Self protocol smart contracts."""

import json
from typing import Optional, List, Dict, Any, Literal
from pydantic import Field
from web3 import Web3
from eth_utils import is_address
from ..utils.networks import CELO_NETWORKS
from ..utils.constants_abi import HUB_CONTRACT_ABI

# Country code mappings (ISO 3166-1 alpha-3)
COUNTRY_CODES = {
    "USA": "United States",
    "GBR": "United Kingdom", 
    "CAN": "Canada",
    "AUS": "Australia",
    "NZL": "New Zealand",
    "IRN": "Iran",
    "PRK": "North Korea",
    "CUB": "Cuba",
    "SYR": "Syria",
    "RUS": "Russia",
    "CHN": "China",
    "IND": "India",
    "JPN": "Japan",
    "KOR": "South Korea",
    "DEU": "Germany",
    "FRA": "France",
    "ITA": "Italy",
    "ESP": "Spain",
    "BRA": "Brazil",
    "ARG": "Argentina",
    "MEX": "Mexico",
    # Add more as needed
}


def format_countries_list(countries: List[str]) -> List[int]:
    """Formats a list of 3-letter country codes into a list of integers for packing."""
    MAX_LENGTH = 40
    
    if len(countries) > MAX_LENGTH:
        raise ValueError(f"Maximum {MAX_LENGTH} countries allowed")
    
    # Validate country codes
    for country in countries:
        if len(country) != 3:
            raise ValueError(f"Invalid country code: {country}. Must be 3 characters.")
    
    # Pad the list to MAX_LENGTH
    padded = countries + [''] * (MAX_LENGTH - len(countries))
    
    # Convert to bytes
    result = []
    for country in padded:
        chars = country.ljust(3, '\0')
        result.extend([ord(c) for c in chars])
    
    return result


def unpack_countries_from_config(packed_countries: List[int]) -> List[str]:
    """Unpacks the country list from the smart contract format."""
    countries = []
    
    # Each uint256 contains up to 30 characters (10 countries)
    for packed_value in packed_countries:
        # Convert the packed value to bytes
        for i in range(10):  # 10 countries per uint256
            # Extract 3 characters for each country
            country = ""
            for j in range(3):
                byte_index = i * 3 + j
                char_code = (packed_value >> (byte_index * 8)) & 0xFF
                if char_code == 0:
                    break
                country += chr(char_code)
            
            if country and country != '\0\0\0':
                countries.append(country)
    
    return countries


async def generate_scope_hash(
    address_or_url: str = Field(description="Ethereum address (0x...) or HTTPS URL"),
    scope_seed: str = Field(description="Scope seed string (max 20 chars, lowercase)")
) -> Dict[str, str]:
    """
    Generate a scope hash for Self verification, replicating hashEndpointWithScope.
    
    Args:
        address_or_url: Either an Ethereum address (0x...) or HTTPS URL
        scope_seed: Scope identifier (max 20 chars, lowercase ASCII only)
        
    Returns:
        Dictionary with scope_hash, validation status, and input type
    """
    # Validate inputs
    errors = []
    input_type = ""
    
    # Validate address_or_url
    if address_or_url.startswith("0x"):
        if is_address(address_or_url):
            input_type = "address"
        else:
            errors.append("Invalid Ethereum address format")
    elif address_or_url.startswith("https://"):
        if len(address_or_url) > 8:  # More than just "https://"
            input_type = "url"
        else:
            errors.append("Invalid HTTPS URL")
    else:
        errors.append("Input must be an Ethereum address (0x...) or HTTPS URL")
    
    # Validate scope_seed
    if not scope_seed:
        errors.append("Scope seed cannot be empty")
    elif len(scope_seed) > 20:
        errors.append("Scope seed must be 20 characters or less")
    elif not all(c.islower() or c.isdigit() or c in " -_.,!?" for c in scope_seed):
        errors.append("Scope seed must contain only lowercase ASCII characters")
    
    if errors:
        return {
            "error": "; ".join(errors),
            "scope_hash": "",
            "validation": "invalid",
            "input_type": input_type
        }
    
    # Generate the hash (keccak256 of concatenated values)
    # This replicates the hashEndpointWithScope function
    combined = address_or_url.lower() + scope_seed
    scope_hash = Web3.keccak(text=combined).hex()
    
    return {
        "scope_hash": scope_hash,
        "validation": "valid",
        "input_type": input_type,
        "address_or_url": address_or_url,
        "scope_seed": scope_seed,
        "tools_url": f"https://tools.self.xyz/#scope-generator"
    }


async def generate_config_id(
    minimum_age: Optional[int] = Field(default=0, description="Minimum age requirement (0 to disable)"),
    excluded_countries: Optional[List[str]] = Field(default=[], description="List of excluded 3-letter country codes"),
    ofac_enabled: Optional[List[bool]] = Field(default=[False, False, False], description="OFAC settings [basic, enhanced, comprehensive]"),
    network: Literal["mainnet", "testnet"] = Field(default="mainnet", description="Network to check config existence")
) -> Dict[str, Any]:
    """
    Generate a configuration ID for Self protocol verification.
    
    This replicates the generateConfigId function from the smart contract.
    """
    # Validate inputs
    if minimum_age < 0 or minimum_age > 150:
        return {"error": "Minimum age must be between 0 and 150"}
    
    if len(ofac_enabled) != 3:
        ofac_enabled = [False, False, False]
    
    # Create the config struct matching Solidity
    config = {
        "olderThanEnabled": minimum_age > 0,
        "olderThan": minimum_age,
        "forbiddenCountriesEnabled": len(excluded_countries) > 0,
        "forbiddenCountriesListPacked": [0, 0, 0, 0],
        "ofacEnabled": ofac_enabled
    }
    
    # Pack countries if provided
    if excluded_countries:
        try:
            country_bytes = format_countries_list(excluded_countries)
            # Pack into four uint256 values
            for i in range(4):
                packed_value = 0
                for j in range(30):  # 30 bytes per uint256
                    byte_index = i * 30 + j
                    if byte_index < len(country_bytes):
                        packed_value |= country_bytes[byte_index] << (j * 8)
                config["forbiddenCountriesListPacked"][i] = packed_value
        except ValueError as e:
            return {"error": str(e)}
    
    # Generate config ID using keccak256
    # Pack the data according to Solidity's abi.encodePacked
    packed_data = bytearray()
    
    # bool olderThanEnabled
    packed_data.extend(config["olderThanEnabled"].to_bytes(1, 'big'))
    # uint256 olderThan
    packed_data.extend(config["olderThan"].to_bytes(32, 'big'))
    # bool forbiddenCountriesEnabled  
    packed_data.extend(config["forbiddenCountriesEnabled"].to_bytes(1, 'big'))
    # uint256[4] forbiddenCountriesListPacked
    for packed_country in config["forbiddenCountriesListPacked"]:
        packed_data.extend(packed_country.to_bytes(32, 'big'))
    # bool[3] ofacEnabled
    for ofac in config["ofacEnabled"]:
        packed_data.extend(ofac.to_bytes(1, 'big'))
    
    config_id = Web3.keccak(bytes(packed_data)).hex()
    
    # Check if config exists on chain
    exists_on_chain = False
    try:
        w3 = Web3(Web3.HTTPProvider(CELO_NETWORKS[network]["rpc"]))
        hub_address = CELO_NETWORKS[network]["contracts"]["hub"]
        hub_contract = w3.eth.contract(address=hub_address, abi=json.loads(HUB_CONTRACT_ABI))
        exists_on_chain = hub_contract.functions.verificationConfigV2Exists(config_id).call()
    except Exception as e:
        print(f"Error checking config existence: {e}")
    
    # Generate URL parameters for tools.self.xyz
    url_params = []
    if minimum_age > 0:
        url_params.append(f"age={minimum_age}")
    if excluded_countries:
        url_params.append(f"countries={','.join(excluded_countries)}")
    if any(ofac_enabled):
        url_params.append(f"ofac={','.join(str(o).lower() for o in ofac_enabled)}")
    
    deploy_url = f"https://tools.self.xyz/?{('&'.join(url_params))}"
    
    return {
        "config_id": config_id,
        "exists_on_chain": exists_on_chain,
        "network": network,
        "configuration": {
            "minimum_age": minimum_age if minimum_age > 0 else "Disabled",
            "excluded_countries": excluded_countries if excluded_countries else "None",
            "ofac_settings": {
                "basic": ofac_enabled[0],
                "enhanced": ofac_enabled[1],
                "comprehensive": ofac_enabled[2]
            }
        },
        "deploy_url": deploy_url if not exists_on_chain else None,
        "message": "Config already exists on-chain" if exists_on_chain else "Config does not exist yet, use deploy_url to create it"
    }


async def read_hub_config(
    config_id: str = Field(description="Configuration ID to read (0x...)"),
    network: Literal["mainnet", "testnet"] = Field(default="mainnet", description="Network to read from")
) -> Dict[str, Any]:
    """
    Read configuration from Self protocol Hub contract with full decoding.
    """
    # Validate config ID
    if not config_id.startswith("0x") or len(config_id) != 66:
        return {"error": "Invalid config ID format. Must be 0x followed by 64 hex characters."}
    
    try:
        # Set up web3 connection
        w3 = Web3(Web3.HTTPProvider(CELO_NETWORKS[network]["rpc"]))
        hub_address = CELO_NETWORKS[network]["contracts"]["hub"]
        hub_contract = w3.eth.contract(address=hub_address, abi=json.loads(HUB_CONTRACT_ABI))
        
        # Check if config exists
        exists = hub_contract.functions.verificationConfigV2Exists(config_id).call()
        if not exists:
            return {
                "error": f"Configuration {config_id} does not exist on {network}",
                "config_id": config_id,
                "network": network,
                "exists": False
            }
        
        # Read config from the contract
        config = hub_contract.functions.getVerificationConfigV2(config_id).call()
        
        # Unpack the response
        older_than_enabled = config[0]
        older_than = config[1]
        forbidden_countries_enabled = config[2]
        forbidden_countries_packed = config[3]
        ofac_enabled = config[4]
        
        # Decode countries if enabled
        excluded_countries = []
        excluded_countries_readable = []
        if forbidden_countries_enabled:
            excluded_countries = unpack_countries_from_config(forbidden_countries_packed)
            # Map to readable names
            excluded_countries_readable = [
                {"code": code, "name": COUNTRY_CODES.get(code, code)} 
                for code in excluded_countries
            ]
        
        return {
            "config_id": config_id,
            "network": network,
            "exists": True,
            "configuration": {
                "minimum_age": {
                    "enabled": older_than_enabled,
                    "value": older_than if older_than_enabled else None,
                    "display": f"{older_than} years" if older_than_enabled else "Disabled"
                },
                "excluded_countries": {
                    "enabled": forbidden_countries_enabled,
                    "codes": excluded_countries,
                    "readable": excluded_countries_readable,
                    "count": len(excluded_countries),
                    "display": f"{len(excluded_countries)} countries excluded" if forbidden_countries_enabled else "No restrictions"
                },
                "ofac_settings": {
                    "basic": ofac_enabled[0],
                    "enhanced": ofac_enabled[1],
                    "comprehensive": ofac_enabled[2],
                    "any_enabled": any(ofac_enabled),
                    "display": "Enabled" if any(ofac_enabled) else "Disabled"
                }
            },
            "hub_address": hub_address,
            "explorer_url": f"{CELO_NETWORKS[network]['explorer']}/address/{hub_address}"
        }
        
    except Exception as e:
        return {
            "error": f"Error reading config: {str(e)}",
            "config_id": config_id,
            "network": network
        }


async def list_country_codes(
    search: Optional[str] = Field(default=None, description="Search term to filter countries")
) -> List[Dict[str, str]]:
    """
    List available country codes for exclusion in Self protocol.
    
    Returns ISO 3166-1 alpha-3 country codes with their names.
    """
    # Extended country list
    all_countries = {
        **COUNTRY_CODES,
        "AFG": "Afghanistan",
        "ALB": "Albania",
        "DZA": "Algeria",
        "AND": "Andorra",
        "AGO": "Angola",
        "ATG": "Antigua and Barbuda",
        "ARM": "Armenia",
        "AUT": "Austria",
        "AZE": "Azerbaijan",
        "BHS": "Bahamas",
        "BHR": "Bahrain",
        "BGD": "Bangladesh",
        "BRB": "Barbados",
        "BLR": "Belarus",
        "BEL": "Belgium",
        "BLZ": "Belize",
        "BEN": "Benin",
        "BTN": "Bhutan",
        "BOL": "Bolivia",
        "BIH": "Bosnia and Herzegovina",
        "BWA": "Botswana",
        "BRN": "Brunei",
        "BGR": "Bulgaria",
        "BFA": "Burkina Faso",
        "BDI": "Burundi",
        "CPV": "Cabo Verde",
        "KHM": "Cambodia",
        "CMR": "Cameroon",
        "CAF": "Central African Republic",
        "TCD": "Chad",
        "CHL": "Chile",
        "COL": "Colombia",
        "COM": "Comoros",
        "COG": "Congo",
        "CRI": "Costa Rica",
        "HRV": "Croatia",
        "CYP": "Cyprus",
        "CZE": "Czech Republic",
        "DNK": "Denmark",
        "DJI": "Djibouti",
        "DMA": "Dominica",
        "DOM": "Dominican Republic",
        "ECU": "Ecuador",
        "EGY": "Egypt",
        "SLV": "El Salvador",
        "GNQ": "Equatorial Guinea",
        "ERI": "Eritrea",
        "EST": "Estonia",
        "SWZ": "Eswatini",
        "ETH": "Ethiopia",
        "FJI": "Fiji",
        "FIN": "Finland",
        "GAB": "Gabon",
        "GMB": "Gambia",
        "GEO": "Georgia",
        "GHA": "Ghana",
        "GRC": "Greece",
        "GRD": "Grenada",
        "GTM": "Guatemala",
        "GIN": "Guinea",
        "GNB": "Guinea-Bissau",
        "GUY": "Guyana",
        "HTI": "Haiti",
        "HND": "Honduras",
        "HUN": "Hungary",
        "ISL": "Iceland",
        "IDN": "Indonesia",
        "IRQ": "Iraq",
        "IRL": "Ireland",
        "ISR": "Israel",
        "JAM": "Jamaica",
        "JOR": "Jordan",
        "KAZ": "Kazakhstan",
        "KEN": "Kenya",
        "KIR": "Kiribati",
        "KWT": "Kuwait",
        "KGZ": "Kyrgyzstan",
        "LAO": "Laos",
        "LVA": "Latvia",
        "LBN": "Lebanon",
        "LSO": "Lesotho",
        "LBR": "Liberia",
        "LBY": "Libya",
        "LIE": "Liechtenstein",
        "LTU": "Lithuania",
        "LUX": "Luxembourg",
        "MDG": "Madagascar",
        "MWI": "Malawi",
        "MYS": "Malaysia",
        "MDV": "Maldives",
        "MLI": "Mali",
        "MLT": "Malta",
        "MHL": "Marshall Islands",
        "MRT": "Mauritania",
        "MUS": "Mauritius",
        "FSM": "Micronesia",
        "MDA": "Moldova",
        "MCO": "Monaco",
        "MNG": "Mongolia",
        "MNE": "Montenegro",
        "MAR": "Morocco",
        "MOZ": "Mozambique",
        "MMR": "Myanmar",
        "NAM": "Namibia",
        "NRU": "Nauru",
        "NPL": "Nepal",
        "NLD": "Netherlands",
        "NIC": "Nicaragua",
        "NER": "Niger",
        "NGA": "Nigeria",
        "MKD": "North Macedonia",
        "NOR": "Norway",
        "OMN": "Oman",
        "PAK": "Pakistan",
        "PLW": "Palau",
        "PSE": "Palestine",
        "PAN": "Panama",
        "PNG": "Papua New Guinea",
        "PRY": "Paraguay",
        "PER": "Peru",
        "PHL": "Philippines",
        "POL": "Poland",
        "PRT": "Portugal",
        "QAT": "Qatar",
        "ROU": "Romania",
        "RWA": "Rwanda",
        "KNA": "Saint Kitts and Nevis",
        "LCA": "Saint Lucia",
        "VCT": "Saint Vincent and the Grenadines",
        "WSM": "Samoa",
        "SMR": "San Marino",
        "STP": "Sao Tome and Principe",
        "SAU": "Saudi Arabia",
        "SEN": "Senegal",
        "SRB": "Serbia",
        "SYC": "Seychelles",
        "SLE": "Sierra Leone",
        "SGP": "Singapore",
        "SVK": "Slovakia",
        "SVN": "Slovenia",
        "SLB": "Solomon Islands",
        "SOM": "Somalia",
        "ZAF": "South Africa",
        "SSD": "South Sudan",
        "LKA": "Sri Lanka",
        "SDN": "Sudan",
        "SUR": "Suriname",
        "SWE": "Sweden",
        "CHE": "Switzerland",
        "TWN": "Taiwan",
        "TJK": "Tajikistan",
        "TZA": "Tanzania",
        "THA": "Thailand",
        "TLS": "Timor-Leste",
        "TGO": "Togo",
        "TON": "Tonga",
        "TTO": "Trinidad and Tobago",
        "TUN": "Tunisia",
        "TUR": "Turkey",
        "TKM": "Turkmenistan",
        "TUV": "Tuvalu",
        "UGA": "Uganda",
        "UKR": "Ukraine",
        "ARE": "United Arab Emirates",
        "URY": "Uruguay",
        "UZB": "Uzbekistan",
        "VUT": "Vanuatu",
        "VAT": "Vatican City",
        "VEN": "Venezuela",
        "VNM": "Vietnam",
        "YEM": "Yemen",
        "ZMB": "Zambia",
        "ZWE": "Zimbabwe"
    }
    
    # Filter results if search term provided
    results = []
    for code, name in sorted(all_countries.items()):
        if search:
            search_lower = search.lower()
            if search_lower in code.lower() or search_lower in name.lower():
                results.append({"code": code, "name": name})
        else:
            results.append({"code": code, "name": name})
    
    return results


async def guide_to_tools(
    action: Literal["deploy-config", "connect-wallet", "select-countries", "generate-scope", "read-config"] = Field(
        description="What user wants to do"
    ),
    parameters: Optional[Dict[str, Any]] = Field(default={}, description="Optional parameters for the action")
) -> str:
    """
    Guide users to appropriate tools.self.xyz features for write operations.
    """
    base_url = "https://tools.self.xyz"
    
    if action == "deploy-config":
        if parameters:
            # Build URL with parameters
            url_params = []
            if "minimum_age" in parameters:
                url_params.append(f"age={parameters['minimum_age']}")
            if "excluded_countries" in parameters:
                countries = parameters['excluded_countries']
                if isinstance(countries, list):
                    url_params.append(f"countries={','.join(countries)}")
            if "ofac_enabled" in parameters:
                ofac = parameters['ofac_enabled']
                if isinstance(ofac, list):
                    url_params.append(f"ofac={','.join(str(o).lower() for o in ofac)}")
            
            url = f"{base_url}?{'&'.join(url_params)}" if url_params else base_url
            
            return f"""## Deploy Configuration to Self Protocol

To deploy your configuration on-chain, you need to use tools.self.xyz:

🔗 **Direct Link with Your Parameters:**
{url}

### Steps:
1. Click the link above to go to tools.self.xyz with pre-filled values
2. Connect your wallet (MetaMask, WalletConnect, etc.)
3. Review the configuration:
   - Minimum Age: {parameters.get('minimum_age', 0)}
   - Excluded Countries: {', '.join(parameters.get('excluded_countries', [])) or 'None'}
   - OFAC: {parameters.get('ofac_enabled', [False, False, False])}
4. Click "Set Verification Config"
5. Approve the transaction in your wallet
6. Wait for confirmation

💡 **Note:** This will cost gas on the Celo network. Make sure you have CELO tokens."""
        else:
            return f"""## Deploy Configuration to Self Protocol

To deploy a verification configuration:

🔗 **Go to:** {base_url}

### Steps:
1. Connect your wallet
2. Navigate to "Hub Contract Operations"
3. Configure your requirements:
   - Set minimum age (or leave at 0)
   - Select countries to exclude
   - Enable OFAC checks if needed
4. Click "Set Verification Config"
5. Sign the transaction

💡 **Tip:** Use `generate_config_id` first to preview your config ID."""
    
    elif action == "connect-wallet":
        return f"""## Connect Wallet to tools.self.xyz

🔗 **Go to:** {base_url}

### Supported Wallets:
- MetaMask
- WalletConnect
- Coinbase Wallet
- And more via RainbowKit

### Steps:
1. Click "Connect Wallet" button (top right)
2. Select your wallet provider
3. Approve the connection
4. Switch to Celo network if prompted

### Networks:
- **Mainnet:** Celo (Chain ID: 42220)
- **Testnet:** Celo Alfajores (Chain ID: 44787)

💡 **Need testnet funds?** Visit https://faucet.celo.org/alfajores"""
    
    elif action == "select-countries":
        return f"""## Select Countries for Exclusion

🔗 **Go to:** {base_url}

### Using the Country Selector:
1. In "Hub Contract Operations" section
2. Click "Select Countries to Exclude"
3. Use the visual country picker:
   - Search by name or code
   - Click to select/deselect
   - Maximum 40 countries
4. Click "Save" when done

### Alternative:
Use `list_country_codes` to see all available codes, then use them with `generate_config_id`.

💡 **Tip:** Common exclusions are sanctioned countries like IRN, PRK, CUB, SYR."""
    
    elif action == "generate-scope":
        return f"""## Generate Scope on tools.self.xyz

🔗 **Go to:** {base_url}#scope-generator

### What is a Scope?
The scope is a unique identifier for your verification requirements, generated by hashing your address/URL with a scope seed.

### Using the Scope Generator:
1. Enter your contract address or website URL
2. Enter a scope seed (max 20 chars, lowercase)
3. The scope hash generates automatically
4. Copy the generated scope for your contract

### Alternative:
Use `generate_scope_hash` in this MCP for local generation.

💡 **Example:** 
- Address: 0x1234...
- Seed: "my-app-v1"
- Result: 0xabcd..."""
    
    elif action == "read-config":
        config_id = parameters.get("config_id") if parameters else None
        if config_id:
            return f"""## Read Configuration

You can read this configuration using our MCP tool:

```
read_hub_config(
    config_id="{config_id}",
    network="mainnet"  # or "testnet"
)
```

Or view it on tools.self.xyz:
🔗 {base_url}#config-reader

Enter the config ID: {config_id}"""
        else:
            return f"""## Read Configuration

### Using MCP:
```
read_hub_config(
    config_id="0x...",
    network="mainnet"
)
```

### Using tools.self.xyz:
🔗 {base_url}#config-reader

1. Go to "Hub Contract Operations"
2. Scroll to "Read Config" section
3. Enter the configuration ID
4. Click "Read Configuration"

The tool will show:
- Minimum age requirement
- Excluded countries (decoded)
- OFAC settings
- Whether config exists on-chain"""
    
    return f"Visit {base_url} for Self protocol developer tools."