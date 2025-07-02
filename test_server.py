#!/usr/bin/env python3
"""Test the refactored Self MCP server"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def test_imports():
    """Test all imports work correctly"""
    print("Testing imports...")
    try:
        from self_mcp import server
        from self_mcp.tools import (
            explain_self_integration,
            generate_verification_code,
            debug_verification_error,
            check_self_status,
            generate_verification_config
        )
        from self_mcp.resources import (
            get_contract_addresses,
            get_example_code,
            get_best_practices
        )
        from self_mcp.prompts import (
            design_verification_flow,
            troubleshoot_integration
        )
        print("✅ All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False


async def test_tools():
    """Test the tools work correctly"""
    print("\nTesting tools...")
    
    try:
        from self_mcp.tools import explain_self_integration, generate_verification_code
        
        # Test explain_self_integration
        result = await explain_self_integration("airdrop")
        print(f"✅ explain_self_integration: {len(result)} chars")
        
        # Test generate_verification_code
        result = await generate_verification_code("frontend-qr", "typescript")
        print(f"✅ generate_verification_code: {len(result)} chars")
        
        return True
    except Exception as e:
        print(f"❌ Tool error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_resources():
    """Test the resources work correctly"""
    print("\nTesting resources...")
    
    try:
        from self_mcp.resources import get_contract_addresses, get_example_code
        
        # Test get_contract_addresses
        result = await get_contract_addresses()
        print(f"✅ get_contract_addresses: {len(result)} chars")
        
        # Test get_example_code
        result = await get_example_code("airdrop")
        print(f"✅ get_example_code: {len(result)} chars")
        
        return True
    except Exception as e:
        print(f"❌ Resource error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_server_creation():
    """Test the MCP server can be created"""
    print("\nTesting server creation...")
    
    try:
        from self_mcp.server import mcp
        
        # Check tools are registered
        tools = [t for t in dir(mcp) if t.startswith('tool_')]
        print(f"✅ Server created with {len(tools)} tools")
        
        return True
    except Exception as e:
        print(f"❌ Server creation error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("Testing refactored Self MCP server\n")
    print("=" * 50)
    
    tests = [
        test_imports(),
        test_tools(),
        test_resources(),
        test_server_creation()
    ]
    
    results = await asyncio.gather(*tests)
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All tests passed!")
        print("\nYou can now run the server with:")
        print("  python server.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())