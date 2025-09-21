# Python Command Terminal

A fully functioning command terminal that mimics the behavior of a real system terminal, built with Python backend. Features file operations, system monitoring, process management, and more.

## Features

- **File Operations**: ls, cd, pwd, mkdir, rm, cp, mv, cat, touch
- **System Monitoring**: cpu, memory, disk, ps (process information)
- **Text Processing**: grep, find, sort, wc
- **Network Utilities**: ping, curl, wget
- **Command History**: Track and recall previous commands
- **Help System**: Comprehensive help for all commands
- **Web Interface**: Modern web-based terminal interface
- **AI-Powered**: Natural language command processing

## Local Development

### Prerequisites
- Python 3.9+
- pip package manager

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally
```bash
# CLI Interface (default for local development)
TERMINAL_INTERFACE=cli python main.py

# Web Interface
TERMINAL_INTERFACE=web python main.py
```

## Deployment to Heroku

### Prerequisites
- Heroku CLI installed
- Git repository

### Deploy Steps
1. **Initialize Git repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```

4. **Deploy to Heroku**:
   ```bash
   git push heroku main
   ```

5. **Open the deployed application**:
   ```bash
   heroku open
   ```

### Environment Variables
- `TERMINAL_INTERFACE`: Set to 'web' for web interface (default)
- `PORT`: Heroku will automatically set this

## Project Structure

```
assignment1/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── Procfile               # Heroku deployment config
├── runtime.txt            # Python version
├── README.md              # This file
└── terminal/
    ├── __init__.py
    ├── core.py            # Core terminal functionality
    ├── interface.py       # CLI interface
    ├── web_interface.py   # Web interface
    ├── system_monitor.py  # System monitoring
    └── ai_processor.py    # AI command processing
```

## Available Commands

### File Operations
- `ls` / `dir` - List directory contents
- `cd <directory>` - Change directory
- `pwd` - Print working directory
- `mkdir <name>` - Create directory
- `rmdir <name>` - Remove directory
- `rm <file>` - Remove files
- `cp <src> <dst>` - Copy files
- `mv <src> <dst>` - Move/rename files
- `cat <file>` - Display file contents
- `touch <file>` - Create empty file

### System Information
- `whoami` - Display current user
- `hostname` - Display system hostname
- `date` - Display current date/time
- `echo <text>` - Display text
- `env` - Display environment variables

### System Monitoring
- `cpu` - Display CPU information
- `memory` - Display memory usage
- `disk` - Display disk usage
- `ps` - Display process information

### Text Processing
- `grep <pattern> <file>` - Search text in files
- `find <path> <pattern>` - Find files and directories
- `sort <file>` - Sort lines in files
- `wc <file>` - Count lines, words, characters

### Utilities
- `clear` - Clear terminal screen
- `history` - Show command history
- `help` - Display help information
- `exit` / `quit` - Exit terminal

## Web Interface

The web interface provides:
- Real-time command execution
- System information display
- Command suggestions and auto-completion
- Modern, responsive design
- SocketIO-based real-time communication

## API Endpoints

- `GET /` - Main web interface
- `GET /api/system/info` - System information
- `GET /api/commands/suggest?q=<query>` - Command suggestions
- SocketIO events: `connect`, `disconnect`, `command`, `get_directory`

## License

This project is created for educational purposes.

## Support

For issues or questions, please refer to the help command within the terminal or check the project documentation.
