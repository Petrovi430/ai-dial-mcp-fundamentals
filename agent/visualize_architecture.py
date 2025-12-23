"""
Generates a visual flow diagram of the multi-MCP architecture
"""


def print_architecture():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     MULTI-MCP SERVER AGENT ARCHITECTURE                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

                                  ┌──────────┐
                                  │   User   │
                                  └────┬─────┘
                                       │
                                       ▼
                          ┌────────────────────────┐
                          │       app.py           │
                          │  (Main Application)    │
                          └───────┬────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
        ┌────────────────────┐      ┌──────────────────────┐
        │   DialClient       │      │ MCPClientManager     │
        │ ┌────────────────┐ │      │                      │
        │ │ - streams LLM  │ │      │ ┌──────────────────┐ │
        │ │ - handles tools│◄┼──────┼►│  Tool Registry:  │ │
        │ │ - agent loop   │ │      │ │  get_user→users  │ │
        │ └────────────────┘ │      │ │  fetch→web_fetch │ │
        └──────────┬─────────┘      │ └──────────────────┘ │
                   │                 └───────┬──────────────┘
                   ▼                         │
          ┌─────────────────┐               │
          │  Azure OpenAI   │               │
          │     GPT-4o      │               │
          │  ┌───────────┐  │               │
          │  │ Generates │  │               │
          │  │ Tool Calls│  │               │
          │  └───────────┘  │               │
          └─────────────────┘               │
                                            │
               ┌────────────────────────────┴────────────────────────────┐
               │                                                          │
               ▼                                                          ▼
    ┌─────────────────────┐                                  ┌─────────────────────┐
    │   MCPClient         │                                  │   MCPClient         │
    │  (users_service)    │                                  │   (web_fetch)       │
    │                     │                                  │                     │
    │ ┌─────────────────┐ │                                  │ ┌─────────────────┐ │
    │ │ Tools:          │ │                                  │ │ Tools:          │ │
    │ │ - get_user      │ │                                  │ │ - fetch         │ │
    │ │ - create_user   │ │                                  │ │                 │ │
    │ │ - update_user   │ │                                  │ │                 │ │
    │ │ - delete_user   │ │                                  │ │                 │ │
    │ │ - search_users  │ │                                  │ │                 │ │
    │ └─────────────────┘ │                                  │ └─────────────────┘ │
    └──────────┬──────────┘                                  └──────────┬──────────┘
               │                                                        │
               │ HTTP/SSE                                               │ HTTP/SSE
               │                                                        │
               ▼                                                        ▼
    ┌─────────────────────┐                                  ┌─────────────────────┐
    │  Users MCP Server   │                                  │  Fetch MCP Server   │
    │  localhost:8005/mcp │                                  │  remote.mcp...      │
    └─────────────────────┘                                  └─────────────────────┘


═══════════════════════════════════════════════════════════════════════════════════

                              🔄 EXAMPLE WORKFLOW

User Request: "Find info about Elon Musk and save as user 100"

Step 1: User → app.py → DialClient → GPT-4
        ↓
        GPT-4 decides: Need to fetch web info
        ↓
Step 2: GPT-4 → DialClient → MCPManager → MCPClient(web_fetch) → Fetch Server
        Tool Call: fetch("https://en.wikipedia.org/wiki/Elon_Musk")
        ↓
Step 3: Web content returned back through chain
        ↓
Step 4: DialClient → GPT-4 (with web content)
        GPT-4 processes content and decides: Need to create user
        ↓
Step 5: GPT-4 → DialClient → MCPManager → MCPClient(users_service) → Users Server
        Tool Call: create_user(id=100, name="Elon", surname="Musk", ...)
        ↓
Step 6: User created, success returned back through chain
        ↓
Step 7: DialClient → GPT-4 (with tool results)
        GPT-4 generates final response
        ↓
Step 8: Response streamed to User

═══════════════════════════════════════════════════════════════════════════════════

                           🔑 KEY DESIGN PRINCIPLES

1. 🎯 1-to-1 Connection
   Each MCPClient maintains exactly ONE connection to ONE MCP server

2. 🗺️  Tool Registry Pattern
   MCPClientManager maintains a map: tool_name → mcp_client_name
   Example: "get_user" → "users_service"
           "fetch" → "web_fetch"

3. 🔀 Transparent Routing
   LLM sees all tools as one unified set
   Routing happens automatically based on tool name

4. ♻️  Agent Loop
   1. Send messages to LLM
   2. LLM returns tool calls
   3. Execute tools via MCPManager
   4. Append results to messages
   5. Recurse until final answer

5. 🔒 Client Isolation
   Each MCP server has its own dedicated client
   No cross-contamination of contexts

═══════════════════════════════════════════════════════════════════════════════════

                              📊 TOOL ROUTING

┌────────────────────────────────────────────────────────────────────────────┐
│  Tool Name     │  MCP Server      │  Description                          │
├────────────────┼──────────────────┼───────────────────────────────────────┤
│  get_user      │  users_service   │  Retrieve user by ID                  │
│  create_user   │  users_service   │  Create new user profile              │
│  update_user   │  users_service   │  Update existing user                 │
│  delete_user   │  users_service   │  Delete user from system              │
│  search_users  │  users_service   │  Search users by criteria             │
│  fetch         │  web_fetch       │  Fetch content from URL               │
└────────────────┴──────────────────┴───────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════
""")


if __name__ == "__main__":
    print_architecture()
