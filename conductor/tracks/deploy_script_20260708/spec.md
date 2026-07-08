# Specification: Cloud Run Deployment Script

## 1. Overview
The goal of this track is to create a robust and automated shell script (`deploy.sh`) to facilitate building and deploying the MCP Summation Server to Google Cloud Run. The script will streamline the release process by automating GCP project checks, container building on Cloud Build, and deployment to Cloud Run.

---

## 2. Requirements

### 2.1 Functional Requirements
1. **Target Shell:** The deployment script must be written in Bash (`#!/bin/bash`).
2. **Prerequisites & CLI Validation:**
   - The script must check that the `gcloud` CLI is installed and configured.
   - The script must verify that the user is authenticated in an active `gcloud` context.
   - The script must verify that the active GCP Project ID is set, defaulting to `ai-hangsik` but allowing override.
3. **Build & Deploy Process:**
   - Use Google Cloud Build to package the Docker image from local source (utilizing the existing `Dockerfile` and `.dockerignore`).
   - Push the built image to Google Artifact Registry.
   - Deploy the image to Google Cloud Run in the `asia-northeast3` region.
   - Ensure the deployment configuration mirrors the existing secure settings (e.g., service name `mcp-summation-server`, ingress `all`, allow-unauthenticated unless requested otherwise).
4. **Configuration & Parameters:**
   - The script must use clean default variables (e.g., `SERVICE_NAME="mcp-summation-server"`, `REGION="asia-northeast3"`, `PROJECT_ID="ai-hangsik"`) which can be overridden via command-line flags or environment variables.
5. **Robust Error Handling:**
   - The script must exit early with a non-zero exit code if any verification or step fails (`set -e`, `set -o pipefail`).
   - Print clean logs indicating success or failure of each step.

### 2.2 Non-Functional Requirements
1. **Security:** Do not bake or store any passwords, keys, or service account details in the script. Relies entirely on active local CLI context.
2. **Execution Permissions:** The script must be marked executable (`chmod +x`).

---

## 3. Acceptance Criteria
- [ ] Running `./deploy.sh --help` prints a help menu describing variables and options.
- [ ] Running `./deploy.sh` verifies `gcloud` commands and successfully triggers a build and deploy on GCP.
- [ ] Failed commands in the pipeline trigger clean, early exits with informative error logs.
- [ ] Successfully outputs the deployed Cloud Run service URL and health check URL upon completion.
