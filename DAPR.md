# Dapr Integration for Zenith NPC Generator

This directory contains the configuration and implementation for running the Zenith NPC Generator Service with Dapr (Distributed Application Runtime) for cloud-native deployments, particularly on Kubernetes.

## 🎯 Migration Overview

The service has been migrated from HTTP-based endpoints to Dapr topic-based communication:

- **Before**: HTTP POST to `/generate-npc` and `/generate-npcs` endpoints
- **After**: Publish messages to `npc-generation-request` topic, receive responses on `npc-generation-response` topic
- **Models**: Migrated from Pydantic to Protocol Buffers for better cross-platform compatibility

## 🏗️ Architecture

```
┌─────────────────┐    Topic     ┌─────────────────┐    Topic     ┌─────────────────┐
│   Client App    │────────────→ │  Dapr PubSub    │────────────→ │  NPC Generator  │
│                 │              │  (Redis/Cloud)  │              │    Service      │
└─────────────────┘              └─────────────────┘              └─────────────────┘
        ↑                                                                   │
        │                        ┌─────────────────┐                       │
        └────────────────────────│ Response Topic  │←──────────────────────┘
                                 │   (per request) │
                                 └─────────────────┘
```

## 📦 Files Overview

- **`dapr_app.py`**: Main Dapr-enabled application using Dapr Python SDK
- **`npc_pb2.py`**: Generated Protocol Buffer classes (auto-generated)
- **`protos/npc.proto`**: Protocol Buffer definitions for NPC models
- **`dapr/components/pubsub.yaml`**: Dapr PubSub component configuration
- **`services/npc_storage_service_pb.py`**: Storage service supporting both Pydantic and Protobuf models
- **`start_dapr.sh`**: Startup script for running with Dapr runtime
- **`dapr_client_example.py`**: Example client showing how to interact with the service
- **`test_both_services.py`**: Test suite supporting both HTTP and Dapr modes

## 🚀 Quick Start

### Prerequisites

1. **Install Dapr CLI**:
   ```bash
   # Linux/macOS
   wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
   
   # Or via package managers
   # brew install dapr/tap/dapr-cli
   # winget install dapr.cli
   ```

2. **Initialize Dapr**:
   ```bash
   dapr init
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Service

1. **Start with Dapr**:
   ```bash
   ./start_dapr.sh
   ```

2. **Test the service**:
   ```bash
   python test_both_services.py
   ```

## 🔧 Configuration

### Environment Variables

The same environment variables as the HTTP version:
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_DEPLOYMENT_NAME`
- `MONGODB_CONNECTION_STRING`

### Dapr Configuration

- **App ID**: `zenith-npc-generator`
- **Ports**: 
  - App Port: 50051 (gRPC)
  - Dapr HTTP Port: 3500
  - Dapr gRPC Port: 50001
- **PubSub Component**: Redis (configurable in `dapr/components/pubsub.yaml`)

## 📡 Topic Communication

### Request Topic: `npc-generation-request`

Send a `GenerateNPCTopicMessage` with:
```protobuf
message GenerateNPCTopicMessage {
    string request_id = 1;                  // Unique request identifier
    NPCGenerationRequest request = 2;       // The generation parameters
    string response_topic = 3;              // Where to send the response
}
```

### Response Topic: Dynamic per request

Receive `NPCGenerationTopicResponse` with:
```protobuf
message NPCGenerationTopicResponse {
    string request_id = 1;                  // Matching request identifier
    NPCGenerationResponse response = 2;     // The generated NPCs and metadata
}
```

## 🧪 Testing

### Test Both Services
```bash
python test_both_services.py
```

### Test Dapr-specific Features
```bash
# Health check via service invocation
curl -X POST http://localhost:3500/v1.0/invoke/zenith-npc-generator/method/health

# Publish to topic (requires proper protobuf encoding)
python dapr_client_example.py
```

## 🐳 Docker & Kubernetes

### Docker Build
```bash
# Build image
docker build -t zenith-npc-generator:dapr .

# Run with Dapr sidecar (requires Dapr setup)
docker run --network dapr zenith-npc-generator:dapr
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: zenith-npc-generator
  labels:
    app: zenith-npc-generator
spec:
  replicas: 1
  selector:
    matchLabels:
      app: zenith-npc-generator
  template:
    metadata:
      labels:
        app: zenith-npc-generator
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "zenith-npc-generator"
        dapr.io/app-port: "50051"
    spec:
      containers:
      - name: zenith-npc-generator
        image: zenith-npc-generator:dapr
        ports:
        - containerPort: 50051
        env:
        - name: AZURE_OPENAI_ENDPOINT
          valueFrom:
            secretKeyRef:
              name: openai-secrets
              key: endpoint
        # ... other environment variables
```

## 🔄 Migration Path

The service supports both HTTP and Dapr modes during transition:

1. **Phase 1**: Deploy both HTTP (`app.py`) and Dapr (`dapr_app.py`) versions
2. **Phase 2**: Migrate clients to use Dapr topics
3. **Phase 3**: Decommission HTTP endpoints

## 🤝 Client Libraries

Example client usage:
```python
from dapr.clients import DaprClient
from npc_pb2 import NPCGenerationRequest, GenerateNPCTopicMessage

# Create request
request = NPCGenerationRequest()
request.count = 1
request.species_preference = "Elf"

# Send via Dapr
with DaprClient() as client:
    client.publish_event(
        pubsub_name='pubsub',
        topic_name='npc-generation-request',
        data=message.SerializeToString()
    )
```

## 📋 Benefits of Dapr Migration

- **Cloud Native**: Better integration with Kubernetes and cloud platforms
- **Resilience**: Built-in retries, circuit breakers, and observability
- **Scalability**: Automatic scaling based on topic backlog
- **Decoupling**: Services communicate via topics, not direct HTTP calls
- **Multi-language**: Protocol Buffers enable polyglot implementations
- **Observability**: Built-in metrics, tracing, and logging via Dapr

## 🔍 Troubleshooting

### Check Dapr Status
```bash
dapr list
```

### View Dapr Logs
```bash
# Application logs
dapr logs --app-id zenith-npc-generator

# Dapr sidecar logs
docker logs dapr_dapr_1
```

### Test Topic Connectivity
```bash
# Publish test message
dapr publish --publish-app-id zenith-npc-generator --pubsub pubsub --topic npc-generation-request --data '{}'
```