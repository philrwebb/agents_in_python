# AGENTS.md - Project Conventions & Guidelines

## Project Overview

This project uses **uv** (PEP 738 virtual environment manager) to manage dependencies. It implements an AI agent framework with versioned assistants (v0-v4) and a unified `harness.py` for production use.

---

## Environment & Dependencies

### Python Version
- Use **Python 3.14.5+** (via `uv python pin`)
- Define in `.python-version`

### Dependency Management
- Use **uv** for all dependency operations:
  ```bash
  uv sync              # Install dependencies
  uv add PACKAGE       # Add dependency
  uv lock              # Update uv.lock
  uv run COMMAND       # Run with isolated venv
  ```
- Never modify `.venv` directly
- Always use `uv sync` after adding dependencies

---

## Code Organization

### Core Structure
```
root/
├── v0.py      # Minimal assistant (no tools)
├── v1.py      # Assistant with list_files, read_file
├── v2.py      # + write_file tool
├── v3.py      # + async MCP servers (time, fetch)
├── v4.py      # + memory persistence
├── harness.py # Unified framework (model switching, all tools, slash commands)
├── tools.py   # Reusable tool implementations (shares with workspace copy)
├── workspace/ # Working directory for assistants
└── pyproject.toml
```

### Tool Organization
- Local tools: `tools.py` (file I/O, shell scripts, memory, ABC news)
- MCP tools: Defined dynamically in `harness.py` via `MCP_SERVERS` config

---

## Coding Conventions

### Imports
- Group imports: stdlib, third-party, local
- Use `from ... import ...` to reduce imports
- Pin versions in `pyproject.toml`

### Types & Static Analysis
- Add type hints for all functions
- Enable **mypy** with strict checks
- Type: `str`, `dict`, `list`, `Path` (no dynamic types)
- Use `Path` for all file operations
- Use `cast()` only when necessary (annotated types preferred)

### File Paths
- All relative paths use `Path(__file__).parent / "workspace"`
- No hardcoded absolute paths
- File errors: `f"error: no {filename}"` (consistent format)

### Testing Strategy
- Write tests for:
  - Tool schema validation
  - Memory file operations
  - Shell script validation
- Use **pytest** with fixtures:
  ```python
  @pytest.fixture
  def sample_tool():
      return {tool_name: arg_value}
  ```

---

## Security Rules

### Shell Script Execution (`run_shell_script`)
**Allowlist approach** - Only allow trusted commands:
```python
# In harness.py handle_command:
ALLOWED_SHELL_CMDS = {"bash", "sh", "grep", "cat"}
```
**Never** execute untrusted scripts without validation.

### MCP Server Security
- Validate each server before connecting
- Log connection attempts for audit
- Require `--privileged` flag for sensitive operations

### Memory Security
- Never store secrets in `memory.md`
- Sanitize user input before saving to memory

---

## Configuration Files

### `.env` vs `.envcopy`
- `.env` (run-only): Secret API keys, local configs
- `.envcopy` (tracked): Template with placeholder values
- Never commit actual secrets to `.env`

### `mcp_servers.json`
- Tracks MCP server connections
- Format: `{ "mcpServers": { "name": { "command": "uvx", "args": ["...]"} } }`
- Loaded dynamically in `harness.py`

---

## SLA (Speed & Latency)

### Assistant Response Time
- Initial response: **< 5 seconds**
- Tool execution: **< 2 seconds**
- Total time (including model): **< 8 seconds**
- Use async for tools that could block

### Timeout & Retry Logic
```python
async def call_tool(name, args):
    # Try up to 3 times
    for attempt in range(3):
        try:
            result = await asyncio.wait_for(run_tool(), timeout=5.0)
            return result
        except asyncio.TimeoutError:
            log(f"tool {name} timed out")
            raise
```

---

## Development Workflow

### Adding a New Tool
1. Define in `tools.py` (implementation)
2. Add to `LOCAL_TOOLS` dict in `harness.py`
3. Add to `TOOL_SCHEMAS` (function schema)
4. Test: `uv run pytest tools/test_<tool_name>.py`

### Adding an MCP Server
1. Update `mcp_servers.json`
2. Load in `connect_mcp()` handler
3. Dynamic schema generation

### Updating MCP Tools
- Use **runtime** tool discovery (check `mcp_sessions`)
- Don't hardcode tool lists

### Memory Updates
- Use `save_memory()` for safe appends
- Consider batching with `memory.md` backup

---

## Error Handling & Logging

### Valid Input
- Validate all tool arguments (type + value)
- Return structured JSON errors

### System Exceptions
- Log non-silent exceptions
- Use logging instead of print for production

---

## Memory File (`memory.md`)

- Location: `memory.md` (tracked by `.gitignore`)
- Format: Markdown bullet list
- Append-only (with backup strategy)
- **Never** write secrets to memory

---

## Tool Implementation Guidelines

### File Tools
```python
def read_file(filename: str) -> str:
    path = WORKSPACE / filename
    return path.read_text(encoding="utf-8") if path.is_file() else f"error: no {filename}"
```

### Shell Script Tools
```python
def run_shell_script(filename, args=None, timeout=60):
    # Validate inputs
    # Execute with subprocess
    # Return JSON with exit_code, stdout, stderr
```

### Memory Tools
```python
def save_memory(fact: str) -> str:
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"- {fact}\n")
    return f"saved: {fact}"
```

---

## Deployment & Hot Reload

### Model Switching (`/model` command)
```python
# Change MODEL configuration via /model command
# No server restart required
```

### MCP Server Management
- Use `uvx` for ephemeral server instances
- No persistence needed between sessions
- `uvx --quiet ...` for cleaner output

---

## Production Readiness Checklist

- [ ] All tools have input validation
- [ ] Tool execution uses async where possible
- [ ] Memory file has backup/serialization hook
- [ ] Shell script execution allowslisted
- [ ] MCP servers load from config file
- [ ] Model switching works without restart
- [ ] Slash commands implemented
- [ ] Error handling logs appropriately

---

## Notes

- `v0.py`: Base (no tools, direct OpenAI calls)
- `v1.py`: Files only (list + read)
- `v2.py`: Files + write
- `v3.py`: Async MCP servers (time, fetch)
- `v4.py`: Memory persistence + conversation history
- `harness.py`: Production-ready (all features + config)
- `tools.py`: Reusable tools (can be shared across v1-v4)

Use **uv** for all dependency operations: `uv sync`, `uv add`, `uv run`.
