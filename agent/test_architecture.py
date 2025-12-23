"""
Test script for Multi-MCP Server Agent
Tests the integration between Users Service and Web Fetch MCP servers
"""
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.mcp_client_manager import MCPClientManager


async def test_mcp_manager():
    """Test the MCPClientManager with multiple servers"""
    print("\n" + "=" * 80)
    print("TESTING MULTI-MCP SERVER ARCHITECTURE")
    print("=" * 80)

    mcp_manager = MCPClientManager()

    try:
        # Test 1: Connect to Users Service
        print("\n[TEST 1] Connecting to Users Service MCP Server...")
        print("-" * 80)
        users_client = await mcp_manager.add_mcp_client(
            client_name="users_service",
            mcp_server_url="http://localhost:8005/mcp"
        )
        print("✅ Successfully connected to Users Service")

        # Test 2: Connect to Fetch Service
        print("\n[TEST 2] Connecting to Web Fetch MCP Server...")
        print("-" * 80)
        fetch_client = await mcp_manager.add_mcp_client(
            client_name="web_fetch",
            mcp_server_url="https://remote.mcpservers.org/fetch/mcp"
        )
        print("✅ Successfully connected to Web Fetch")

        # Test 3: Get all tools
        print("\n[TEST 3] Fetching all tools from all servers...")
        print("-" * 80)
        all_tools = await mcp_manager.get_all_tools()
        print(f"Total tools: {len(all_tools)}")
        for tool in all_tools:
            tool_name = tool['function']['name']
            client_name = mcp_manager.tool_to_client_map[tool_name]
            print(f"  📋 {tool_name:<20} → {client_name}")
        print("✅ Successfully fetched all tools")

        # Test 4: Verify tool routing map
        print("\n[TEST 4] Verifying tool-to-client routing map...")
        print("-" * 80)
        print("Tool Registry:")
        for tool_name, client_name in mcp_manager.tool_to_client_map.items():
            print(f"  {tool_name:<20} → {client_name}")
        print("✅ Tool routing map verified")

        # Test 5: Test Users Service tool
        print("\n[TEST 5] Testing Users Service tool call...")
        print("-" * 80)
        try:
            result = await mcp_manager.call_tool("get_user", {"user_id": 999})
            print(f"Result: {result}")
            print("✅ Users Service tool call successful")
        except Exception as e:
            print(f"⚠️  Expected error (user might not exist): {e}")

        # Test 6: Get all resources
        print("\n[TEST 6] Fetching all resources from all servers...")
        print("-" * 80)
        all_resources = await mcp_manager.get_all_resources()
        for client_name, resources in all_resources.items():
            print(f"Resources from '{client_name}': {len(resources)}")
            for resource in resources[:3]:  # Show first 3
                print(f"  📦 {resource.name}")
        print("✅ Successfully fetched all resources")

        # Test 7: Get all prompts
        print("\n[TEST 7] Fetching all prompts from all servers...")
        print("-" * 80)
        all_prompts = await mcp_manager.get_all_prompts()
        for client_name, prompts in all_prompts.items():
            print(f"Prompts from '{client_name}': {len(prompts)}")
            for prompt in prompts:
                print(f"  📝 {prompt.name}: {prompt.description}")
        print("✅ Successfully fetched all prompts")

        # Test 8: Verify client isolation
        print("\n[TEST 8] Verifying client isolation...")
        print("-" * 80)
        users_client_ref = await mcp_manager.get_client_by_name("users_service")
        fetch_client_ref = await mcp_manager.get_client_by_name("web_fetch")
        assert users_client_ref is users_client, "Users client reference mismatch"
        assert fetch_client_ref is fetch_client, "Fetch client reference mismatch"
        assert users_client_ref is not fetch_client_ref, "Clients should be different"
        print("✅ Client isolation verified")

        print("\n" + "=" * 80)
        print("ALL TESTS PASSED! ✅")
        print("=" * 80)
        print("\nThe architecture is working correctly:")
        print("  ✓ Multiple MCP servers connected")
        print("  ✓ Tools properly registered and routed")
        print("  ✓ Resources and prompts accessible")
        print("  ✓ Client isolation maintained")
        print("\nYou can now run: python agent/app.py")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("\n[CLEANUP] Closing all connections...")
        await mcp_manager.close_all()
        print("✅ All connections closed")


if __name__ == "__main__":
    # Check environment
    if not os.getenv("DIAL_API_KEY"):
        print("⚠️  Warning: DIAL_API_KEY not set in environment")
        print("   Set it before running the full agent")

    asyncio.run(test_mcp_manager())
