# Quick Reference Card - Multi-MCP Agent

## 🚀 Quick Start

```bash
# 1. Start Users MCP Server (Terminal 1)
cd mcp_server && python server.py

# 2. Set API Key (Terminal 2)
set DIAL_API_KEY=your_key  # Windows
export DIAL_API_KEY=your_key  # Linux/Mac

# 3. Test Architecture
python agent/test_architecture.py

# 4. Run Agent
python agent/app.py
```

## 📋 Example Commands

| Command | What It Does | Tools Used |
|---------|--------------|------------|
| `Find info about Elon Musk and save as user 100` | Fetches from web + creates user | fetch → create_user |
| `Get user 100` | Retrieves user info | get_user |
| `Search for users named Smith` | Searches user database | search_users |
| `Update user 100 with email test@example.com` | Updates user | update_user |
| `Delete user 100` | Removes user | delete_user |

## 🔧 Key Components

```python
# MCPClientManager - Routes tools to correct MCP server
mcp_manager = MCPClientManager()
await mcp_manager.add_mcp_client("users_service", url1)
await mcp_manager.add_mcp_client("web_fetch", url2)

# DialClient - Handles LLM and tool execution
dial_client = DialClient(api_key, endpoint, tools, mcp_manager)

# MCPClient - 1-to-1 connection with MCP server
mcp_client = MCPClient(server_url)
```

## 🗺️ Tool Routing Map

```
get_user      → users_service
create_user   → users_service
update_user   → users_service
delete_user   → users_service
search_users  → users_service
fetch         → web_fetch
```

## 📊 Architecture Flow

```
User → App → DialClient → GPT-4 → Tool Call
                ↓
          MCPClientManager (routes based on tool name)
                ↓
          ┌─────┴─────┐
          ↓           ↓
    MCPClient1   MCPClient2
          ↓           ↓
    MCP Server1  MCP Server2
```

## 🧪 Test Commands

```bash
# Full test suite
python agent/test_architecture.py

# Visual diagram
python agent/visualize_architecture.py
```

## 📁 File Map

```
agent/
├── app.py                    # Main entry point
├── mcp_client_manager.py     # Multi-MCP router
├── dial_client.py            # LLM interface
├── mcp_client.py             # Single MCP connection
├── prompts.py                # System prompt
└── models/message.py         # Message model
```

## 🔑 Key Concepts

- **1-to-1**: Each MCPClient connects to ONE MCP server
- **Tool Registry**: Maps tool names to MCP clients
- **Transparent Routing**: LLM doesn't know about routing
- **Agent Loop**: LLM → Tools → LLM → ... → Final Answer

## 🐛 Troubleshooting

| Error | Solution |
|-------|----------|
| Connection refused | Start MCP server: `python mcp_server/server.py` |
| DIAL_API_KEY not set | Set environment variable |
| Tool not found | Check tool registry: run test script |

## 📚 Documentation

- **ARCHITECTURE.md** - Detailed technical architecture
- **USAGE.md** - Complete usage guide
- **IMPLEMENTATION_SUMMARY.md** - Implementation overview

## 💡 Pro Tips

1. **Add new MCP server**: Just call `add_mcp_client()` - tools auto-register
2. **Debug routing**: Check `mcp_manager.tool_to_client_map`
3. **Test changes**: Run `test_architecture.py` before agent
4. **Monitor tools**: Tool execution prints routing info

---

**Need help? Check the full documentation!**
