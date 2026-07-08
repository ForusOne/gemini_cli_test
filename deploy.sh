#!/bin/bash
set -e
set -o pipefail

# Default variables
SERVICE_NAME="mcp-summation-server"
REGION="asia-northeast3"
PROJECT_ID="ai-hangsik"

# Print help / usage
show_help() {
  echo "Usage: ./deploy.sh [OPTIONS]"
  echo ""
  echo "Deploys the MCP Summation Server to Google Cloud Run."
  echo ""
  echo "Options:"
  echo "  -h, --help            Show this help message and exit"
  echo "  -s, --service NAME    Cloud Run service name (default: mcp-summation-server)"
  echo "  -r, --region REGION   GCP region (default: asia-northeast3)"
  echo "  -p, --project ID      GCP project ID (default: ai-hangsik)"
  echo ""
}

# Parse command line options
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      show_help
      exit 0
      ;;
    -s|--service)
      SERVICE_NAME="$2"
      shift 2
      ;;
    -r|--region)
      REGION="$2"
      shift 2
      ;;
    -p|--project)
      PROJECT_ID="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

echo "=== Pre-deployment Verification ==="

# 1. Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
  echo "Error: 'gcloud' CLI is not installed." >&2
  echo "Please install the Google Cloud SDK and try again." >&2
  exit 1
fi
echo "✓ 'gcloud' CLI is installed."

# 2. Check if user is authenticated
ACTIVE_ACCOUNT=$(gcloud config get-value account 2>/dev/null)
if [[ -z "$ACTIVE_ACCOUNT" ]]; then
  echo "Error: No active Google Cloud account found." >&2
  echo "Please authenticate using: gcloud auth login" >&2
  exit 1
fi
echo "✓ Authenticated as: $ACTIVE_ACCOUNT"

# 3. Validate active project configuration
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
if [[ -n "$PROJECT_ID" ]]; then
  echo "Configuring GCP Project to: $PROJECT_ID"
  gcloud config set project "$PROJECT_ID"
elif [[ -n "$CURRENT_PROJECT" ]]; then
  PROJECT_ID="$CURRENT_PROJECT"
  echo "✓ Using active GCP Project: $PROJECT_ID"
else
  echo "Error: No active GCP project is set, and no default was specified." >&2
  exit 1
fi

echo "✓ GCP environment verified successfully."

echo ""
echo "=== Step 1: Submit Build to Google Cloud Build ==="
IMAGE_TAG="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"
echo "Submitting build to Cloud Build: ${IMAGE_TAG}"
gcloud builds submit --tag "${IMAGE_TAG}" .

echo ""
echo "=== Step 2: Deploy to Google Cloud Run ==="
echo "Deploying to service: ${SERVICE_NAME} in region: ${REGION}"
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE_TAG}" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated

# Retrieve and print the service URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --region "${REGION}" --format="value(status.url)" 2>/dev/null)

echo ""
echo "=================================================="
echo "         DEPLOYMENT COMPLETED SUCCESSFULLY"
echo "=================================================="
echo "  Service Name: ${SERVICE_NAME}"
echo "  Region:       ${REGION}"
echo "  Project ID:   ${PROJECT_ID}"
echo "  Service URL:  ${SERVICE_URL}"
echo "  Health Check: ${SERVICE_URL}/health"
echo "=================================================="
