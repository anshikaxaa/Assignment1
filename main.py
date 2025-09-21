#!/usr/bin/env python3
"""
Python-Based Command Terminal
A fully functioning command terminal that mimics system terminal behavior.
Built with Python backend supporting file operations, system monitoring, and more.
"""

import sys
import os
from terminal.core import TerminalCore
from terminal.interface import TerminalInterface
from terminal.ai_processor import AICommandProcessor
from terminal.system_monitor import SystemMonitor


def main():
    """Main entry point for the command terminal."""
    print("🚀 Welcome to Python Command Terminal")
    print("Type 'help' for available commands or 'exit' to quit.")
    print("-" * 50)

    # Initialize core components
    terminal_core = TerminalCore()
    system_monitor = SystemMonitor()
    ai_processor = AICommandProcessor(terminal_core)

    # Choose interface type (default to web for deployment)
    interface_type = os.environ.get('TERMINAL_INTERFACE', 'web')

    if interface_type == 'web':
        # Web interface (default for deployment)
        from terminal.simple_web_interface import SimpleWebTerminalInterface
        interface = SimpleWebTerminalInterface(terminal_core, system_monitor, ai_processor)
        interface.start()
    else:
        # CLI interface (for local development)
        interface = TerminalInterface(terminal_core, system_monitor, ai_processor)
        interface.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Terminal session ended.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
