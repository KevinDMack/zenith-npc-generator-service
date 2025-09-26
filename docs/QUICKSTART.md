# Quick Start Guide

## 🚀 Getting Started with Zenith NPC Generator Service

### 1. Set up Azure OpenAI

Before running the service, you need:
- An Azure OpenAI resource
- A deployed model (GPT-3.5-turbo or GPT-4)
- API key and endpoint

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Azure OpenAI credentials
nano .env
```

Required environment variables:
```
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Service

```bash
python3 app.py
```

The service will start on http://localhost:5000

### 5. Test the Service

```bash
# Test with the included test script
./test_service.py

# Or manually test the health endpoint
curl http://localhost:5000/health
```

### 6. Generate Your First NPC

```bash
# Generate a single NPC
curl -X POST http://localhost:5000/generate-npc \
  -H "Content-Type: application/json" \
  -d '{}'

# Generate multiple NPCs with preferences
curl -X POST http://localhost:5000/generate-npcs \
  -H "Content-Type: application/json" \
  -d '{
    "count": 3,
    "species_preference": "Elf",
    "district_preference": "Mystic Gardens"
  }'
```

### 7. Check Generated Files

Your NPCs will be saved as JSON files in the `citizens/` directory:
```bash
ls -la citizens/
cat citizens/20241126_*.json
```

## Docker Deployment (Optional)

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Troubleshooting

- **Service won't start**: Check that all environment variables are set correctly in `.env`
- **No NPCs generated**: Verify your Azure OpenAI deployment is active and accessible
- **JSON parsing errors**: The service will retry failed generations automatically

## API Endpoints Summary

- `GET /health` - Health check
- `POST /generate-npc` - Generate single NPC
- `POST /generate-npcs` - Generate multiple NPCs
- `GET /npcs` - Get all stored NPCs
- `GET /storage-stats` - Storage statistics

Ready to generate some amazing NPCs! 🎭