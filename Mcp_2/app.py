import asyncio

import streamlit as st
from mcp_use import MCPAgent

from server.client import create_memory_agent


def get_event_loop() -> asyncio.AbstractEventLoop:
    """Create/reuse one event loop per Streamlit session."""
    loop = st.session_state.get("event_loop")
    if loop is None or loop.is_closed():
        loop = asyncio.new_event_loop()
        st.session_state["event_loop"] = loop
    return loop


def initialize_agent() -> MCPAgent:
    """Initialize agent by importing setup from server/client.py."""
    agent, _ = create_memory_agent()
    return agent


def run_async(coro):
    """Run async calls from Streamlit safely on a dedicated loop."""
    loop = get_event_loop()
    return loop.run_until_complete(coro)


def reset_chat():
    """Clear Streamlit chat + MCP agent memory."""
    agent = st.session_state.get("agent")
    if agent is not None:
        agent.clear_conversation_history()
    st.session_state["messages"] = []


st.set_page_config(page_title="MCP Weather Chat", page_icon="⛅", layout="centered")
st.title("MCP Weather Assistant")
st.caption("Powered by Streamlit + MCP Agent (`server/client.py` setup)")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "agent" not in st.session_state:
    try:
        st.session_state["agent"] = initialize_agent()
    except Exception as exc:
        st.error(f"Failed to initialize agent: {exc}")
        st.stop()

with st.sidebar:
    st.subheader("Controls")
    if st.button("Clear chat", use_container_width=True):
        reset_chat()
        st.rerun()

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask weather alerts like: Any alerts for CA?")
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = run_async(st.session_state["agent"].run(prompt))
            except Exception as exc:
                response = f"Error: {exc}"
        st.markdown(response)

    st.session_state["messages"].append({"role": "assistant", "content": response})
