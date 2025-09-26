# Docker Deployment Guide for Zenith NPC Generator

## 🐳 Docker Deployment Options

### Quick Start with Docker Compose (Recommended)

1. **Prepare your environment:**
   ```bash
   # Clone or navigate to the project directory
   cd zenith-npc-generator-service
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

2. **Deploy with one command:**
   ```bash
   docker-compose up --build -d
   ```

3. **Verify deployment:**
   ```bash
   # Check container status
   docker-compose ps
   
   # Check health
   curl http://localhost:5000/health
   
   # View logs
   docker-compose logs -f
   ```

### Manual Docker Build

```bash
# Build the image
docker build -t zenith-npc-generator:latest .

# Run the container
docker run -d \
  --name npc-generator \
  -p 5000:5000 \
  --env-file .env \
  -v $(pwd)/citizens:/app/citizens \
  --restart unless-stopped \
  zenith-npc-generator:latest
```

### Production Deployment

For production environments, consider these additional configurations:

#### Docker Compose Override for Production
Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  npc-generator:
    restart: always
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "3"
```

Deploy with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

#### With Reverse Proxy (Nginx)
Add to your `docker-compose.yml`:
```yaml
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - npc-generator
    networks:
      - npc-network
```

### Environment Variables

Required for Docker deployment:
```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
```

### Docker Management Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f npc-generator

# Update and restart
docker-compose pull
docker-compose up -d --force-recreate

# Scale the service (if needed)
docker-compose up -d --scale npc-generator=3

# Clean up
docker-compose down --rmi all --volumes --remove-orphans
```

### Monitoring and Health Checks

The container includes built-in health checks:
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' zenith-npc-generator

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' zenith-npc-generator
```

### Volume Persistence

NPCs are stored in a mounted volume:
- **Host path**: `./citizens/`
- **Container path**: `/app/citizens/`
- **Backup**: `tar -czf npc-backup.tar.gz citizens/`

### Troubleshooting

**Container won't start:**
```bash
# Check logs
docker-compose logs npc-generator

# Check environment variables
docker-compose exec npc-generator env | grep AZURE
```

**Health check failing:**
```bash
# Manual health check
docker-compose exec npc-generator curl -f http://localhost:5000/health

# Check if service is listening
docker-compose exec npc-generator netstat -tlnp | grep 5000
```

**Permission issues:**
```bash
# Fix volume permissions
sudo chown -R 1000:1000 ./citizens/
```

### Security Considerations

- Container runs as non-root user
- Environment variables are isolated
- Network is isolated by default
- Regularly update the base image
- Use secrets management in production

### Multi-stage Build (Advanced)

For smaller production images, consider this multi-stage Dockerfile:
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
RUN mkdir -p citizens
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```