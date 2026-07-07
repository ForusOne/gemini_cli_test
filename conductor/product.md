# Product Guide - MCP Summation Server

## Initial Concept
I want to build a MCP server responding result of calcuation, the calculation should be executed to sum up from lower value to high value. I want to build this on cloud run and deploy it in GCP server.

---

## 1. Product Vision & Overview
The **MCP Summation Server** is a specialized Model Context Protocol (MCP) server designed to offload range-based arithmetic calculations (specifically, summing integers from a specified lower bound to an upper bound) for AI assistants. It will be built using Python, containerized with Docker, and deployed on **Google Cloud Run (GCP)** to ensure high availability, scalability, and easy access over the web (via SSE/HTTP).

## 2. Key Features
- **MCP Tool Exposure**: Implements the Model Context Protocol to expose a tool named `calculate_sum` to compliant LLM/AI clients.
- **Range Summation Logic**: Given a `start` (lower value) and `end` (higher value), calculates the sum of all integers in that range. Correctly handles parameter validation (e.g., ensuring lower value is <= higher value, or adjusting if reversed).
- **HTTP / SSE Transport**: Since it runs on GCP Cloud Run (a serverless container platform), it will use the HTTP/SSE (Server-Sent Events) transport layer for MCP, allowing remote AI clients to connect securely over HTTPS.
- **Cloud Run Deployment**: Optimized Docker configuration, minimal footprint, and structured Deployment instructions/scripts for seamless deployment to Google Cloud Platform.

## 3. Technology & Architecture
- **Language**: Python 3.11+
- **MCP Framework**: `mcp` Python SDK (or `fastmcp` for high-level tool declaration)
- **Web Framework**: FastAPI or Starlette (to handle SSE/HTTP transport for Cloud Run)
- **Deployment**: Google Cloud Run, Artifact Registry, and Docker.
