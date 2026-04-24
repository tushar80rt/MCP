# MCP — Model Context Protocol Experiments

<div align="center">

[![License](https://img.shields.io/github/license/tushar80rt/MCP?style=flat-square)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/tushar80rt/MCP?style=flat-square)](https://github.com/tushar80rt/MCP/commits/main)
[![Open Issues](https://img.shields.io/github/issues/tushar80rt/MCP?style=flat-square)](https://github.com/tushar80rt/MCP/issues)
[![Stars](https://img.shields.io/github/stars/tushar80rt/MCP?style=flat-square)](https://github.com/tushar80rt/MCP/stargazers)
[![Forks](https://img.shields.io/github/forks/tushar80rt/MCP?style=flat-square)](https://github.com/tushar80rt/MCP/network/members)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue?style=flat-square&logo=python)](https://www.python.org/)

</div>

> A collection of hands-on **Model Context Protocol (MCP)** examples built with Python, LangChain, and Groq — covering interactive CLI agents, a Streamlit weather assistant, a Dockerised MCP server, and LangChain adapter patterns.

---

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [mcp — Browser-Enabled Chat Agent](#mcp--browser-enabled-chat-agent)
  - [Mcp\_2 — Weather Assistant (Streamlit + Custom Server)](#mcp_2--weather-assistant-streamlit--custom-server)
  - [mcp\_langchain — LangChain MCP Adapters](#mcp_langchain--langchain-mcp-adapters)
- [Usage](#usage)
  - [mcp](#mcp-usage)
  - [Mcp\_2](#mcp_2-usage)
  - [mcp\_langchain](#mcp_langchain-usage)
- [Configuration](#configuration)
- [Docker](#docker)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Model Context Protocol (MCP)** is an open standard that lets AI agents interact with external tools and data sources through a unified interface. This repository contains three self-contained example projects that explore different patterns for building MCP-powered applications:

| Project | Description |
|---------|-------------|
| [`mcp/`](mcp/) | Interactive CLI chat agent that controls a browser, searches DuckDuckGo, and browses Airbnb listings using MCP tools |
| [`Mcp_2/`](Mcp_2/) | Weather assistant with a Streamlit web UI backed by a custom MCP server that queries the US National Weather Service (NWS) API |
| [`mcp_langchain/`](mcp_langchain/) | Demonstrates how to connect multiple MCP servers (math & weather) through the LangChain MCP adapters library |

---

## Repository Structure

```
MCP/
├── mcp/                        # Project 1 — Browser-enabled chat agent
│   ├── app.py                  # Interactive CLI chat loop (entry point)
│   ├── browser_mcp.json        # MCP server config (Playwright, Airbnb, DuckDuckGo)
│   ├── requirements.txt
│   └── pyproject.toml
│
├── Mcp_2/                      # Project 2 — Weather assistant + Streamlit UI
│   ├── app.py                  # Streamlit web UI (entry point)
│   ├── server/
│   │   ├── client.py           # MCP agent factory used by the UI
│   │   ├── weather.py          # Custom weather MCP server (NWS API)
│   │   └── weather.json        # MCP config pointing to weather.py
│   ├── mcpserver/              # Standalone MCP server (SSE transport + Docker)
│   │   ├── server.py           # Weather server — SSE & stdio transports
│   │   ├── Dockerfile
│   │   ├── client-sse.py       # SSE client example
│   │   ├── client-stdio.py     # stdio client example
│   │   └── requirements.txt
│   └── pyproject.toml
│
└── mcp_langchain/              # Project 3 — LangChain MCP adapters demo
    ├── client.py               # Multi-server agent (entry point)
    ├── mathserver.py           # MCP server exposing add / multiply tools
    ├── weather.py              # MCP server exposing a weather tool
    ├── requirements.txt
    └── pyproject.toml
```

---

## Features

### `mcp/` — Browser-Enabled Chat Agent
- 🌐 **Browser automation** via Playwright MCP server
- 🔍 **Web search** via DuckDuckGo MCP server
- 🏠 **Airbnb listings** via OpenBnB MCP server
- 💬 **Persistent conversation memory** powered by `mcp-use`
- ⌨️ **Interactive CLI** with `exit`, `quit`, and `clear` commands

### `Mcp_2/` — Weather Assistant
- ⛅ **Real-time weather alerts** from the US National Weather Service (NWS) API
- 🌡️ **Weather forecast** by latitude/longitude (standalone server)
- 🖥️ **Streamlit web UI** for a chat-based experience
- 🐳 **Docker support** for the standalone MCP server
- 🔌 **Both SSE and stdio transports** supported

### `mcp_langchain/` — LangChain MCP Adapters
- ➕ **Math server** with `add` and `multiply` tools
- 🌦️ **Weather server** with a `get_weather` tool
- 🔗 **Multi-server** orchestration via `langchain-mcp-adapters`
- 📡 **Mixed transports** (stdio + streamable HTTP)

---

## Prerequisites

- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** (recommended package manager)  
  ```bash
  pip install uv
  ```
- **Node.js / npx** — required only by `mcp/` for the browser MCP servers
- **[Groq API key](https://console.groq.com/)** — used by all three projects as the LLM provider
- **Docker** (optional) — only for the `Mcp_2/mcpserver/` standalone server

---

## Installation & Setup

Each project is independent. Navigate into the relevant directory and follow the steps below.

### `mcp/` — Browser-Enabled Chat Agent

```bash
cd mcp

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

Create a `.env` file in the `mcp/` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### `Mcp_2/` — Weather Assistant (Streamlit + Custom Server)

```bash
cd Mcp_2

uv venv
source .venv/bin/activate
uv pip install -e .
```

Create a `.env` file in the `Mcp_2/` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### `mcp_langchain/` — LangChain MCP Adapters

```bash
cd mcp_langchain

uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Create a `.env` file in the `mcp_langchain/` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## Usage

### `mcp` Usage

Run the interactive CLI agent. It will connect to the Playwright, Airbnb, and DuckDuckGo MCP servers automatically (requires `npx` to be available):

```bash
cd mcp
source .venv/bin/activate
python app.py
```

**Example session:**

```
Initializing chat...

 ==== Interactive MCP Chat====
Type 'exit or 'quit' to end the chat
Type 'clear' to clear the memory
==========================

You: Search for pet-friendly Airbnb listings in Austin, TX
 Assistant: Here are some pet-friendly options in Austin...

You: clear
Cleared conversation history...

You: exit
Ending conversation...
```

---

### `Mcp_2` Usage

#### Streamlit Web UI

Launch the Streamlit app — it starts the weather MCP server in the background automatically:

```bash
cd Mcp_2
source .venv/bin/activate
streamlit run app.py
```

Open your browser at **http://localhost:8501** and ask questions like:
- *"Any active weather alerts for CA?"*
- *"Are there storm warnings in TX?"*

#### CLI Chat (no UI)

```bash
cd Mcp_2
source .venv/bin/activate
python server/client.py
```

#### Standalone MCP Server (SSE transport)

```bash
cd Mcp_2/mcpserver
uv run server.py
# Server starts on http://localhost:8000
```

Then in a second terminal, run the SSE client example:

```bash
python client-sse.py
```

Or the stdio client example (starts the server as a subprocess):

```bash
python client-stdio.py
```

---

### `mcp_langchain` Usage

Start the weather HTTP server first, then run the multi-server agent:

```bash
# Terminal 1 — start the weather server
cd mcp_langchain
source .venv/bin/activate
python weather.py   # listens on http://localhost:8000/mcp

# Terminal 2 — run the agent (math server starts automatically via stdio)
python client.py
```

**Expected output:**

```
math message:  The result of (3+5) × 12 is 96.
weather response:  It's always raining in California.
```

---

## Configuration

All projects read secrets from a `.env` file in their respective directories. The `.gitignore` already excludes `.env`.

| Variable | Required By | Description |
|----------|-------------|-------------|
| `GROQ_API_KEY` | `mcp/`, `Mcp_2/`, `mcp_langchain/` | API key from [console.groq.com](https://console.groq.com/) |

### MCP Server Config Files

| File | Project | Description |
|------|---------|-------------|
| `mcp/browser_mcp.json` | `mcp/` | Defines Playwright, Airbnb, and DuckDuckGo MCP servers |
| `Mcp_2/server/weather.json` | `Mcp_2/` | Points to the local `server/weather.py` MCP server |

---

## Docker

The `Mcp_2/mcpserver/` directory contains a Dockerfile for running the standalone weather MCP server in a container.

### Build the image

```bash
cd Mcp_2/mcpserver
docker build -t mcp-weather-server .
```

### Run the container

```bash
docker run -p 8000:8000 mcp-weather-server
```

The server exposes the following MCP tools via SSE at **http://localhost:8000**:

| Tool | Description |
|------|-------------|
| `get_alerts(state)` | Active weather alerts for a US state (e.g. `CA`, `NY`) |
| `get_forecast(latitude, longitude)` | 5-period weather forecast for any US location |

---

## Development

### Virtual environments

Each sub-project uses its own virtual environment managed by `uv`:

```bash
cd <project-dir>
uv venv
source .venv/bin/activate
```

### Adding dependencies

```bash
uv pip install <package>
uv pip freeze > requirements.txt   # update requirements.txt
```

### Code style

There are no enforced linting configurations in this repository. Contributions are encouraged to follow [PEP 8](https://pep8.org/) and use a formatter such as `ruff` or `black`:

```bash
pip install ruff
ruff check .
ruff format .
```

---

## Contributing

Contributions, issues, and feature requests are welcome!

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Commit** your changes: `git commit -m "feat: add your feature"`
4. **Push** to the branch: `git push origin feature/your-feature`
5. **Open a Pull Request** against `main`

Please keep each sub-project self-contained and update any relevant documentation.

---

## License

This project is open source. See the [LICENSE](LICENSE) file for details. If no LICENSE file is present, the default copyright laws apply.

---

<div align="center">

Made with ❤️ by [tushar80rt](https://github.com/tushar80rt)

</div>
