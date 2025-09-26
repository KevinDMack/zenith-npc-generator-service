# VSCode Development Guide

## 🚀 Quick Start with VSCode

### First Time Setup
1. **Open the project in VSCode:**
   ```bash
   code .
   ```

2. **Install recommended extensions** when prompted (or manually via Extensions tab)

3. **Setup environment:**
   - Use task: `📄 Setup Environment File` (Ctrl+Shift+P → "Tasks: Run Task")
   - Edit `.env` with your Azure OpenAI credentials

4. **Install dependencies:**
   - Use task: `🐍 Install Dependencies`

### 🎯 Available Tasks (Ctrl+Shift+P → "Tasks: Run Task")

#### Local Development Workflow
```
📄 Setup Environment File    → 🐍 Install Dependencies → 🔧 Check Environment → 🚀 Run Application (Local)
                                                                              ↓
                                                                         🧪 Test Service
```

#### Docker Development Workflow
```
🐳 Docker: Build Image → 🐳 Docker: Run Container → 📋 Health Check → 🐳 Docker: View Logs
                                    ↓
                              🐳 Docker: Stop Container → 🐳 Docker: Remove Container
```

#### Docker Compose Workflow (Easiest)
```
🐳 Docker Compose: Up → 📋 Health Check → 🐳 Docker Compose: Logs → 🐳 Docker Compose: Down
```

### 🐛 Debugging

#### Debug Local Application
1. Set breakpoints in your code
2. Press `F5` or select "🐍 Debug NPC Generator" from the debug panel
3. Application runs with full debugging support

#### Debug Tests
1. Select "🧪 Debug Test Service" from the debug panel
2. Step through test execution

### 💡 Pro Tips

#### Keyboard Shortcuts
- `Ctrl+Shift+P` - Command Palette (access all tasks)
- `F5` - Start debugging
- `Ctrl+C` - Stop running tasks
- `Ctrl+`` - Toggle integrated terminal

#### Task Groups
- **Build tasks**: Setup, install, build, run
- **Test tasks**: Health checks, testing, logs, monitoring

#### Quick Actions
- **Start developing locally**: 
  1. `📄 Setup Environment File`
  2. `🐍 Install Dependencies` 
  3. `🚀 Run Application (Local)`

- **Deploy with Docker**:
  1. `🐳 Docker Compose: Up (Background)`
  2. `📋 Health Check`

- **View generated NPCs**:
  1. `📁 Open Citizens Directory`

### 🔧 Workspace Features

#### Automatic Environment Loading
- `.env` file automatically loaded for debugging
- PYTHONPATH set to workspace folder
- Virtual environment activation support

#### File Associations
- `.env` files syntax highlighted
- Docker files properly recognized
- YAML files for docker-compose

#### Code Quality
- Python linting enabled (flake8)
- Code formatting (black)
- Spell checking
- Auto-exclusion of cache files

### 📝 Development Workflow Examples

#### Feature Development
1. `🚀 Run Application (Local)` - Start service
2. Make code changes
3. `📋 Health Check` - Verify service
4. `🧪 Test Service` - Run tests
5. Debug with `F5` if issues found

#### Production Testing
1. `🐳 Docker: Build Image` - Build production image
2. `🐳 Docker: Run Container` - Test container
3. `🐳 Docker: View Logs` - Check for issues
4. `🧪 Test Service` - Validate functionality

#### Clean Development
1. `🧹 Clean Up Docker` - Remove unused resources
2. `🐳 Docker: Remove Container` - Clean containers
3. Fresh start with `🚀 Run Application (Local)`

The VSCode integration makes development seamless with one-click operations for all common tasks! 🎉