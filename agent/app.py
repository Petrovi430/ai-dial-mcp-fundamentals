import asyncio
import json
import os

from mcp import Resource
from mcp.types import Prompt

from agent.mcp_client import MCPClient
from agent.dial_client import DialClient
from agent.models.message import Message, Role
from agent.prompts import SYSTEM_PROMPT


# https://remote.mcpservers.org/fetch/mcp
# Pay attention that `fetch` doesn't have resources and prompts

async def main():
    # 1. Create MCP client and open connection to the MCP server
    async with MCPClient(mcp_server_url="http://localhost:8005/mcp") as mcp_client:
        # 2. Get Available MCP Resources and print them
        resources = await mcp_client.get_resources()
        print(f"MCP resources: {resources}")

        # 3. Get Available MCP Tools, assign to `tools` variable, print tool as well
        tools = await mcp_client.get_tools()
        print(f"MCP tools: {tools}")

        # 4. Create DialClient
        dial_client = DialClient(
            api_key=os.getenv("DIAL_API_KEY"),
            endpoint="https://ai-proxy.lab.epam.com",
            tools=tools,
            mcp_client=mcp_client
        )

        # 5. Create list with messages and add SYSTEM_PROMPT
        messages = [Message(role=Role.SYSTEM, content=SYSTEM_PROMPT)]

        # 6. Add to messages Prompts from MCP server as User messages
        prompts = await mcp_client.get_prompts()
        for prompt in prompts:
            prompt_content = await mcp_client.get_prompt(prompt.name)
            messages.append(Message(role=Role.USER, content=prompt_content))

        # 7. Console chat loop
        print("Type your message (type 'exit' to quit):")
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


if __name__ == "__main__":
    asyncio.run(main())