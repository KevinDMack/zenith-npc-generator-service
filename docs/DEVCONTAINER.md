# Devcontainer Development Guide

## 🏠 Development Container Setup

The Zenith NPC Generator includes a comprehensive development container that provides:
- **Complete Python 3.11 environment** with all dependencies
- **Docker-in-Docker** support for container operations
- **VSCode extensions** automatically installed
- **Zsh with Oh My Zsh** for enhanced terminal experience
- **Pre-commit hooks** for code quality
- **Development tools** (black, flake8, pytest, etc.)

## 🚀 Quick Start

### Option 1: Using VSCode (Recommended)
1. **Install VSCode extensions:**
   - Dev Containers extension
   - Docker extension (if not already installed)

2. **Open in container:**
   - Open the project in VSCode
   - Click "Reopen in Container" when prompted
   - Or: `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"

3. **Wait for setup:**
   - Container builds automatically
   - Post-create script configures environment
   - All dependencies installed

### Option 2: Using Dev Containers CLI
```bash
# Install devcontainer CLI
npm install -g @devcontainers/cli

# Build and start the devcontainer
devcontainer up --workspace-folder .

# Execute commands in the container
devcontainer exec --workspace-folder . zsh
```

## 🎯 Development Environment Features

### **🐍 Python Environment**
- **Python 3.11** with optimized configuration
- **All project dependencies** pre-installed
- **Development tools**: black, flake8, isort, mypy, pytest
- **Interactive tools**: ipython, jupyter
- **Pre-commit hooks** for code quality

### **🐳 Docker Integration**
- **Docker-in-Docker** support
- **Docker Compose** available
- **Full Docker CLI** access
- Build and test containers from within devcontainer

### **🎨 Enhanced Terminal**
- **Zsh with Oh My Zsh** (agnoster theme)
- **Auto-suggestions** and syntax highlighting
- **Custom aliases** for common tasks
- **Service status indicator** in prompt
- **Git integration** with branch display

### **📝 Code Quality Tools**
- **Black** formatter (88 char line length)
- **Flake8** linter with sensible rules
- **isort** import organizer
- **Pre-commit hooks** run automatically
- **MyPy** type checking available

## 🛠️ Built-in Commands & Aliases

Once inside the devcontainer, you have access to these convenient commands:

```bash
# Service management
start    # Start the NPC Generator service (python3 app.py)
test     # Run the test suite (python3 test_service.py)
health   # Check service health (curl health endpoint)

# Docker operations
build    # Build Docker image
clean    # Clean Python cache and Docker resources

# Code quality
format   # Format code with black and isort
lint     # Run flake8 linting

# Standard commands
python3 app.py           # Start service
python3 test_service.py  # Run tests
curl http://localhost:5000/health  # Health check
```

## 📁 Container Structure

```
/workspace/                 # Your project directory (mounted)
├── .devcontainer/         # Container configuration
├── .vscode/              # VSCode settings (preserved)
├── citizens/             # Generated NPCs storage
├── app.py               # Main service
└── ...                  # All your project files

/home/vscode/             # User home directory
├── .oh-my-zsh/          # Zsh configuration
├── .zshrc              # Shell configuration
└── .zsh_welcome        # Welcome message
```

## 🔧 Environment Variables

The devcontainer automatically configures:
```bash
PYTHONPATH=/workspace     # Python path set to workspace
FLASK_ENV=development     # Development mode
FLASK_DEBUG=True         # Debug mode enabled
```

Your `.env` file is automatically created from `.env.example` during setup.

## 🌐 Port Forwarding

- **Port 5000**: NPC Generator Service (automatically forwarded)
- **Port 5432**: PostgreSQL (if enabled with extras profile)
- **Port 6379**: Redis (if enabled with extras profile)

## 🎨 VSCode Integration

### **Automatic Extensions**
- Python support with IntelliSense
- Docker integration
- Code formatting and linting
- JSON and YAML editing
- GitHub Copilot (if available)
- Spell checking

### **Debugging Support**
- **F5**: Debug the main application
- **Breakpoints**: Full debugging support
- **Environment**: .env automatically loaded
- **Terminal**: Integrated zsh terminal

### **Tasks Integration**
All VSCode tasks work seamlessly in the devcontainer:
- 🚀 Run Application (Local)
- 🐳 Docker operations
- 🧪 Testing tasks
- 🔧 Utility tasks

## 🚀 Advanced Usage

### **Multiple Services**
Enable additional services with profiles:
```bash
# Start with Redis and PostgreSQL
docker-compose --profile extras up devcontainer

# Or rebuild devcontainer with extras
devcontainer up --workspace-folder . --additional-features redis postgres
```

### **Custom Configuration**
Modify `.devcontainer/devcontainer.json` to:
- Add more VSCode extensions
- Install additional tools
- Configure different Python version
- Add more forwarded ports

### **Persistent Data**
- **Workspace**: Fully persistent (mounted from host)
- **Extensions**: Persist across container rebuilds
- **Shell history**: Maintained in container
- **Generated NPCs**: Stored in mounted `citizens/` directory

## 🔍 Troubleshooting

### **Container Won't Start**
```bash
# Rebuild the container
Dev Containers: Rebuild Container (in VSCode)
# Or with CLI
devcontainer up --workspace-folder . --build
```

### **Missing Dependencies**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or rebuild container
Dev Containers: Rebuild Container
```

### **Docker Issues**
```bash
# Check Docker access
docker --version
docker ps

# Fix Docker socket permissions (if needed)
sudo chmod 666 /var/run/docker.sock
```

### **Port Conflicts**
- Change port forwarding in `devcontainer.json`
- Or use different ports in docker-compose.yml

## 🎉 Benefits

✅ **Consistent Environment** - Same setup for all developers
✅ **Zero Configuration** - Everything works out of the box  
✅ **Isolated Development** - No conflicts with host system
✅ **Full Feature Parity** - All tools available as in local dev
✅ **Docker Integration** - Build and test containers seamlessly
✅ **Version Control Ready** - Configuration tracked in git
✅ **Cross Platform** - Works on Windows, macOS, Linux

The devcontainer provides a professional-grade development environment that's ready to use in seconds! 🎭✨