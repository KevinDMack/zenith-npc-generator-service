# Zenith NPC Generator Service

A Python microservice that leverages Azure OpenAI to generate unique NPCs (Non-Player Characters) for fantasy and sci-fi settings. Each generated NPC includes detailed attributes and is saved as JSON files in a local "citizens" directory.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Azure OpenAI service with a deployed model (GPT-3.5-turbo or GPT-4 recommended)
- Azure OpenAI API key and endpoint

### Getting Started in 5 Steps

1. **Set up your Azure OpenAI credentials:**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure OpenAI details
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the service:**
   ```bash
   python3 app.py
   ```

4. **Test the service:**
   ```bash
   ./test_service.py
   # Or manually: curl http://localhost:5000/health
   ```

5. **Generate your first NPC:**
   ```bash
   curl -X POST http://localhost:5000/generate-npc \
     -H "Content-Type: application/json" \
     -d '{}'
   ```

Your NPCs will be saved as JSON files in the `citizens/` directory! 🎭

## 🐳 Docker Deployment

### Option 1: Docker Compose (Recommended)
```bash
# Make sure your .env file is configured
cp .env.example .env
# Edit .env with your Azure OpenAI credentials

# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop the service
docker-compose down
```

### Option 2: Manual Docker Build and Run
```bash
# Step 1: Build the Docker image
docker build -t zenith-npc-generator:latest .

# Step 2: Run the container
docker run -d \
  --name npc-generator \
  -p 5000:5000 \
  --env-file .env \
  -v $(pwd)/citizens:/app/citizens \
  --restart unless-stopped \
  zenith-npc-generator:latest

# Step 3: Check if container is running
docker ps

# Step 4: View container logs
docker logs npc-generator

# Step 5: Test the service
curl http://localhost:5000/health

# Step 6: Stop and remove container (when done)
docker stop npc-generator
docker rm npc-generator
```

### Option 3: Quick Test Run (Temporary Container)
```bash
# Build the image
docker build -t zenith-npc-generator:latest .

# Run temporarily (container auto-removes when stopped)
docker run --rm -it \
  -p 5000:5000 \
  --env-file .env \
  -v $(pwd)/citizens:/app/citizens \
  zenith-npc-generator:latest

# Press Ctrl+C to stop and auto-remove container
```

### Option 3: Pre-built Image (coming soon)
```bash
# Pull and run from Docker Hub (when available)
docker pull zenith/npc-generator:latest
docker run -p 5000:5000 --env-file .env zenith/npc-generator:latest
```

### Docker Benefits
- ✅ **Isolated Environment**: No dependency conflicts
- ✅ **Easy Deployment**: One command to run anywhere
- ✅ **Persistent Storage**: Citizens directory is mounted as volume
- ✅ **Auto-restart**: Container restarts on failure
- ✅ **Production Ready**: Optimized for production workloads

📖 **For detailed Docker deployment instructions, see [DOCKER.md](DOCKER.md)**

## 💻 VSCode Integration

This project includes comprehensive VSCode tasks for streamlined development:

### 🎯 Quick Access via Command Palette
Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) and type "Tasks: Run Task" to see all available tasks:

**Local Development:**
- `🐍 Install Dependencies` - Install Python packages
- `🚀 Run Application (Local)` - Start the service locally
- `🔧 Check Environment` - Verify environment variables
- `🧪 Test Service` - Run comprehensive tests
- `📋 Health Check` - Quick service health verification

**Docker Operations:**
- `🐳 Docker: Build Image` - Build the Docker image
- `🐳 Docker: Run Container` - Run container in background
- `🐳 Docker: Run Container (Interactive)` - Run container interactively
- `🐳 Docker Compose: Up` - Start with Docker Compose
- `🐳 Docker Compose: Up (Background)` - Start in background
- `🐳 Docker: View Logs` - Monitor container logs

**Utility Tasks:**
- `📄 Setup Environment File` - Copy .env.example to .env
- `🧹 Clean Up Docker` - Remove unused Docker resources
- `📁 Open Citizens Directory` - View generated NPCs

### 🐛 Debugging Support
- Press `F5` to debug the application with full breakpoint support
- Environment variables automatically loaded from `.env`
- Integrated terminal for easy testing

### 🔧 Recommended Extensions
The project includes extension recommendations for optimal development experience:
- Python support with linting and formatting
- Docker integration
- YAML and JSON editing
- Code spell checking

📖 **For detailed VSCode setup and usage, see [VSCODE.md](VSCODE.md)**

## 🏠 Development Container

This project includes a complete development container for consistent development environments:

### 🚀 Get Started with Dev Containers
1. **Install VSCode** with the "Dev Containers" extension
2. **Open project** and click "Reopen in Container" when prompted
3. **Wait for setup** - everything installs automatically
4. **Start developing** - all tools and dependencies ready!

### ✨ What's Included
- **Python 3.11** with all dependencies pre-installed
- **Docker-in-Docker** for building and testing containers
- **Zsh + Oh My Zsh** with custom aliases and themes
- **All VSCode extensions** automatically installed
- **Code quality tools** (black, flake8, pre-commit hooks)
- **Service status indicator** in terminal prompt

### 🛠️ Built-in Commands
```bash
start    # Start the NPC service
test     # Run test suite  
health   # Check service health
build    # Build Docker image
format   # Format code
lint     # Lint code
clean    # Clean up resources
```

📖 **For complete devcontainer documentation, see [DEVCONTAINER.md](DEVCONTAINER.md)**

## Features

- Generate single or multiple NPCs using Azure OpenAI
- Customizable generation parameters (species, district, age range)
- Automatic JSON file storage in the "citizens" directory
- RESTful API endpoints
- Comprehensive logging and error handling
- Health check and storage statistics endpoints

## NPC Attributes

Each generated NPC includes the following attributes:
- **Name**: Character's full name
- **Age**: Numeric age
- **Species**: Species/Race (e.g., Human, Elf, Orc, etc.)
- **PhysicalDescription**: Detailed physical appearance
- **PersonalityDescription**: Personality traits and characteristics
- **ResidentDistrict**: The district or area where they live

## Setup

### Prerequisites

- Python 3.8+
- Azure OpenAI service with a deployed model
- pip (Python package manager)

### Installation

1. **Clone or create the project directory:**
   ```bash
   mkdir zenith-npc-generator-service
   cd zenith-npc-generator-service
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your Azure OpenAI credentials:
   ```
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
   ```

4. **Run the service:**
   ```bash
   python app.py
   ```

The service will start on `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```
Returns service health status.

### Generate Single NPC
```
POST /generate-npc
Content-Type: application/json

{
  "species_preference": "Elf",           // Optional
  "district_preference": "Mystic Gardens", // Optional
  "age_range": "25-35"                   // Optional
}
```

### Generate Multiple NPCs
```
POST /generate-npcs
Content-Type: application/json

{
  "count": 5,                            // Number of NPCs to generate
  "species_preference": "Human",         // Optional
  "district_preference": "Tech District", // Optional
  "age_range": "20-40"                   // Optional
}
```

### Get All Stored NPCs
```
GET /npcs
```
Returns all NPCs stored in the citizens directory.

### Get Storage Statistics
```
GET /storage-stats
```
Returns statistics about stored NPC files.

## Example Usage

### Generate a Single NPC
```bash
curl -X POST http://localhost:5000/generate-npc \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Generate Multiple NPCs with Preferences
```bash
curl -X POST http://localhost:5000/generate-npcs \
  -H "Content-Type: application/json" \
  -d '{
    "count": 3,
    "species_preference": "Dwarf",
    "district_preference": "Merchant Quarter"
  }'
```

## File Storage

Generated NPCs are automatically saved to the `citizens/` directory in two formats:

1. **Individual files**: `YYYYMMDD_HHMMSS_NPC_Name.json`
2. **Collection files**: `npc_collection_YYYYMMDD_HHMMSS.json` (when generating multiple NPCs)

### Example NPC JSON Output
```json
{
  "Name": "Eldara Moonwhisper",
  "Age": 127,
  "Species": "Elf",
  "PhysicalDescription": "Tall and graceful with silver hair that shimmers like moonlight. Her violet eyes hold ancient wisdom, and intricate tattoos of celestial patterns adorn her arms.",
  "PersonalityDescription": "Quiet and contemplative, Eldara speaks in riddles and has an uncanny ability to predict weather patterns. She collects rare books and has a deep fear of iron.",
  "ResidentDistrict": "Mystic Gardens"
}
```

## Project Structure

```
zenith-npc-generator-service/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── citizens/                       # Directory for generated NPC files
├── models/
│   ├── __init__.py
│   └── npc.py                      # NPC data models
└── services/
    ├── __init__.py
    ├── azure_openai_service.py     # Azure OpenAI integration
    └── npc_storage_service.py      # File storage service
```

## Configuration

### Environment Variables

- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI resource endpoint
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_API_VERSION`: API version (default: 2024-02-15-preview)
- `AZURE_OPENAI_DEPLOYMENT_NAME`: Name of your deployed model
- `FLASK_ENV`: Flask environment (development/production)
- `FLASK_DEBUG`: Enable Flask debug mode (True/False)

## Error Handling

The service includes comprehensive error handling:
- Invalid JSON responses from OpenAI are caught and logged
- Missing environment variables are validated on startup
- File storage errors are handled gracefully
- All endpoints return appropriate HTTP status codes

## Logging

The service logs important events including:
- NPC generation success/failure
- File storage operations
- API request errors
- Service startup information

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

### Testing the Service
Use the provided curl examples or any HTTP client like Postman to test the endpoints.

## License

This project is open source and available under the MIT License.