# Python Development Project

A collection of Python development resources and educational materials.

---

## 📚 Python Files

> **Note:** No `.py` source files currently exist in this workspace. The Python content consists of:
> - `python_doc.md` - Complete Python language documentation (11 sections, January 2025)
> - `python.md` - Python OOP concepts and patterns (last updated 2024)
> - `v0.py` through `v4.py` - Personal assistant agent versions with increasing capabilities
> - `harness.py` - Complete production-ready agent infrastructure

---

## 🔄 Assistant Agent Evolution (v0-v4)

### **v0.py** - Basic Chat Assistant
**What:** Simple chat interface with OpenAI integration
**Key Features:**
- Uses `Qwen3.5-4B-4bit` model (local, not API)
- Reads from `http://127.0.0.1:8000/v1`
- Basic single-shot chat with user messages
- No tools - just conversation
- Interactive CLI loop (`ctrl+c` to quit)

**Changes from previous:** Initial version with basic model configuration

---

### **v1.py** - Tool-Enhanced Assistant
**What:** Chat assistant with workspace tools
**Key Features:**
- Adds **3 tools**: `list_files()`, `read_file(filename)`, `write_file(filename, content)`
- Tool schemas defined for OpenAI function calling
- Single-shot tool execution model
- Inline tool execution (runs immediately when model requests it)
- Tracks tool calls with JSON parsing

**Improvement over v0:**
- Extends basic chat with file system operations
- Model can "talk to tools" through JSON schema
- Single-shot tool execution pattern

---

### **v2.py** - Iterative Tool Agent
**What:** Enhanced tool orchestration with write capability
**Key Features:**
- Adds `write_file` tool (previously only read)
- **Multi-shot loop:** Instead of single-shot, implements iterative agent loop
  - Model responds with tool call → execute tool → continue loop
  - Continues until assistant message (no tool_call)
- Maintains `LOCAL_TOOLS` dictionary
- Same OpenAI `OpenAI` client (synchronous)

**Improvement over v1:**
- Adds file write capability (full read-write access)
- Introduces **iterative loop pattern** - tool calls can be chained
- Model can make multiple tool calls in sequence

---

### **v3.py** - Async MCP Integration
**What:** Asynchronous MCP-based agent with remote servers
**Key Features:**
- **Async/Await:** All `run_agent()` and `call_tool()` are now `async`
- Adds **MCP (Model Context Protocol)** integration
- `MCP_SERVERS` dictionary with `time` and `fetch` servers
- `connect_mcp()` starts MCP servers via `asyncio` and `AsyncExitStack`
- `mcp_sessions` dictionary tracks which sessions are running
- `call_tool()` routes to local tools OR MCP server tools via MCP protocol
- `AsyncOpenAI` client (async instead of sync)
- CLI loop uses `asyncio.to_thread()` for synchronous `input()`

**Improvements over v2:**
- Adds **external MCP servers** (time, fetch)
- Tools can now come from MCP servers, not just local
- **Asynchronous execution** - faster startup, more efficient
- Merges local tools + MCP server tools into unified `TOOL_SCHEMAS`

---

### **v4.py** - Full-Fledged Harness with Memory
**What:** Complete agent infrastructure with model registry, memory, and MCP config
**Key Features:**
- **Model Registry:** `ModelConfig` class with config for multiple models
- `memory.md` file for user memory storage (persistent)
- `mcp_servers.json` config file for MCP servers
- **Slash commands:** `/models`, `/model <name>`, `/tools`, `/memory`, `/quit`
- **Tool origin tracking:** distinguishes local vs MCP tools
- `handle_command()` parses and handles slash commands
- Global `messages` list shared across all model switches
- CLI handles commands in addition to normal chat

**Comprehensive Features:**
- **Pillar 1 (MCP):** Manages MCP server connections dynamically
- **Pillar 2 (Memory):** Loads memory before each session
- **Pillar 3 (Model Registry):** Supports multiple models (including cloud endpoints)
- **Systems:** Memory file, MCP config, unified tool dispatch

**Major Improvements over v3:**
- Full model registry (not just single model)
- Config file-based MCP server management
- Conversation history persists across model switches
- Multi-command CLI interface
- Production-ready configuration management

---

## 📁 Project Structure

### Core Python Files
- `python_doc.md` - Complete Python language reference
- `python.md` - Python OOP concepts and patterns

### Web Content
- `index.html` - Main HTML page
- `style.css` - CSS styles
- `code.js` - JavaScript code
- `techwithtim.md` - Tech/programming content

### Personal Documents
- `sonnet.txt` - Personal notes (sonnet)
- `copysonnet.txt` - Copy of sonnet
- `PLC.md` - PLC-related documentation
- `test.txt` - Test file
- `hello.txt` - Simple content
- `copytext.txt` - Copy file

---

## 🎯 Design Patterns Used

### 1. **Tool Registration Pattern**
```python
TOOLS: dict[str, Callable] = {"tool_name": tool_func}
TOOL_SCHEMAS: list[ToolSchema] = [...]
```
Tools are registered and their schemas are automatically built for LLM function calling.

### 2. **Iterative Agent Loop**
Instead of single-shot response, implement loop that:
1. Get response from model
2. If tool call → execute tool, continue loop
3. When no tool call → return response

### 3. **Async Tool Routing**
```python
async def call_tool(name, args):
    if name in LOCAL_TOOLS:
        return LOCAL_TOOLS[name](**args)
    result = await mcp_sessions[name].call_tool(name, args)
    return result
```
Single function routes to local or MCP servers.

### 4. **Memory Layer**
```python
def load_memory() -> str
def save_memory(fact: str) -> str
# Memory file served as system prompt
```
User memory is loaded into conversation and can be persisted.

---

## 📦 Dependencies

```yaml
# Required packages
python-dotenv
openai>=1.0.0
mcp>=0.0.0
pydantic>=2.0.0
# uvx (for MCP server commands)
```

---

## 🛠️ Configuration Structure (v4)

```yaml
# ~/.env (optional)
LOCAL_API_KEY=your_key

# ~/.mcp_servers.json
{
  "mcpServers": {
    "time": {"command": "uvx", "args": ["mcp-server-time"]},
    "fetch": {"command": "uvx", "args": ["mcp-server-fetch"]}
  }
}
```

---

## 📝 Usage Examples

### Basic Chat (v0)
```python
python v0.py
# Interact in CLI, conversation flows naturally
```

### Tool Usage (v1-v2)
```python
python v2.py
# Model can call:
# - list_files() (no args)
# - read_file("README.md") (filename: "README.md")
# - write_file("new.txt", "content here") (filename, content)
```

### MCP Integration (v3-v4)
```python
python v3.py
# Model can also call:
# - time() - get current time
# - fetch(url) - fetch URL content
```

### Full Harness (v4)
```python
python v4.py
# Interactive CLI with slash commands:
# /models      - list available models
# /model qwen - switch model
# /tools      - list all tools (with origin)
# /memory     - view memory
# /quit       - exit
```

---

## 🌟 harness.py - Complete Production Harness

### **Overview**
`harness.py` is the most complete and production-ready implementation, integrating and extending all the concepts from v0-v4 into a unified, configurable system. It's essentially a supercharged v4 with enhanced architecture and proper separation of concerns.

### **Purpose**
`harness.py` serves as a complete infrastructure layer for deploying and managing a multi-model, tool-enabled, memory-aware AI assistant. It provides:
- Centralized configuration management
- Multiple model support with dynamic switching
- Persistent memory storage
- Dynamic MCP server management
- Slash command interface for runtime configuration

### **Key Components**

#### **1. Model Registry (Pillar 1)**
```python
class ModelConfig(BaseModel):
    base_url: str
    api_key: str
    model: str

MODELS: dict[str, ModelConfig] = {
    "local": ModelConfig(
        base_url="http://127.0.0.1:8000/v1",
        api_key=os.environ["LOCAL_API_KEY"],
        model="Qwen3.5-4B-4bit",
    ),
}
```
- Centralizes all model configurations
- Supports cloud endpoints and local servers
- Dynamic model switching via slash commands

#### **2. Memory System (Pillar 2)**
```python
def load_memory() -> str
def save_memory(fact: str) -> str

MEMORY_FILE = ROOT / "memory.md"
SYSTEM_PROMPT = f"""You are a helpful personal assistant running inside a \
custom harness. Be concise.

Here is what you remember about the user from previous sessions:
{load_memory()}
"""
```
- Persists user information to `memory.md`
- Loads memory into conversation context
- Tools to add, read, and view memory

#### **3. MCP Server Management**
```python
async def connect_mcp(stack: AsyncExitStack):
    config = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
    for name, spec in config["mcpServers"].items():
        params = StdioServerParameters(command=spec["command"], args=spec["args"])
        # Start each MCP server
```
- Reads from `mcp_servers.json` configuration file
- Dynamically starts and manages MCP server connections
- Supports multiple MCP servers simultaneously
- Handles connection failures gracefully

#### **4. Unified Tool Dispatch**
```python
async def call_tool(name: str, args: dict) -> str:
    if name in LOCAL_TOOLS:
        return LOCAL_TOOLS[name](**args)
    if name in mcp_sessions:
        result = await mcp_sessions[name].call_tool(name, args)
        return result
    return f"error: unknown tool {name}"
```
- Routes tool execution based on tool origin
- Single entry point for all tools
- Type-Checking with Pydantic validation

#### **5. Slash Command Handler**
```python
def handle_command(line: str) -> bool:
    """Returns True if the line was a command."""
    global model_name
    if not line.startswith("/"):
        return False
    cmd, _, arg = line.partition(" ")
    if cmd == "/models":
        for name, cfg in MODELS.items():
            marker = "*" if name == model_name else " "
            print(f" {marker} {name:<12} {cfg.model}  ({cfg.base_url})")
    elif cmd == "/model":
        if arg in MODELS:
            model_name = arg
            print(f"  switched to {arg} ({MODELS[arg].model})")
    elif cmd == "/tools":
        for schema in TOOL_SCHEMAS:
            if schema["type"] != "function":
                continue
            print(f"  [{schema.get('origin', 'local')}] {schema['name']}")
    # ... more commands
```
- Runtime configuration interface
- Model switching
- Tool listing
- Memory viewing
- Graceful exit command

#### **6. Async Agent Loop**
```python
async def run_agent(user_message: str) -> str:
    cfg = MODELS[model_name]
    client = AsyncOpenAI(base_url=cfg.base_url, api_key=cfg.api_key)
    messages.append({"role": "user", "content": user_message})
    while True:
        response = await client.chat.completions.create(
            model=cfg.model, messages=messages, tools=TOOL_SCHEMAS
        )
        # Process tool calls, continue loop
```
- Uses `AsyncOpenAI` for all model calls
- Maintains global message history
- Returns conversation with remembered context
- Async-friendly design

---

## 🚀 Recommended Usage

### **Installation & Setup**
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
# Copy .env.example to .env
cp .env.example .env
# Edit .env with your LOCAL_API_KEY
```

3. Configure MCP servers:
```json
// Edit mcp_servers.json
{
  "mcpServers": {
    "time": {"command": "uvx", "args": ["mcp-server-time"]},
    "fetch": {"command": "uvx", "args": ["mcp-server-fetch"]}
  }
}
```

### **Running the Harness**
```bash
python harness.py
# Start the interactive CLI
```

### **Interactive Commands**
```bash
# List all available models
/models

# Switch model (e.g., to "mistral")
/model mistral

# List all tools
/tools

# View current memory
/memory

# Exit the CLI
/quit
```

### **Normal Conversation**
After typing `/quit`, the harness:
1. Accepts normal conversation
2. Maintains message history across all model switches
3. Automatically remembers user facts
4. Supports MCP server tools (time, fetch, etc.)

---

## 💡 Key Advantages of harness.py

| Feature | Benefit |
|---------|---------|
| **Model Registry** | Switch between models at runtime without restarting |
| **Config-Driven** | All MCP servers defined in `mcp_servers.json` |
| **Persistent Memory** | User facts saved to `memory.md` across sessions |
| **Async Design** | Faster startup, efficient resource management |
| **Type-Safe** | Pydantic validation for model configurations |
| **Error Recovery** | Graceful handling of failed MCP connections |
| **Slash Commands** | Runtime configuration without code changes |
| **Unified Tool Dispatch** | Single entry point for all tools (local or MCP) |

---

## 📊 Version Comparison Summary

| Version | Async | Tools | Memory | MCP | Models | Slash Commands | Status |
|---------|-------|-------|--------|-----|--------|---------------|--------|
| **v0** | ❌ | None | ❌ | ❌ | ❌ | ❌ | Basic |
| **v1** | ❌ | 2 | ❌ | ❌ | ❌ | ❌ | Simple |
| **v2** | ❌ | 3 | ❌ | ❌ | ❌ | ❌ | Multi-shot |
| **v3** | ✅ | 3 + MCP | ❌ | ✅ | ❌ | ❌ | Async |
| **v4** | ✅ | 3 + MCP | ✅ | ✅ | ❌ | ✅ | Full |
| **harness.py** | ✅ | 4 + MCP | ✅ | ✅ | ✅ | ✅ | **Production** |

---

## 🌟 Project Summary

This workspace contains:
- **Complete Python language documentation** (`python_doc.md`, `python.md`)
- **5 companion agent versions** (`v0.py` through `v4.py`, `harness.py`) demonstrating progressive evolution:
  - v0: Basic chat
  - v1: Simple tools with function calling
  - v2: Multi-shot iterative tool execution
  - v3: Async + MCP integration
  - v4: Memory persistence + config files
  - **harness.py**: Complete production infrastructure with model registry, dynamic MCP management, and slash command interface

The progression demonstrates a clear evolution from simple chatbot to full-featured local AI assistant with memory, MCP connectivity, multi-model support, and production-ready architecture.

`harness.py` represents the culmination of this evolution, providing a production-ready foundation for deploying a configurable, scalable AI assistant with persistent memory and external tool integration.

---

*Last updated: 2025*
