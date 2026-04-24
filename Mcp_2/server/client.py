import asyncio
from langchain_groq import ChatGroq
from mcp_use import MCPAgent , MCPClient, config
import os
from dotenv import load_dotenv

def create_memory_agent(config_file: str = "server/weather.json") -> tuple[MCPAgent, MCPClient]:
  """Create and return an MCP agent with memory + its client."""
  load_dotenv()
  os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

  client = MCPClient.from_config_file(config_file)
  llm = ChatGroq(model = "openai/gpt-oss-120b")

  agent = MCPAgent(
    llm=llm,
    client=client,
    max_steps=5,
    memory_enabled=True
  )
  return agent, client


async def close_client_sessions(client: MCPClient) -> None:
  """Close open MCP client sessions safely."""
  if client and client.sessions:
    await client.close_all_sessions()


async def run_memory_chat():
  """ Run a chat using Mcp Agent's built-in coversation memory. """
  print("Initializing chat...")

  # Create MCP Client and agent with memory enabled
  agent, client = create_memory_agent()


  print("\n============Intrective MCP Chat================")
  print("Type 'exit'  or 'quit' to end the conversation")
  print("Type 'clear' to clear this  conversation history")


  try:
    while True:
      user_input = input("\n You: ")

      if user_input.lower() in ("exit", "quit"):
        print("Your chat has Quited")
        break

      if user_input.lower() == "clear":
        agent.clear_conversation_history()
        print("Your conversation history cleared")
        continue


      print("\n Assistant: ", end=" ", flush=True)

      try:
        response = await agent.run(user_input)
        print(response)

      except Exception as e:
        print(f"\n Error {e}")

  finally:
    # Clean
    await close_client_sessions(client)



if __name__ == "__main__":
  asyncio.run(run_memory_chat())



