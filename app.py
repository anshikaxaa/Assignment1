#!/usr/bin/env python3
"""
Flask application entry point for deployment.
This file is used for deploying the Python Command Terminal to platforms like Render.
"""

import os
import sys
from main import main

def create_app():
    """Create and configure the Flask application."""
    # Set environment for web interface
    os.environ['TERMINAL_INTERFACE'] = 'web'

    # Create Flask app
    app = main()

    return app

# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get('PORT', 10000))

    # Run the Flask app with production settings
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,  # Disable debug mode for production
        allow_unsafe_werkzeug=True  # Allow Werkzeug in production
    )
