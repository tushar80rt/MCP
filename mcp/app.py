from langchain_groq import ChatGroq
from dotenv import load_dotenv
from mcp_use import MCPAgent , MCPClient
import os
import asyncio

async def run_memory_chat():
  """Run a  chat using MCPAgent built in converstional memory"""
  load_dotenv()
  os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# configure file path - change this to your own file path
  config_file = "browser_mcp.json"
  print("Initializing chat...")


  # create MCP client and agent with memory enabled
  client = MCPClient.from_config_file(config_file)
  llm = ChatGroq(
    model="openai/gpt-oss-120b",
    max_tokens=1000,
    temperature=0.1
)


  # create agent with memory enabled = True
  agent = MCPAgent(
    llm=llm,
    client=client,
    max_steps=15,
    memory_enabled=True  #Enabled built-in conversation memory
  )


  print("\n ==== Interactive MCP Chat====")
  print("Type 'exit or 'quit' to end the chat")
  print("Type 'clear' to clear the memory")
  print("==========================\n")

  try:
    # Main chat loop
    while True:
      user_input = input("\nYou: ")

      # check for exit commands
      if user_input.lower() in ['exit' , 'quit']:
        print("Ending conversation...")
        break

      # Check for clear history command
      if user_input.lower() == 'clear':
        agent.clear_conversation_history()
        print("Cleared conversation history...")
        continue

      print("\n Assistant: ", end="", flush=True)
      # get Response from agent
      try:
        response = await agent.run(user_input)
        print(response)

      except Exception as e:
        print(f"\nError: {e}")

  finally:
    # clean up - close MCP client
    print("\nClosing MCP client...")
    if client and client.sessions:
      await client.close_all_sessions()
    print("Chat ended. Thank you!")

if __name__ == "__main__":
  asyncio.run(run_memory_chat())

