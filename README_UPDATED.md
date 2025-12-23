# Framework-based MCP (Server & Client) - ✅ Multi-MCP Implementation
Python implementation for building Users Management Agent with MCP tools and MCP server

**🎉 Extended with Multi-MCP Server Support!** This implementation now supports connecting to multiple MCP servers simultaneously, enabling the agent to fetch information from the web and manage users in a single conversation.

## 🎯 Task Overview

Create and run MCP server with simple tools. Implement simple Users Management Agent with MCP Client that will use MCP tools from created server.

**BONUS**: Extended to support multiple MCP servers, allowing the agent to combine capabilities from different services (web fetch + user management).

## 🎓 Learning Goals

By exploring and working with this project, you will learn:

- How to configure simple MCP server
- How to configure client and connect to MCP server
- How to create simple Agent with tools from MCP server
- Key features of MCP
- **NEW**: How to architect multi-MCP server systems
- **NEW**: Tool routing and registry patterns
- **NEW**: Building complex agent workflows

## 🏗️ Architecture

### Project Structure
```
task/
├── agent/
│   ├── models/           
│   │   └── message.py              ✅ Complete
│   ├── app.py                      ✅ Complete (Multi-MCP Support)
│   ├── prompts.py                  ✅ Complete
│   ├── dial_client.py              ✅ Complete (Multi-MCP Support)
│   ├── mcp_client.py               ✅ Complete
│   ├── mcp_client_manager.py       ✅ NEW: Multi-MCP Router
│   ├── test_architecture.py        ✅ NEW: Comprehensive Tests
│   ├── visualize_architecture.py   ✅ NEW: Visual Diagrams
│   ├── ARCHITECTURE.md             ✅ NEW: Architecture Docs
│   ├── USAGE.md                    ✅ NEW: Usage Guide
│   ├── IMPLEMENTATION_SUMMARY.md   ✅ NEW: Implementation Summary
│   └── QUICK_REFERENCE.md          ✅ NEW: Quick Reference
└── mcp_server/               
    ├── server.py                   ✅ Complete
    ├── user_client.py              ✅ Complete
    └── Dockerfile                  ✅ Complete
```

### Multi-MCP Architecture Diagram

```
                User
                 │
                 ▼
              app.py
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
   DialClient    MCPClientManager
        │                 │
        ▼                 │
   Azure OpenAI          │
     (GPT-4)             │
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
  MCPClient                         MCPClient
 (users_service)                   (web_fetch)
        │                                 │
        ▼                                 ▼
Users MCP Server                  Fetch MCP Server
localhost:8005                    remote.mcpservers.org
```

# <img src="flow.png">

## 🎉 What's New: Multi-MCP Server Support

This implementation extends the original task to support **multiple MCP servers simultaneously**!

### Key Features:
- ✅ **Multiple MCP Connections**: Connect to multiple MCP servers at once
- ✅ **Intelligent Tool Routing**: Automatically routes tool calls to the correct MCP server
- ✅ **Unified Interface**: LLM sees all tools as one unified set
- ✅ **Combined Workflows**: Fetch info from web + save to user database in one conversation
- ✅ **1-to-1 Connections**: Each MCPClient maintains one connection to one server
- ✅ **Comprehensive Documentation**: Architecture, usage guides, and examples

### Example Usage:
```
You: Find information about Elon Musk and save as user 100

🤖: Let me fetch information about Elon Musk...
    🔀 Routing 'fetch' to 'web_fetch'
    ⚙️: [Wikipedia content]
    
    Now I'll create a user profile...
    🔀 Routing 'create_user' to 'users_service'
    ⚙️: User created successfully
    
    ✅ I've created user 100 with Elon Musk's information.
```

## 📋 Requirements

- **Python**: 3.13 or higher (3.11+ supported)
- **Dependencies**: Listed in `requirements.txt`
- **API Access**: DIAL API key (Azure OpenAI) with appropriate permissions
- **Network**: EPAM VPN connection for internal API access
- Docker and Docker Compose
- Postman (optional, for MCP server testing)

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Docker and Docker Compose
- Azure OpenAI API Key (DIAL_API_KEY)

### Setup & Run

```bash
# 1. Start Users MCP Server (Terminal 1)
cd mcp_server
python server.py

# 2. Set API Key (Terminal 2)
set DIAL_API_KEY=your_azure_openai_key  # Windows
export DIAL_API_KEY=your_azure_openai_key  # Linux/Mac

# 3. Test Architecture (Optional but recommended)
cd agent
python test_architecture.py

# 4. Run Agent
python app.py
```

### Try These Commands:
- `Find info about Elon Musk and save as user 100`
- `Get user 100`
- `Search for users with surname Smith`
- `Look up Tim Cook online and update user 50 with his info`

## ✍️ Tasks:

If the task in the main branch is hard for you, then switch to the `with-detailed-description` branch

You need to implement the Users Management Agent, that will be able to perform CRUD operations within User Management Service.

### Create and run MCP server:
1. Run [root docker-compose](docker-compose.yml) (Optional step in case if you have it from previous tasks)
2. Open [mcp_server](mcp_server/server.py)
3. Implement all ***TODO***
4. Run [mcp_server](mcp_server/server.py)

### OPTIONAL: Work with MCP server in Postman
1. Import [mcp.postman_collection](mcp.postman_collection.json) to Postman
2. Make `init` call and get `mcp-session-id` in response headers
3. Make `init-notification`. Pay attention that you need to use `mcp-session-id` retrieved from `init` request. it should return 202 status
4. Get tools (don't forget about `mcp-session-id`). It should return stream with tools.
5. Call calculator (don't forget about `mcp-session-id`). It should return stream tool execution result.


### Create and run Agent:
1. Open [mcp_client](agent/mcp_client.py) and implement all ***TODO***
2. Open [dial_client](agent/dial_client.py) and implement all ***TODO***
3. Open [prompts](agent/prompts.py) and write System prompt
4. Open [app](agent/app.py) and implement all ***TODO***
5. Run application [mcp_client](agent/app.py) and test that it is connecting to MCP Server and works properly
6. Try with your solution with `fetch MCP` `https://remote.mcpservers.org/fetch/mcp` and check the differences on the `init` step (what they have and don't)

### ✅ COMPLETED: Support both (users-management and fetch) MCP servers:

**Status**: ✅ **FULLY IMPLEMENTED**

The agent now supports multiple MCP servers through the `MCPClientManager` component:

1. ✅ **1-to-1 Connection**: Each MCPClient maintains exactly one connection to one MCP server
2. ✅ **Tool Registry Pattern**: Central registry maps tool names to their respective MCP clients
3. ✅ **Intelligent Routing**: Tool calls are automatically routed to the correct MCP server
4. ✅ **Combined Capabilities**: Agent can fetch info from web AND manage users
5. ✅ **Transparent to LLM**: All tools appear as a unified set to the AI model

**Implementation Details:**
- Created `MCPClientManager` class (`agent/mcp_client_manager.py`)
- Updated `DialClient` to use the manager instead of single client
- Updated `app.py` to connect to multiple MCP servers
- Added comprehensive documentation and tests

**Key Components:**
```python
# MCPClientManager - Routes tools to correct server
mcp_manager = MCPClientManager()
await mcp_manager.add_mcp_client("users_service", url1)
await mcp_manager.add_mcp_client("web_fetch", url2)

# Tool calls are automatically routed
await mcp_manager.call_tool("get_user", {...})  # → users_service
await mcp_manager.call_tool("fetch", {...})     # → web_fetch
```

**Documentation:**
- 📖 **[ARCHITECTURE.md](agent/ARCHITECTURE.md)** - Detailed technical architecture
- 📖 **[USAGE.md](agent/USAGE.md)** - Complete usage guide with examples
- 📖 **[IMPLEMENTATION_SUMMARY.md](agent/IMPLEMENTATION_SUMMARY.md)** - Implementation overview
- 📖 **[QUICK_REFERENCE.md](agent/QUICK_REFERENCE.md)** - Quick reference card

**Testing:**
```bash
# Run comprehensive tests
python agent/test_architecture.py

# View visual diagram
python agent/visualize_architecture.py
```

## 📚 Documentation

### For Users
- **[QUICK_REFERENCE.md](agent/QUICK_REFERENCE.md)** - Quick start and common commands
- **[USAGE.md](agent/USAGE.md)** - Detailed usage guide with examples

### For Developers
- **[ARCHITECTURE.md](agent/ARCHITECTURE.md)** - Technical architecture deep-dive
- **[IMPLEMENTATION_SUMMARY.md](agent/IMPLEMENTATION_SUMMARY.md)** - Implementation details

### Visual Tools
- **[visualize_architecture.py](agent/visualize_architecture.py)** - ASCII art architecture diagram
- **[test_architecture.py](agent/test_architecture.py)** - Comprehensive test suite

## 🧪 Testing

```bash
# Test the multi-MCP architecture
python agent/test_architecture.py

# Expected output:
# ✅ Successfully connected to Users Service
# ✅ Successfully connected to Web Fetch
# ✅ Successfully fetched all tools
# ✅ Tool routing map verified
# ... (more tests)
# ALL TESTS PASSED! ✅
```

## 🔑 Key Concepts

### 1. MCPClientManager
Central hub that manages multiple MCP clients and routes tool calls:
```python
class MCPClientManager:
    - add_mcp_client()      # Connect to new MCP server
    - get_all_tools()       # Aggregate tools from all servers
    - call_tool()           # Route to correct server
    - close_all()           # Clean shutdown
```

### 2. Tool Registry Pattern
Maps tool names to their MCP clients:
```
{
    "get_user": "users_service",
    "create_user": "users_service",
    "fetch": "web_fetch"
}
```

### 3. Agent Loop
```
1. User Input → DialClient
2. DialClient → GPT-4 (with all available tools)
3. GPT-4 → Tool Call
4. DialClient → MCPClientManager → Correct MCP Server
5. Tool Result → GPT-4
6. Repeat until final answer
```

## 🛠️ Adding New MCP Servers

Adding a new MCP server is simple:

```python
# In app.py
await mcp_manager.add_mcp_client(
    client_name="my_service",
    mcp_server_url="http://localhost:9000/mcp"
)
```

That's it! Tools will be auto-discovered and registered.

## 🐛 Troubleshooting

| Error | Solution |
|-------|----------|
| Connection refused to Users Server | Start MCP server: `cd mcp_server && python server.py` |
| DIAL_API_KEY not set | Set environment variable: `set DIAL_API_KEY=your_key` |
| Tool not found in any MCP client | Run `test_architecture.py` to verify connections |
| Import errors | Install dependencies: `pip install -r requirements.txt` |

## 💡 Example Workflows

### 1. Research and Save
```
You: Find information about Bill Gates and save as user 200

Agent:
1. fetch("https://en.wikipedia.org/wiki/Bill_Gates")
2. create_user(id=200, name="Bill", surname="Gates", ...)
3. Returns: "✅ Created user 200 with Bill Gates' information"
```

### 2. Enrich Existing User
```
You: Look up Satya Nadella online and update user 50

Agent:
1. fetch("https://en.wikipedia.org/wiki/Satya_Nadella")
2. update_user(id=50, name="Satya", surname="Nadella", ...)
3. Returns: "✅ Updated user 50 with Satya Nadella's information"
```

### 3. Search and Verify
```
You: Search for users named Smith, then verify if we have Tim Cook

Agent:
1. search_users(surname="Smith")
2. search_users(name="Tim", surname="Cook")
3. Returns: Results from both searches
```

## 🚀 Performance Tips

1. **Connection Reuse**: MCPClientManager reuses connections
2. **Parallel Requests**: Multiple tool calls can execute in parallel
3. **Caching**: Consider caching frequently-used data
4. **Error Handling**: Robust error handling prevents cascading failures

## 🔒 Security Considerations

1. **API Keys**: Never commit API keys - use environment variables
2. **Input Validation**: Tool arguments are validated before execution
3. **Error Messages**: Errors are sanitized before returning to user
4. **Data Privacy**: Be careful with sensitive information in prompts

## 📈 Future Enhancements

- [ ] Dynamic MCP server discovery
- [ ] Load balancing across server replicas
- [ ] Tool call caching and memoization
- [ ] Monitoring and telemetry
- [ ] Retry logic with exponential backoff
- [ ] Web UI for agent interaction

## 🤝 Contributing

This is an educational project. Feel free to:
- Extend with more MCP servers
- Add new capabilities
- Improve documentation
- Share feedback

## 📄 License

MIT License - Feel free to use and modify!

---

# <img src="dialx-banner.png">

---

**Built with ❤️ as an educational demonstration of Multi-MCP Server Architecture**
