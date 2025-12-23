# Multi-MCP Server Agent - Usage Guide

## Overview

This agent demonstrates how to build an AI assistant that can interact with **multiple MCP servers simultaneously**. It combines web search capabilities with user management to create a powerful, multi-domain agent.

## What Can This Agent Do?

### 🌐 Web Information Retrieval
- Fetch content from any URL
- Search for information about people, companies, events
- Extract data from web pages

### 👤 User Management
- Create, read, update, delete users
- Search users by various criteria
- Manage user profiles and information

### 🔗 Combined Workflows
- **Research and Save**: Find information online and save it to the user database
- **Enrich Profiles**: Look up additional information about existing users
- **Batch Operations**: Process multiple users with web-enriched data

## Quick Start

### Prerequisites

1. **Python 3.13+** installed
2. **Users MCP Server** running on `http://localhost:8005/mcp`
3. **Azure OpenAI API Key** with access to GPT-4
4. **Internet connection** for web fetch capabilities

### Setup

1. **Install dependencies**:
```bash
cd agent
pip install -r requirements.txt
```

2. **Set environment variables**:
```bash
# Windows (CMD)
set DIAL_API_KEY=your_azure_openai_api_key

# Windows (PowerShell)
$env:DIAL_API_KEY="your_azure_openai_api_key"

# Linux/Mac
export DIAL_API_KEY=your_azure_openai_api_key
```

3. **Start the Users MCP Server** (in a separate terminal):
```bash
cd mcp_server
python server.py
```

4. **Test the architecture**:
```bash
python agent/test_architecture.py
```

5. **Run the agent**:
```bash
python agent/app.py
```

## Usage Examples

### Example 1: Fetch Information and Create User

**Input:**
```
You: Find information about Elon Musk from Wikipedia and save him as user 100
```

**What happens:**
1. Agent calls `fetch` tool (routed to Web Fetch MCP Server)
2. Retrieves content from Wikipedia
3. Agent extracts relevant information
4. Agent calls `create_user` tool (routed to Users MCP Server)
5. Creates user with ID 100

**Expected Output:**
```
🤖: Let me fetch information about Elon Musk...
    🔀 Routing 'fetch' to 'web_fetch'
    ⚙️: [content from Wikipedia]
    
    Now I'll create a user profile...
    🔀 Routing 'create_user' to 'users_service'
    ⚙️: User created successfully
    
    ✅ I've created user 100 with Elon Musk's information from Wikipedia.
```

### Example 2: Get Existing User

**Input:**
```
You: Get user 100
```

**What happens:**
1. Agent calls `get_user` tool (routed to Users MCP Server)
2. Retrieves user information

**Expected Output:**
```
🤖: 
    🔀 Routing 'get_user' to 'users_service'
    ⚙️: {"id": 100, "name": "Elon", "surname": "Musk", ...}
    
    Here's the information for user 100:
    - Name: Elon Musk
    - Email: ...
    - ...
```

### Example 3: Search and Enrich

**Input:**
```
You: Search for users with surname "Smith" and update user 1 with info about Will Smith from the web
```

**What happens:**
1. Agent calls `search_users` (Users MCP Server)
2. Agent calls `fetch` to get Will Smith info (Web Fetch MCP Server)
3. Agent calls `update_user` with new data (Users MCP Server)

### Example 4: Complex Multi-Step

**Input:**
```
You: Find the CEO of Tesla online, then check if we have a user with that name, if not create one with ID 200
```

**What happens:**
1. `fetch` - Get Tesla CEO information
2. `search_users` - Search for existing user
3. `create_user` - Create new user if not found

## Architecture Overview

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         app.py                              │
│                    (Main Application)                       │
└──────────────┬─────────────────────────────┬───────────────┘
               │                             │
               ▼                             ▼
      ┌────────────────┐           ┌──────────────────────┐
      │  DialClient    │           │ MCPClientManager    │
      │ (LLM Interface)│◄──────────│  (Tool Router)      │
      └────────────────┘           └──────┬───────────────┘
               │                          │
               ▼                          │
      ┌────────────────┐                  │
      │   Azure OpenAI │                  │
      │     GPT-4      │                  │
      └────────────────┘                  │
                                          │
                    ┌─────────────────────┴─────────────────────┐
                    │                                           │
                    ▼                                           ▼
           ┌─────────────────┐                        ┌─────────────────┐
           │   MCPClient     │                        │   MCPClient     │
           │ (users_service) │                        │  (web_fetch)    │
           └────────┬────────┘                        └────────┬────────┘
                    │                                          │
                    ▼                                          ▼
           ┌─────────────────┐                        ┌─────────────────┐
           │ Users MCP Server│                        │ Fetch MCP Server│
           │  localhost:8005 │                        │   remote.mcp... │
           └─────────────────┘                        └─────────────────┘
```

### Key Features

1. **Tool Registry Pattern**: Automatically maps tools to their MCP servers
2. **Transparent Routing**: LLM doesn't need to know which server provides which tool
3. **1-to-1 Connections**: Each MCPClient maintains one connection to one server
4. **Unified Interface**: All tools appear as a single set to the LLM
5. **Async Management**: Proper async context management for all connections

## Configuration

### Adding More MCP Servers

To add additional MCP servers, edit `agent/app.py`:

```python
# Add your new MCP server
await mcp_manager.add_mcp_client(
    client_name="my_service",
    mcp_server_url="http://localhost:9000/mcp"
)
```

That's it! The tools will automatically:
- Be discovered and registered
- Be added to the LLM's tool list
- Be routed correctly when called

### Customizing the System Prompt

Edit `agent/prompts.py` to change how the agent behaves:

```python
SYSTEM_PROMPT = """
Your custom instructions here...
"""
```

## Troubleshooting

### Error: "Connection refused" to Users MCP Server

**Solution**: Make sure the Users MCP Server is running:
```bash
cd mcp_server
python server.py
```

### Error: "DIAL_API_KEY not set"

**Solution**: Set the environment variable:
```bash
set DIAL_API_KEY=your_api_key  # Windows CMD
$env:DIAL_API_KEY="your_api_key"  # PowerShell
export DIAL_API_KEY=your_api_key  # Linux/Mac
```

### Error: "Tool not found in any MCP client"

**Solution**: This means the LLM tried to call a tool that doesn't exist. Check:
1. All MCP servers are connected
2. Tool names match exactly
3. Run `test_architecture.py` to verify tool registration

### Error: "RuntimeError: Attempted to exit cancel scope in a different task"

**Solution**: This is a cleanup error. The code includes proper error handling to prevent this from affecting functionality, but if persistent:
1. Update to the latest version of `mcp` library
2. Check your Python version (3.13+ recommended)

## Performance Tips

1. **Connection Pooling**: Reuse the same `MCPClientManager` instance
2. **Parallel Tool Calls**: The architecture supports parallel tool execution
3. **Caching**: Consider caching frequently-used prompts and resources
4. **Timeouts**: Add timeout handling for long-running tool calls

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Input Validation**: The agent validates tool arguments before calling
3. **Error Handling**: Errors are caught and reported safely
4. **Data Privacy**: Be careful with sensitive information in prompts

## Advanced Usage

### Accessing Resources

```python
# Get all resources from all servers
all_resources = await mcp_manager.get_all_resources()
for client_name, resources in all_resources.items():
    print(f"Resources from {client_name}:")
    for resource in resources:
        print(f"  - {resource.name}")
```

### Using Prompts

```python
# Get all prompts from all servers
all_prompts = await mcp_manager.get_all_prompts()
for client_name, prompts in all_prompts.items():
    for prompt in prompts:
        content = await client.get_prompt(prompt.name)
        print(content)
```

### Direct Tool Calls

```python
# Bypass the LLM and call tools directly
result = await mcp_manager.call_tool("get_user", {"user_id": 100})
```

## Testing

Run the comprehensive test suite:

```bash
python agent/test_architecture.py
```

This will verify:
- ✅ Connection to multiple MCP servers
- ✅ Tool registration and routing
- ✅ Resource and prompt fetching
- ✅ Client isolation
- ✅ Error handling

## Next Steps

1. **Add More MCP Servers**: Integrate additional services (database, email, etc.)
2. **Implement Caching**: Cache tool schemas and common queries
3. **Add Monitoring**: Track tool call latencies and success rates
4. **Build UI**: Create a web interface for the agent
5. **Deploy**: Containerize and deploy to production

## References

- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Architecture Documentation](./ARCHITECTURE.md)

## License

MIT License - Feel free to use and modify!

## Support

For questions or issues:
1. Check the [Architecture Documentation](./ARCHITECTURE.md)
2. Run the test script to diagnose problems
3. Review error messages carefully - they include helpful hints

---

**Happy Building! 🚀**
