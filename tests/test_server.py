from fastapi.testclient import TestClient
import pytest
import json
from server import app, mcp

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_routes_exist():
    # Verify the SSE and messages endpoints are correctly registered in the FastAPI app
    routes = [route.path for route in app.routes]
    assert "/sse" in routes
    assert "/messages" in routes

@pytest.mark.asyncio
async def test_mcp_tool_registration():
    # Verify the calculate_sum tool is registered under MCP
    tools = await mcp.list_tools()
    tool_names = [tool.name for tool in tools]
    assert "calculate_sum" in tool_names
    
    # Check details of calculate_sum tool
    sum_tool = next(t for t in tools if t.name == "calculate_sum")
    assert "low" in sum_tool.inputSchema["properties"]
    assert "high" in sum_tool.inputSchema["properties"]

@pytest.mark.asyncio
async def test_mcp_tool_execution():
    # Verify calling the tool through FastMCP returns correct results
    response = await mcp.call_tool("calculate_sum", {"low": 1, "high": 10})
    assert len(response) == 1
    assert response[0].type == "text"
    
    data = json.loads(response[0].text)
    assert data["low"] == 1
    assert data["high"] == 10
    assert data["sum"] == 55
    assert "Successfully calculated" in data["message"]

@pytest.mark.asyncio
async def test_mcp_tool_execution_reversed():
    # Verify calling the tool with reversed bounds returns correct results
    response = await mcp.call_tool("calculate_sum", {"low": 10, "high": 1})
    assert len(response) == 1
    assert response[0].type == "text"
    
    data = json.loads(response[0].text)
    assert data["low"] == 10
    assert data["high"] == 1
    assert data["sum"] == 55
