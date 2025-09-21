# Python Command Terminal

A fully functioning command terminal built in Python that mimics the behavior of a real system terminal. This project supports both CLI and web interfaces, includes system monitoring capabilities, and features AI-driven command processing.

##  Features

### Core Terminal Functionality
- **File Operations**: `ls`, `cd`, `pwd`, `mkdir`, `rm`, `cp`, `mv`, `cat`, `touch`
- **System Information**: `whoami`, `hostname`, `date`, `env`
- **Process Management**: `ps`, `kill`, `jobs`, `bg`, `fg`
- **System Monitoring**: `cpu`, `memory`, `disk` usage information
- **Text Processing**: `grep`, `find`, `sort`, `uniq`, `wc`
- **Archive Operations**: `tar`, `zip`, `unzip`

### Advanced Features
- **Command History**: Track and navigate through previous commands
- **Error Handling**: Comprehensive error handling for invalid commands
- **AI-Driven Commands**: Natural language processing for command interpretation
- **Web Interface**: Browser-based terminal interface
- **System Monitoring**: Real-time CPU, memory, and disk usage

##  Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd python-command-terminal
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the terminal**

   **CLI Mode (default):**
   ```bash
   python main.py
   ```

   **Web Mode:**
   ```bash
   python main.py
   # Or set environment variable:
   # export TERMINAL_INTERFACE=web
   # python main.py
   ```

##  Web Interface

The web interface provides a browser-based terminal experience:

1. **Start the web server:**
   ```bash
   python main.py
   ```

2. **Open your browser:**
   Navigate to `http://localhost:5000`

3. **Use the terminal:**
   - Type commands in the input field
   - Click "Execute" or press Enter
   - View results in real-time

##  Available Commands

### File Operations
- `ls [directory]` - List directory contents
- `cd [directory]` - Change directory
- `pwd` - Print working directory
- `mkdir [directory]` - Create directory
- `rmdir [directory]` - Remove directory
- `rm [file]` - Remove files
- `cp [source] [destination]` - Copy files
- `mv [source] [destination]` - Move/rename files
- `cat [file]` - Display file contents
- `touch [file]` - Create empty file

### System Information
- `whoami` - Display current user
- `hostname` - Display system hostname
- `date` - Display current date and time
- `env` - Display environment variables
- `echo [text]` - Display text

### System Monitoring
- `cpu` - Display CPU information and usage
- `memory` - Display memory usage statistics
- `disk` - Display disk usage information
- `ps` - Display process information

### Utilities
- `clear` - Clear terminal screen
- `history` - Show command history
- `help [command]` - Display help information
- `exit` / `quit` - Exit terminal

##  AI-Driven Commands

The terminal supports natural language command processing:

**Examples:**
- "create a new folder called test" → `mkdir test`
- "show me the current directory" → `pwd`
- "list all files in the current folder" → `ls`
- "show me system processes" → `ps`

##  Project Structure

```
python-command-terminal/
├── main.py                    # Entry point
├── app.py                     # Flask application for deployment
├── requirements.txt           # Python dependencies
├── Procfile                   # Heroku/Render deployment config
├── runtime.txt               # Python runtime specification
├── README.md                 # This file
└── terminal/                 # Core terminal package
    ├── __init__.py
    ├── core.py               # Core terminal functionality
    ├── interface.py          # CLI interface
    ├── web_interface.py      # Advanced web interface (SocketIO)
    ├── simple_web_interface.py # Simple web interface (Flask only)
    ├── system_monitor.py     # System monitoring utilities
    └── ai_processor.py       # AI command processing
```

##  Deployment

### Render Deployment

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service:**
   - Connect your GitHub repository
   - Set Runtime to `Python 3`
   - Set Build Command: `pip install -r requirements.txt`
   - Set Start Command: `python app.py`

3. **Environment Variables:**
   ```
   TERMINAL_INTERFACE=web
   PYTHONPATH=.
   FLASK_ENV=production
   ```

4. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Access your terminal at the provided URL

### Heroku Deployment

1. **Install Heroku CLI** and login

2. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

3. **Deploy:**
   ```bash
   git push heroku main
   ```

##  Configuration

### Environment Variables

- `TERMINAL_INTERFACE`: Set to `web` for web interface, `cli` for CLI interface
- `FLASK_ENV`: Set to `production` for production deployment
- `PORT`: Port number (automatically set by deployment platforms)
- `PYTHONPATH`: Should include current directory

### Customization

You can extend the terminal by:

1. **Adding new commands** in `terminal/core.py`
2. **Modifying the web interface** in `terminal/web_interface.py`
3. **Enhancing AI processing** in `terminal/ai_processor.py`
4. **Adding system monitoring** in `terminal/system_monitor.py`

##  Troubleshooting

### Common Issues

1. **Import Errors:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Port Already in Use:**
   ```bash
   # Kill process using the port
   lsof -ti:5000 | xargs kill -9
   ```

3. **Permission Errors:**
   ```bash
   # Run with appropriate permissions
   sudo python main.py
   ```

4. **Web Interface Not Loading:**
   - Check if Flask is installed
   - Verify port 5000 is available
   - Check firewall settings

### Debug Mode

Enable debug mode for development:
```bash
export FLASK_ENV=development
python main.py
```

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


**Happy coding!** 
