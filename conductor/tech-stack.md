# Technology Stack - MCP Summation Server

This document outlines the languages, frameworks, libraries, and infrastructure used in the MCP Summation Server project.

---

## 1. Core Language & Runtime
- **Language**: Python 3.11+
- **Rationale**: Python is the primary development language of the project (`count.py`), offering excellent ecosystem support for the Model Context Protocol and rapid development of lightweight APIs.

## 2. Frameworks & Protocols
- **Model Context Protocol (MCP)**: Custom MCP server exposing computational tools.
- **Transport Protocol**: **Streamable HTTP (SSE - Server-Sent Events)**
  - *Rationale*: Allows standard stream-based, asynchronous, and stateful communication over HTTP/HTTPS, enabling remote clients (like Cursor, Claude Desktop, or custom clients) to connect securely and dynamically to the server hosted on Cloud Run.
- **Web Framework**: FastAPI / ASGI (via `uvicorn`)
  - *Rationale*: Modern, high-performance web framework for Python, ideally suited for handling asynchronous connections and SSE streams natively.

## 3. Local Client Application
- **Local PC Client**: A lightweight local CLI utility (`client.py`) written in Python using `httpx` or `mcp` client library.
- **Rationale**: Allows you to easily test, query, and verify the summation results from your local PC by sending the start and end range directly to the server.

## 4. Tooling & Infrastructure
- **Containerization**: Docker
  - *Rationale*: Provides a reproducible runtime environment and forms the deployment unit for Google Cloud Run.
- **Hosting Platform**: Google Cloud Run (GCP)
  - *Rationale*: Fully managed, serverless platform that automatically scales containers up and down, supports HTTP/HTTPS, and works seamlessly with SSE streams when configured with appropriate timeout settings.
- **Container Registry**: GCP Artifact Registry

## 5. Testing & Quality Assurance
- **Testing**: `pytest`
- **Linting & Formatting**: `black`, `flake8` or `ruff`
