"""
Web interface for the terminal application.
Provides a web-based terminal interface using Flask.
"""

import os
import sys
import json
from typing import Dict, Any
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from .core import TerminalCore
from .system_monitor import SystemMonitor
from .ai_processor import AICommandProcessor


class WebTerminalInterface:
    """
    Web-based terminal interface using Flask and SocketIO.
    """

    def __init__(self, terminal_core: TerminalCore, system_monitor: SystemMonitor,
                 ai_processor: AICommandProcessor):
        self.terminal_core = terminal_core
        self.system_monitor = system_monitor
        self.ai_processor = ai_processor
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.setup_routes()

    def setup_routes(self):
        """Set up Flask routes and SocketIO handlers."""

        @self.app.route('/')
        def index():
            """Serve the main web interface."""
            return render_template('terminal.html')

        @self.app.route('/api/system/info')
        def get_system_info():
            """Get system information via REST API."""
            try:
                info = self.system_monitor.get_detailed_system_info()
                return jsonify(info)
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/commands/suggest')
        def suggest_commands():
            """Get command suggestions via REST API."""
            try:
                query = request.args.get('q', '')
                if query:
                    result = self.ai_processor.process_natural_language(query)
                    return jsonify(result)
                return jsonify({'suggestions': list(self.terminal_core.supported_commands.keys())})
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection."""
            print("Client connected")
            emit('status', {'message': 'Connected to terminal server'})

        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection."""
            print("Client disconnected")

        @self.socketio.on('command')
        def handle_command(data):
            """Handle command execution from client."""
            try:
                command = data.get('command', '').strip()
                if not command:
                    emit('output', {'output': '', 'error': 'Empty command'})
                    return

                # Execute command
                output, exit_code, error = self.terminal_core.execute_command(command)

                # Send result back to client
                response = {
                    'command': command,
                    'output': output,
                    'exit_code': exit_code,
                    'error': error,
                    'directory': self.terminal_core.current_directory
                }

                emit('output', response)

            except Exception as e:
                emit('output', {
                    'command': data.get('command', ''),
                    'output': '',
                    'exit_code': 1,
                    'error': str(e),
                    'directory': self.terminal_core.current_directory
                })

        @self.socketio.on('get_directory')
        def handle_get_directory():
            """Handle request for current directory contents."""
            try:
                # Get directory listing
                items = []
                try:
                    for item in os.listdir(self.terminal_core.current_directory):
                        item_path = os.path.join(self.terminal_core.current_directory, item)
                        try:
                            stat_info = os.stat(item_path)
                            items.append({
                                'name': item,
                                'type': 'directory' if os.path.isdir(item_path) else 'file',
                                'size': stat_info.st_size,
                                'modified': stat_info.st_mtime
                            })
                        except:
                            items.append({
                                'name': item,
                                'type': 'unknown',
                                'size': 0,
                                'modified': 0
                            })
                except Exception as e:
                    emit('directory_error', {'error': str(e)})
                    return

                emit('directory', {
                    'path': self.terminal_core.current_directory,
                    'items': items
                })

            except Exception as e:
                emit('directory_error', {'error': str(e)})

    def start(self, host: str = 'localhost', port: int = 5000):
        """Start the web server."""
        print("🌐 Starting Web Terminal Interface")
        print(f"📍 Server will be available at: http://{host}:{port}")
        print("📱 Open the URL in your browser to access the terminal")
        print("-" * 50)

        try:
            self.socketio.run(self.app, host=host, port=port, debug=False)
        except KeyboardInterrupt:
            print("\n👋 Web terminal server stopped.")
        except Exception as e:
            print(f"❌ Failed to start web server: {e}")

    def create_templates(self):
        """Create HTML templates for the web interface."""
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        static_dir = os.path.join(os.path.dirname(__file__), 'static')

        # Create directories if they don't exist
        os.makedirs(template_dir, exist_ok=True)
        os.makedirs(static_dir, exist_ok=True)

        # Create main HTML template
        html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Command Terminal</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='terminal.css') }}">
</head>
<body>
    <div class="terminal-container">
        <div class="terminal-header">
            <h1>🐍 Python Command Terminal</h1>
            <div class="system-info">
                <span id="current-dir">/</span>
                <span id="system-status">● Connected</span>
            </div>
        </div>

        <div class="terminal-output" id="output">
            <div class="welcome-message">
                <p>🚀 Welcome to Python Command Terminal (Web Interface)</p>
                <p>Type 'help' for available commands or 'exit' to quit.</p>
                <p>Current directory: <span id="welcome-dir">/</span></p>
            </div>
        </div>

        <div class="command-input-container">
            <div class="command-prompt">
                <span class="prompt-symbol">$</span>
                <input type="text" id="command-input" placeholder="Enter command..." autocomplete="off">
                <button id="send-button">Send</button>
            </div>
        </div>

        <div class="suggestions" id="suggestions" style="display: none;">
            <div class="suggestions-content" id="suggestions-content"></div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script src="{{ url_for('static', filename='terminal.js') }}"></script>
</body>
</html>"""

        # Create CSS file
        css_content = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Courier New', monospace;
    background-color: #1a1a1a;
    color: #ffffff;
    line-height: 1.6;
}

.terminal-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    height: 100vh;
    display: flex;
    flex-direction: column;
}

.terminal-header {
    background-color: #2d2d2d;
    padding: 15px;
    border-radius: 8px 8px 0 0;
    border-bottom: 2px solid #4a4a4a;
}

.terminal-header h1 {
    color: #61dafb;
    margin-bottom: 10px;
}

.system-info {
    display: flex;
    gap: 20px;
    font-size: 14px;
    color: #cccccc;
}

.terminal-output {
    flex: 1;
    background-color: #0d1117;
    padding: 20px;
    overflow-y: auto;
    border-left: 2px solid #4a4a4a;
    border-right: 2px solid #4a4a4a;
    font-size: 14px;
}

.welcome-message {
    margin-bottom: 20px;
}

.welcome-message p {
    margin: 5px 0;
}

.command-entry {
    display: flex;
    margin: 5px 0;
}

.command-entry .prompt {
    color: #61dafb;
    margin-right: 10px;
}

.command-entry .command {
    color: #ffffff;
}

.command-entry .output {
    color: #cccccc;
    margin-left: 20px;
}

.command-entry .error {
    color: #ff6b6b;
    margin-left: 20px;
}

.command-input-container {
    background-color: #2d2d2d;
    padding: 15px;
    border-radius: 0 0 8px 8px;
    border-top: 2px solid #4a4a4a;
}

.command-prompt {
    display: flex;
    align-items: center;
    gap: 10px;
}

.prompt-symbol {
    color: #61dafb;
    font-weight: bold;
}

#command-input {
    flex: 1;
    background-color: #1a1a1a;
    border: 1px solid #4a4a4a;
    color: #ffffff;
    padding: 8px 12px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-size: 14px;
}

#command-input:focus {
    outline: none;
    border-color: #61dafb;
}

#send-button {
    background-color: #61dafb;
    color: #1a1a1a;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
}

#send-button:hover {
    background-color: #4fb3d9;
}

.suggestions {
    position: absolute;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #2d2d2d;
    border: 1px solid #4a4a4a;
    border-radius: 4px;
    min-width: 300px;
    max-height: 200px;
    overflow-y: auto;
    z-index: 1000;
}

.suggestions-content {
    padding: 10px;
}

.suggestion-item {
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 3px;
}

.suggestion-item:hover {
    background-color: #4a4a4a;
}

.suggestion-command {
    color: #61dafb;
    font-weight: bold;
}

.suggestion-description {
    color: #cccccc;
    font-size: 12px;
    margin-left: 10px;
}

/* Scrollbar styling */
.terminal-output::-webkit-scrollbar {
    width: 8px;
}

.terminal-output::-webkit-scrollbar-track {
    background: #1a1a1a;
}

.terminal-output::-webkit-scrollbar-thumb {
    background: #4a4a4a;
    border-radius: 4px;
}

.terminal-output::-webkit-scrollbar-thumb:hover {
    background: #61dafb;
}"""

        # Create JavaScript file
        js_content = """document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const outputDiv = document.getElementById('output');
    const commandInput = document.getElementById('command-input');
    const sendButton = document.getElementById('send-button');
    const suggestionsDiv = document.getElementById('suggestions');
    const suggestionsContent = document.getElementById('suggestions-content');
    const currentDirSpan = document.getElementById('current-dir');
    const welcomeDirSpan = document.getElementById('welcome-dir');

    let commandHistory = [];
    let historyIndex = -1;

    // Socket event handlers
    socket.on('connect', function() {
        console.log('Connected to server');
        addOutput('System', 'Connected to terminal server', 'system');
    });

    socket.on('status', function(data) {
        addOutput('System', data.message, 'system');
    });

    socket.on('output', function(data) {
        const command = data.command;
        const output = data.output;
        const error = data.error;
        const exitCode = data.exit_code;
        const directory = data.directory;

        // Update current directory
        if (directory) {
            currentDirSpan.textContent = directory;
            welcomeDirSpan.textContent = directory;
        }

        // Add command to output
        addOutput('user', command, 'command');

        // Add output
        if (output) {
            addOutput('system', output, 'output');
        }

        // Add error
        if (error) {
            addOutput('system', 'Error: ' + error, 'error');
        }

        // Add exit code if not successful
        if (exitCode !== 0 && !output && !error) {
            addOutput('system', 'Command exited with code: ' + exitCode, 'error');
        }

        // Scroll to bottom
        outputDiv.scrollTop = outputDiv.scrollHeight;
    });

    socket.on('directory', function(data) {
        // Handle directory listing if needed
        console.log('Directory info:', data);
    });

    socket.on('directory_error', function(data) {
        addOutput('system', 'Directory error: ' + data.error, 'error');
    });

    // Command input handling
    function sendCommand() {
        const command = commandInput.value.trim();
        if (command) {
            socket.emit('command', {command: command});
            commandInput.value = '';
            hideSuggestions();
        }
    }

    sendButton.addEventListener('click', sendCommand);

    commandInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendCommand();
        } else if (e.key === 'Tab') {
            e.preventDefault();
            showSuggestions(commandInput.value);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            navigateHistory('up');
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            navigateHistory('down');
        }
    });

    // Command history navigation
    function navigateHistory(direction) {
        if (direction === 'up' && historyIndex < commandHistory.length - 1) {
            historyIndex++;
            commandInput.value = commandHistory[commandHistory.length - 1 - historyIndex];
        } else if (direction === 'down' && historyIndex > -1) {
            historyIndex--;
            if (historyIndex === -1) {
                commandInput.value = '';
            } else {
                commandInput.value = commandHistory[commandHistory.length - 1 - historyIndex];
            }
        }
    }

    // Suggestions
    function showSuggestions(query) {
        if (!query) {
            hideSuggestions();
            return;
        }

        fetch('/api/commands/suggest?q=' + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {
                if (data.suggestions && data.suggestions.length > 0) {
                    suggestionsContent.innerHTML = '';

                    data.suggestions.forEach(suggestion => {
                        const item = document.createElement('div');
                        item.className = 'suggestion-item';
                        item.innerHTML = '<span class="suggestion-command">' + suggestion + '</span>' +
                                       '<span class="suggestion-description">' + (data.description || '') + '</span>';
                        item.onclick = function() {
                            commandInput.value = suggestion;
                            hideSuggestions();
                            commandInput.focus();
                        };
                        suggestionsContent.appendChild(item);
                    });

                    suggestionsDiv.style.display = 'block';
                } else {
                    hideSuggestions();
                }
            })
            .catch(error => {
                console.error('Error fetching suggestions:', error);
                hideSuggestions();
            });
    }

    function hideSuggestions() {
        suggestionsDiv.style.display = 'none';
    }

    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!suggestionsDiv.contains(e.target) && e.target !== commandInput) {
            hideSuggestions();
        }
    });

    // Add output to terminal
    function addOutput(type, content, className) {
        const entry = document.createElement('div');
        entry.className = 'command-entry';

        if (type === 'user') {
            entry.innerHTML = '<span class="prompt">$</span> <span class="command">' + escapeHtml(content) + '</span>';
        } else {
            const span = document.createElement('span');
            span.className = className;
            span.textContent = content;
            entry.appendChild(span);
        }

        outputDiv.appendChild(entry);
    }

    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Focus on input when page loads
    commandInput.focus();
});"""

        # Write template files
        with open(os.path.join(template_dir, 'terminal.html'), 'w') as f:
            f.write(html_template)

        with open(os.path.join(static_dir, 'terminal.css'), 'w') as f:
            f.write(css_content)

        with open(os.path.join(static_dir, 'terminal.js'), 'w') as f:
            f.write(js_content)

        print("📄 Created web interface templates")
