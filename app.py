#!/usr/bin/env python3
"""
Flask application entry point for deployment.
This file is used for deploying the Python Command Terminal to platforms like Render.
"""

import os
import sys
from terminal.core import TerminalCore
from terminal.system_monitor import SystemMonitor
from terminal.ai_processor import AICommandProcessor
from terminal.simple_web_interface import SimpleWebTerminalInterface

def create_app():
    """Create and configure the Flask application."""
    # Set environment for web interface
    os.environ['TERMINAL_INTERFACE'] = 'web'

    # Initialize core components
    terminal_core = TerminalCore()
    system_monitor = SystemMonitor()
    ai_processor = AICommandProcessor(terminal_core)

    # Create web interface
    web_interface = SimpleWebTerminalInterface(terminal_core, system_monitor, ai_processor)

    return web_interface.app

# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get('PORT', 10000))

    # Run the Flask app with production settings
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # Disable debug mode for production
    )
