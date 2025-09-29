FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Generate protobuf files
RUN python -m grpc_tools.protoc --python_out=. --proto_path=protos protos/npc.proto

# Create citizens directory and set permissions
RUN mkdir -p citizens && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port (both HTTP and Dapr app port)
EXPOSE 5000 50051

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check (supports both HTTP and Dapr modes)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || curl -f http://localhost:3500/v1.0/invoke/zenith-npc-generator/method/health || exit 1

# Run the application
CMD ["python", "app.py"]