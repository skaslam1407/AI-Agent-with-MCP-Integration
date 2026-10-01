# AI Agent with MCP Integration

An AI agent that uses the Model Context Protocol (MCP) to interact with external tools through a planning and execution loop.

## Features

- **Planning**: Uses OpenAI to plan the next action based on user requests
- **Execution**: Executes tools via MCP (Model Context Protocol)
- **Tools Available**:
  - `current_time` - Get current date and time
  - `roll_dice` - Roll a six-sided dice
  - `generate_password` - Generate secure passwords

## Requirements

- Python 3.10+
- OpenAI API compatible endpoint
- MCP Server (included as `server.py`)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with the following variables:

```env
BASE_URL=https://api.openai.com/v1
API_KEY=your_api_key_here
MODEL=gpt-4o-mini
```

## Usage

### Start the MCP Server (in one terminal)

```bash
python server.py
```

### Run the Agent (in another terminal)

```bash
python runner.py
```

Then enter your request when prompted.

## Project Structure

```
agent/
├── server.py          # MCP server with tools
├── mcp_client.py      # MCP client for tool communication
├── planner.py         # AI planner using OpenAI
├── executor.py        # Tool executor
├── loop.py            # Agent planning/execution loop
├── runner.py          # Main entry point
├── state.py           # State management
├── requirements.txt   # Python dependencies
└── .env               # Environment variables
```