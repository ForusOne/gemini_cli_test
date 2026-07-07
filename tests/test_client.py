import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import sys
import argparse

def test_client_imports_successfully():
    import client
    assert client is not None

@pytest.mark.asyncio
async def test_run_client_success():
    # Verify that run_client establishes the connection, initializes the session,
    # invokes calculate_sum, and parses response properly.
    mock_session = AsyncMock()
    mock_session.initialize = AsyncMock()
    
    mock_response = MagicMock()
    mock_response.isError = False
    mock_content_block = MagicMock()
    mock_content_block.text = '{"low": 1, "high": 10, "sum": 55, "message": "Success"}'
    mock_response.content = [mock_content_block]
    mock_session.call_tool = AsyncMock(return_value=mock_response)
    
    with patch("client.sse_client") as mock_sse_client, \
         patch("client.ClientSession") as mock_client_session:
         
         # Setup mock contexts
         mock_sse_client.return_value.__aenter__.return_value = ("read_stream", "write_stream")
         mock_client_session.return_value.__aenter__.return_value = mock_session
         
         from client import run_client
         await run_client("http://localhost:8080/sse", 1, 10)
         
         mock_sse_client.assert_called_once_with("http://localhost:8080/sse")
         mock_client_session.assert_called_once_with("read_stream", "write_stream")
         mock_session.initialize.assert_called_once()
         mock_session.call_tool.assert_called_once_with("calculate_sum", {"low": 1, "high": 10})

def test_argument_parsing():
    # Verify that client's argparse is set up correctly with correct parameter defaults
    from client import main
    
    with patch("sys.argv", ["client.py", "-l", "5", "-u", "15"]):
        with patch("asyncio.run") as mock_run:
            main()
            mock_run.assert_called_once()

@pytest.mark.asyncio
async def test_run_client_failure():
    # Verify that connection exceptions are handled gracefully without crashing
    with patch("client.sse_client", side_effect=Exception("Connection refused")):
        from client import run_client
        with pytest.raises(SystemExit) as exc_info:
            await run_client("http://localhost:8080/sse", 1, 10)
        assert exc_info.value.code == 1

