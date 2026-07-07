from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount, Route
import logging

from summation import calculate_sum as do_calculate_sum

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_summation_server")

# 1. Initialize FastMCP
mcp = FastMCP("MCP Summation Server")

# 2. Register the tool
@mcp.tool()
def calculate_sum(low: int, high: int) -> dict:
    """
    Calculates the sum of all integers between low and high (inclusive).
    
    If low > high, automatically swaps them and logs a warning.
    Uses O(1) analytical formula for performance and safety.
    """
    logger.info(f"Received calculate_sum request with low={low}, high={high}")
    result = do_calculate_sum(low, high)
    return {
        "low": low,
        "high": high,
        "sum": result,
        "message": f"Successfully calculated the sum of integers from {min(low, high)} to {max(low, high)}."
    }

# 3. Setup SSE Transport
# Note: FastAPI/Starlette handles trailing slash routing beautifully.
sse = SseServerTransport("/messages")

async def handle_sse(request: Request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await mcp._mcp_server.run(
            streams[0], streams[1], mcp._mcp_server.create_initialization_options()
        )

# 4. Create FastAPI app
app = FastAPI(title="MCP Summation Server", version="1.0.0")

# Register health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Mount SSE endpoints using routing list
app.router.routes.append(Route("/sse", endpoint=handle_sse, methods=["GET"]))
app.router.routes.append(Mount("/messages", app=sse.handle_post_message))

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
