#!/bin/bash

# Start script for Zenith NPC Generator Service with Dapr
# This script starts the service with Dapr runtime

set -e

echo "🚀 Starting Zenith NPC Generator Service with Dapr..."

# Check if Dapr is installed
if ! command -v dapr &> /dev/null; then
    echo "❌ Dapr CLI is not installed. Please install Dapr first."
    echo "Visit: https://docs.dapr.io/getting-started/install-dapr-cli/"
    exit 1
fi

# Check if environment file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "Please edit .env with your Azure OpenAI credentials before running."
    exit 1
fi

# Default values
APP_ID=${DAPR_APP_ID:-"zenith-npc-generator"}
APP_PORT=${DAPR_APP_PORT:-"50051"}
DAPR_HTTP_PORT=${DAPR_HTTP_PORT:-"3500"}
DAPR_GRPC_PORT=${DAPR_GRPC_PORT:-"50051"}
COMPONENTS_PATH=${DAPR_COMPONENTS_PATH:-"./dapr/components"}

echo "📋 Configuration:"
echo "   App ID: $APP_ID"
echo "   App Port: $APP_PORT"
echo "   Dapr HTTP Port: $DAPR_HTTP_PORT"
echo "   Dapr gRPC Port: $DAPR_GRPC_PORT"
echo "   Components Path: $COMPONENTS_PATH"
echo ""

# Start the application with Dapr
exec dapr run \
    --app-id "$APP_ID" \
    --app-port "$APP_PORT" \
    --dapr-http-port "$DAPR_HTTP_PORT" \
    --dapr-grpc-port "$DAPR_GRPC_PORT" \
    --components-path "$COMPONENTS_PATH" \
    --log-level info \
    -- python dapr_app.py