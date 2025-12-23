from typing import Any

from agent.mcp_client import MCPClient


class MCPClientManager:
    """
    Manages multiple MCP clients and routes tool calls to the appropriate client.
    Each MCP server provides its own set of tools, and we need to maintain
    a 1-to-1 connection between each MCP client and its server.
    """

    def __init__(self):
        self.mcp_clients: dict[str, MCPClient] = {}
        self.tool_to_client_map: dict[str, str] = {}  # tool_name -> client_name

    async def add_mcp_client(self, client_name: str, mcp_server_url: str) -> MCPClient:
        """
        Add a new MCP client and connect to its server.
        Returns the connected MCP client.
        """
        mcp_client = MCPClient(mcp_server_url)
        await mcp_client.__aenter__()
        self.mcp_clients[client_name] = mcp_client

        # Register tools from this client
        tools = await mcp_client.get_tools()
        for tool in tools:
            tool_name = tool["function"]["name"]
            self.tool_to_client_map[tool_name] = client_name
            print(f"📋 Registered tool '{tool_name}' from '{client_name}'")

        return mcp_client

    async def get_all_tools(self) -> list[dict[str, Any]]:
        """Get all tools from all connected MCP clients"""
        all_tools = []
        for client in self.mcp_clients.values():
            tools = await client.get_tools()
            all_tools.extend(tools)
        return all_tools

    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        """
        Route tool call to the appropriate MCP client based on the tool name.
        """
        client_name = self.tool_to_client_map.get(tool_name)
        if not client_name:
            raise ValueError(f"Tool '{tool_name}' not found in any MCP client")

        mcp_client = self.mcp_clients[client_name]
        print(f"    🔀 Routing '{tool_name}' to '{client_name}'")
        return await mcp_client.call_tool(tool_name, tool_args)

    async def get_all_resources(self) -> dict[str, list]:
        """Get resources from all MCP clients, grouped by client name"""
        all_resources = {}
        for client_name, client in self.mcp_clients.items():
            resources = await client.get_resources()
            if resources:
                all_resources[client_name] = resources
        return all_resources

    async def get_all_prompts(self) -> dict[str, list]:
        """Get prompts from all MCP clients, grouped by client name"""
        all_prompts = {}
        for client_name, client in self.mcp_clients.items():
            prompts = await client.get_prompts()
            if prompts:
                all_prompts[client_name] = prompts
        return all_prompts

    async def get_client_by_name(self, client_name: str) -> MCPClient:
        """Get a specific MCP client by name"""
        if client_name not in self.mcp_clients:
            raise ValueError(f"MCP client '{client_name}' not found")
        return self.mcp_clients[client_name]

    async def close_all(self):
        """Close all MCP client connections gracefully"""
        errors = []
    
        for client_name, client in list(self.mcp_clients.items()):
            try:
                await client.__aexit__(None, None, None)
                print(f"✅ Closed connection to '{client_name}'")
            except Exception as e:
                error_msg = f"Error closing '{client_name}': {e}"
                errors.append(error_msg)
                print(f"⚠️  {error_msg}")
    
        # Clear the dictionaries after cleanup
        self.mcp_clients.clear()
        self.tool_to_client_map.clear()
    
        if errors:
            print(f"⚠️  Cleanup completed with {len(errors)} error(s)")
