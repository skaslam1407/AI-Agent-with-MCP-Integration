# User Guide

## Getting Started

### Prerequisites

1. Python 3.10 or higher
2. An OpenAI API key (or compatible API endpoint)
3. Virtual environment (recommended)

### Setup

1. **Clone/navigate to the project directory**
   ```bash
   cd agent
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   BASE_URL=https://api.openai.com/v1
   API_KEY=sk-your-openai-api-key
   MODEL=gpt-4o-mini
   ```

## Running the Agent

### Option 1: Two Terminals (Recommended)

**Terminal 1 - Start the MCP Server:**
```bash
python server.py
```
You should see: `Starting MCP server..`

**Terminal 2 - Run the Agent:**
```bash
python runner.py
```

### Option 2: Single Terminal (Background Server)
```bash
python server.py &
python runner.py
```

## Using the Agent

Once running, you'll see:
```
Available Tools
----------------
current_time
roll_dice
generate_password

User : 
```

Type your request and press Enter. Examples:
- "What time is it?"
- "Roll a dice for me"
- "Generate a 16-character password"
- "What time is it and roll a dice?"

Type `exit` or press `Ctrl+C` to quit.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `current_time` | Returns current date/time | None |
| `roll_dice` | Returns random 1-6 | None |
| `generate_password` | Generates secure password | `length` (optional, default: 12) |

## How It Works

1. **User Request** → Entered at prompt
2. **Planner** (OpenAI) → Decides which tool to use next
3. **Executor** → Calls the tool via MCP
4. **Observation** → Result returned to planner
5. **Loop** → Repeats until `FINISH` or max iterations
6. **Formatter** → Creates natural language response

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `BASE_URL` | OpenAI API base URL | `https://api.openai.com/v1` |
| `API_KEY` | Your API key | Required |
| `MODEL` | Model to use | `gpt-4o-mini` |

## Troubleshooting

### "Connection refused" error
- Ensure MCP server is running (`python server.py`)
- Check server.py is in the same directory

### "API key invalid" error
- Verify `API_KEY` in `.env` is correct
- Check `BASE_URL` matches your provider

### No tools showing
- Server must be running before `runner.py`
- Restart both if tools don't appear

## Extending the Agent

### Adding New Tools

1. Edit `server.py` and add a new `@mcp.tool()` function
2. Restart the MCP server
3. The agent will automatically discover the new tool

### Customizing the Planner

Edit `planner.py` to modify:
- System prompt
- Planning rules
- Response format

### Adjusting Loop Behavior

Edit `loop.py` to change:
- Maximum iterations
- Loop logic
- State management