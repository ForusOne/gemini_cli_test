import asyncio
import argparse
import sys
import json
from contextlib import AsyncExitStack
import logging

from mcp import ClientSession
from mcp.client.sse import sse_client

# Setup logging
logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("mcp_summation_client")

async def run_client(url: str, low: int, high: int):
    """
    Connects to the MCP server via SSE transport, executes the calculate_sum tool,
    and prints the formatted calculation results.
    """
    async with AsyncExitStack() as stack:
        try:
            # 1. Establish the SSE transport connection
            transport = await stack.enter_async_context(sse_client(url))
            
            # 2. Establish the Client session
            session = await stack.enter_async_context(
                ClientSession(transport[0], transport[1])
            )
            
            # 3. Initialize connection with the server
            await session.initialize()
            
            # 4. Invoke the calculate_sum tool
            response = await session.call_tool("calculate_sum", {"low": low, "high": high})
            
            if response.isError:
                print("Error: MCP Server returned an error.", file=sys.stderr)
                if response.content:
                    print(response.content[0].text, file=sys.stderr)
                sys.exit(1)
                
            if not response.content:
                print("Error: Received empty response from MCP Server.", file=sys.stderr)
                sys.exit(1)
            
            # Parse response
            response_text = response.content[0].text
            try:
                data = json.loads(response_text)
                
                # Pretty print results
                print("\n" + "=" * 50)
                print("           MCP SUMMATION RESULT")
                print("=" * 50)
                print(f"  Range:  [{data.get('low')} ... {data.get('high')}]")
                print(f"  Sum:    {data.get('sum'):,}")
                print(f"  Info:   {data.get('message')}")
                print("=" * 50 + "\n")
                
            except json.JSONDecodeError:
                # Fallback to plain text print
                print("Result:")
                print(response_text)
                
        except Exception as e:
            print(f"Error: Failed to communicate with MCP Server. Details: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Query the MCP Summation Server for a range calculation."
    )
    parser.add_argument(
        "-l", "--low",
        type=int,
        required=True,
        help="Lower boundary of the range"
    )
    parser.add_argument(
        "-u", "--high",
        type=int,
        required=True,
        help="Upper boundary of the range"
    )
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8080/sse",
        help="The server SSE endpoint URL (default: http://localhost:8080/sse)"
    )
    
    args = parser.parse_args()
    
    asyncio.run(run_client(args.url, args.low, args.high))

if __name__ == "__main__":
    main()
