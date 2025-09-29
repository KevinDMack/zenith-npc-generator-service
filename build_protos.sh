#!/bin/bash

# Build script for generating protobuf Python files
# Run this after changing .proto files or setting up a new environment

set -e

echo "🔨 Building protobuf files..."

# Check if protoc is available
if ! command -v python -m grpc_tools.protoc &> /dev/null; then
    echo "❌ grpcio-tools not found. Installing..."
    pip install grpcio-tools>=1.48.0
fi

# Generate Python classes from protobuf definitions
echo "📦 Generating Python protobuf classes..."
python -m grpc_tools.protoc \
    --python_out=. \
    --proto_path=protos \
    protos/npc.proto

# Verify generated files
if [ -f "npc_pb2.py" ]; then
    echo "✅ Generated npc_pb2.py"
else
    echo "❌ Failed to generate npc_pb2.py"
    exit 1
fi

# Test import
echo "🧪 Testing protobuf import..."
python -c "from npc_pb2 import NPC; print('✅ Import test passed')"

echo "🎉 Build completed successfully!"
echo ""
echo "Generated files:"
echo "  - npc_pb2.py (Python protobuf classes)"
echo ""
echo "Note: These files are excluded from git (see .gitignore)"
echo "Run this script after cloning or when proto files change."