import asyncio
import json
import os

from mcp import Resource
from mcp.types import Prompt

from agent.mcp_client_manager import MCPClientManager
from agent.dial_client import DialClient
from agent.models.message import Message, Role
from agent.prompts import SYSTEM_PROMPT


# https://remote.mcpservers.org/fetch/mcp
# Pay attention that `fetch` doesn't have resources and prompts

# MCP Server URLs
USERS_MCP_SERVER_URL = "http://localhost:8005/mcp"
FETCH_MCP_SERVER_URL = "https://remote.mcpservers.org/fetch/mcp"


async def main():
    # 1. Create MCP Client Manager to handle multiple MCP servers
    mcp_manager = MCPClientManager()

    try:
        # 2. Connect to Users Service MCP Server
        print("\n🔌 Connecting to Users Service MCP Server...")
        users_client = await mcp_manager.add_mcp_client(
            client_name="users_service",
            mcp_server_url=USERS_MCP_SERVER_URL
        )

        # 3. Connect to Web Fetch MCP Server
        print("\n🔌 Connecting to Web Fetch MCP Server...")
        fetch_client = await mcp_manager.add_mcp_client(
            client_name="web_fetch",
            mcp_server_url=FETCH_MCP_SERVER_URL
        )

        # 4. Get all available tools from all MCP servers
        print("\n📚 Getting all available tools...")
        all_tools = await mcp_manager.get_all_tools()
        print(f"Total tools available: {len(all_tools)}")
        for tool in all_tools:
            print(f"  - {tool['function']['name']}")

        # 5. Get all resources from all MCP servers
        print("\n📦 Getting all resources...")
        all_resources = await mcp_manager.get_all_resources()
        for client_name, resources in all_resources.items():
            print(f"Resources from '{client_name}': {len(resources)}")

        # 6. Create DialClient with all tools and the manager
        dial_client = DialClient(
            api_key=os.getenv("DIAL_API_KEY"),
            endpoint="https://ai-proxy.lab.epam.com",
            tools=all_tools,
            mcp_manager=mcp_manager
        )

        # 7. Create list with messages and add SYSTEM_PROMPT
        messages = [Message(role=Role.SYSTEM, content=SYSTEM_PROMPT)]

        # 8. Add prompts from all MCP servers as User messages
        print("\n📝 Loading prompts from MCP servers...")
        all_prompts = await mcp_manager.get_all_prompts()
        for client_name, prompts in all_prompts.items():
            print(f"Prompts from '{client_name}': {len(prompts)}")
            for prompt in prompts:
                client = await mcp_manager.get_client_by_name(client_name)
                prompt_content = await client.get_prompt(prompt.name)
                messages.append(Message(role=Role.USER, content=prompt_content))
                print(f"  - Loaded prompt: {prompt.name}")

        # 9. Console chat loop
        print("\n" + "="*60)
        print("🤖 Agent ready! I can fetch info from the web and save to Users Service.")
        print("Example: 'Find info about Elon Musk and save as user 100'")
        print("="*60)
        print("\nType your message (type 'exit' to quit):")
        while True:
            user_input = input("You: ")
            if user_input.strip().lower() in {"exit", "quit"}:
                print("Exiting chat.")
                break
            messages.append(Message(role=Role.USER, content=user_input))
            # Call DialClient with the message history
            response = await dial_client.get_completion(messages)
            # Response is already printed by the streaming in DialClient
            messages.append(response)

    finally:
        # 10. Close all MCP connections
        print("\n🔌 Closing all MCP connections...")
        await mcp_manager.close_all()


if __name__ == "__main__":
    asyncio.run(main())