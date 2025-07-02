#!/usr/bin/env python3
"""Test script for Self MCP server"""

import asyncio
import json


async def test_tools():
    """Test the MCP tools locally"""
    # Import the server module
    from server import explain_self_integration, generate_verification_code, debug_verification_error
    
    print("Testing Self MCP Server Tools\n")
    print("="*50)
    
    # Test 1: explain_self_integration
    print("\n1. Testing explain_self_integration - Airdrop use case:")
    print("-"*50)
    result = await explain_self_integration("airdrop")
    print(result[:500] + "...\n")  # Show first 500 chars
    
    # Test 2: generate_verification_code
    print("\n2. Testing generate_verification_code - Frontend QR:")
    print("-"*50)
    result = await generate_verification_code("frontend-qr", "typescript")
    print(result[:500] + "...\n")
    
    print("\n3. Testing generate_verification_code - Backend verify:")
    print("-"*50)
    result = await generate_verification_code("backend-verify", "typescript")
    print(result[:500] + "...\n")
    
    # Test 3: debug_verification_error
    print("\n4. Testing debug_verification_error - Scope mismatch:")
    print("-"*50)
    result = await debug_verification_error("Invalid scope validation failed", "scope-mismatch")
    print(result[:500] + "...\n")
    
    print("\n5. Testing debug_verification_error - Unknown error:")
    print("-"*50)
    result = await debug_verification_error("Something went wrong with verification")
    print(result[:500] + "...\n")
    
    print("="*50)
    print("All tests completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_tools())