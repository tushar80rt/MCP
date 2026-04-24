import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client


nest_asyncio.apply() #Needed to run intrective python

"""
Make sure:
1. The server is running before runnig this script.
2. The server is configured to use SSE transport.
3. The server is listening on port 8050.

The run the server:
uv run server.py

"""

async def main():
  # Connect to the server using SSE
  async with sse_client("http://loacalhost:8000/sse") as (read_stream, write_stream):
    async with ClientSession(read_stream , write_stream) as session:
      # Initilize the connection
      await session.initialize()

      # List available tools
      tools_result = await session.list_tools()
      print("Available tools : ")
      for tool in tools_result:
        print(f"  - {tool.name}: {tool.description}")

      # Call our weather tool
      result = await session.call_tool("get_alerts" , arguments={"state":"CA"})
      print(f"The weather alerts are = {result.content[0].text}")


if __name__ == "__main__":
  asyncio.run(main())

