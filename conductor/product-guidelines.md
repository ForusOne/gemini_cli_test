# Product Guidelines - MCP Summation Server

This document outlines the design, security, and operational guidelines for developing and maintaining the MCP Summation Server.

---

## 1. Design & Protocol Guidelines

### MCP Conformity
- **Standard Protocol Compliance**: Follow the Model Context Protocol (MCP) spec strictly. All exposed tools must return results in the standard JSON format expected by MCP clients.
- **Descriptive Schemas**: Every tool must have a clear description, and parameters must have detailed descriptions and clear types (e.g., `low` and `high` as integers) to help LLMs understand how to use them.

### Input Validation & Range Safety
- **Robust Input Verification**: Ensure that the inputs are valid integers.
- **Safe Execution Limits**: To prevent denial of service (DoS) or memory exhaustion on serverless containers, enforce a maximum limit on the range (e.g., maximum difference of 10,000,000). If the range is too large, use the analytical formula `sum = (high - low + 1) * (low + high) / 2` instead of looping to perform $O(1)$ calculations! This is highly efficient and safe.
- **Reversed Range Handling**: If `low` is greater than `high`, automatically swap them or calculate the sum correctly without throwing an error, but log a warning.

---

## 2. API & Transport Guidelines

### SSE & HTTP Transport
- **FastAPI / Starlette Implementation**: Use a robust, asynchronous ASGI server to handle incoming connections.
- **Connection Lifecycle**: Implement proper keep-alive mechanisms for Server-Sent Events (SSE) to prevent GCP Cloud Run from prematurely terminating connections.
- **Graceful Shutdown**: Handle SIGTERM signals gracefully, completing any active summation requests before terminating.

---

## 3. GCP Cloud Run & Container Guidelines

### Security & Non-Root Execution
- **Run as Non-Root**: The Dockerfile must create and run as a non-privileged user (e.g., `appuser`) rather than `root`.
- **Minimal Base Image**: Use `python:3.11-slim` or similar minimal official images to reduce container size and vulnerabilities.

### Observability & Logging
- **Structured JSON Logging**: Format logs as structured JSON to stdout/stderr. This ensures that GCP Cloud Logging (Stackdriver) parses severities (INFO, WARNING, ERROR) and payloads correctly.
- **No Sensitive Info**: Never log credentials, API keys, or personally identifiable information (PII).

### Performance & Scaling
- **Stateless Design**: Ensure the server remains completely stateless so Cloud Run can scale down to 0 or scale up dynamically based on load.
- **Container Health Check**: Expose a `/health` or `/ready` endpoint to allow Cloud Run or other GCP services to verify service availability.
