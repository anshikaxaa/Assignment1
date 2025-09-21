"""
Simple web interface for the terminal application.
Provides a web-based terminal interface using Flask without SocketIO.
This is designed for deployment platforms like Render.
"""

import os
import json
from typing import Dict, Any
from flask import Flask, render_template, request, jsonify
from .core import TerminalCore
from .system_monitor import SystemMonitor
from .ai_processor import AICommandProcessor


class SimpleWebTerminalInterface:
    """
    Simple web-based terminal interface using Flask (no SocketIO).
    Designed for deployment platforms like Render.
    """

    def __init__(self, terminal_core: TerminalCore, system_monitor: SystemMonitor,
                 ai_processor: AICommandProcessor):
        self.terminal_core = terminal_core
        self.system_monitor = system_monitor
        self.ai_processor = ai_processor
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        """Set up Flask routes."""

        @self.app.route('/')
        def index():
            """Serve the main web interface."""
            return self.get_html_template()

        @self.app.route('/execute', methods=['POST'])
        def execute():
            """Execute a command via REST API."""
            try:
                data = request.get_json()
                command = data.get('command', '')

                if not command:
                    return jsonify({
                        'output': '',
                        'error': 'Empty command',
                        'exit_code': 1
                    })

                # Execute command
                output, exit_code, error = self.terminal_core.execute_command(command)

                return jsonify({
                    'command': command,
                    'output': output,
                    'exit_code': exit_code,
                    'error': error,
                    'directory': self.terminal_core.current_directory
                })

            except Exception as e:
                return jsonify({
                    'command': data.get('command', '') if 'data' in locals() else '',
                    'output': '',
                    'exit_code': 1,
                    'error': str(e),
                    'directory': self.terminal_core.current_directory
                })

        @self.app.route('/api/system/info')
        def get_system_info():
            """Get system information via REST API."""
            try:
                # Get basic system info
                info = {
                    'current_directory': self.terminal_core.current_directory,
                    'supported_commands': len(self.terminal_core.supported_commands),
                    'command_history_count': len(self.terminal_core.command_history)
                }
                return jsonify(info)
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    def get_html_template(self):
        """Generate HTML template for the web interface."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Python Command Terminal</title>
            <style>
                body {{
                    font-family: monospace;
                    background: #1a1a1a;
                    color: #fff;
                    padding: 20px;
                    margin: 0;
                }}
                .terminal {{
                    background: #000;
                    padding: 20px;
                    border-radius: 5px;
                    min-height: 400px;
                    max-height: 600px;
                    overflow-y: auto;
                    margin-bottom: 20px;
                }}
                .command {{ color: #61dafb; }}
                .output {{ color: #ccc; }}
                .error {{ color: #ff6b6b; }}
                input {{
                    width: 100%;
                    padding: 10px;
                    background: #333;
                    color: #fff;
                    border: none;
                    margin: 10px 0;
                    font-family: monospace;
                }}
                button {{
                    background: #61dafb;
                    color: #000;
                    border: none;
                    padding: 10px 20px;
                    cursor: pointer;
                    margin: 10px 0;
                }}
                .command-entry {{ margin: 5px 0; }}
            </style>
        </head>
        <body>
            <h1>🐍 Python Command Terminal</h1>
            <div class="terminal" id="terminal">
                <div class="command-entry">
                    <span class="command">🚀 Welcome to Python Command Terminal</span>
                </div>
                <div class="command-entry">
                    <span class="output">Type 'help' for available commands or 'exit' to quit.</span>
                </div>
                <div class="command-entry">
                    <span class="output">Current directory: {self.terminal_core.current_directory}</span>
                </div>
            </div>
            <br>
            <input type="text" id="commandInput" placeholder="Enter command..." autofocus>
            <button onclick="executeCommand()">Execute</button>

            <script>
                let commandHistory = [];
                let historyIndex = -1;

                function executeCommand() {{
                    const input = document.getElementById('commandInput');
                    const command = input.value.trim();
                    if (!command) return;

                    // Add command to terminal
                    const terminal = document.getElementById('terminal');
                    terminal.innerHTML += '<div class="command-entry"><span class="command">$ ' + escapeHtml(command) + '</span></div>';

                    // Send to server
                    fetch('/execute', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ command: command }})
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        // Add output
                        if (data.output) {{
                            terminal.innerHTML += '<div class="command-entry"><span class="output">' + escapeHtml(data.output).replace(/\\n/g, '<br>') + '</span></div>';
                        }}
                        // Add error
                        if (data.error) {{
                            terminal.innerHTML += '<div class="command-entry"><span class="error">Error: ' + escapeHtml(data.error) + '</span></div>';
                        }}
                        // Update directory if changed
                        if (data.directory) {{
                            terminal.innerHTML += '<div class="command-entry"><span class="output">Directory: ' + escapeHtml(data.directory) + '</span></div>';
                        }}
                        terminal.scrollTop = terminal.scrollHeight;
                    }})
                    .catch(error => {{
                        terminal.innerHTML += '<div class="command-entry"><span class="error">Network error: ' + error + '</span></div>';
                    }});

                    input.value = '';
                }}

                document.getElementById('commandInput').addEventListener('keypress', function(e) {{
                    if (e.key === 'Enter') {{
                        executeCommand();
                    }}
                }});

                // Escape HTML to prevent XSS
                function escapeHtml(text) {{
                    const div = document.createElement('div');
                    div.textContent = text;
                    return div.innerHTML;
                }}

                // Focus on input when page loads
                document.getElementById('commandInput').focus();
            </script>
        </body>
        </html>
        """

    def start(self, host: str = '0.0.0.0', port: int = 5000):
        """Start the web server."""
        print("🌐 Starting Simple Web Terminal Interface")
        print(f"📍 Server will be available at: http://{host}:{port}")
        print("-" * 50)

        try:
            self.app.run(host=host, port=port, debug=False)
        except KeyboardInterrupt:
            print("\n👋 Web terminal server stopped.")
        except Exception as e:
            print(f"❌ Failed to start web server: {e}")
