"""
Terminal interface for user interaction.
Handles command input, output display, and user experience.
"""

import os
import sys
import time
from typing import Optional, Tuple
from .core import TerminalCore
from .system_monitor import SystemMonitor
from .ai_processor import AICommandProcessor


class TerminalInterface:
    """
    Command-line interface for the terminal application.
    Handles user input, command processing, and output display.
    """

    def __init__(self, terminal_core: TerminalCore, system_monitor: SystemMonitor,
                 ai_processor: AICommandProcessor):
        self.terminal_core = terminal_core
        self.system_monitor = system_monitor
        self.ai_processor = ai_processor
        self.running = False
        self.command_count = 0

    def start(self):
        """Start the terminal interface."""
        self.running = True
        self._show_welcome()

        try:
            while self.running:
                try:
                    # Get current directory for prompt
                    current_dir = self.terminal_core.current_directory
                    dir_name = os.path.basename(current_dir) or current_dir

                    # Create prompt
                    prompt = f"🐍 {dir_name} $ "

                    # Get user input
                    command = input(prompt).strip()

                    if not command:
                        continue

                    self.command_count += 1

                    # Process command
                    self._process_command(command)

                except KeyboardInterrupt:
                    print("\nType 'exit' to quit or press Ctrl+C again to force quit.")
                    continue
                except EOFError:
                    print("\n👋 Goodbye!")
                    break

        except Exception as e:
            print(f"❌ Interface error: {e}")
        finally:
            self._cleanup()

    def _show_welcome(self):
        """Display welcome message and system information."""
        print("🚀 Python Command Terminal")
        print("=" * 40)
        print("A powerful terminal emulator built with Python")
        print()
        print("Features:")
        print("  • File operations (ls, cd, mkdir, rm, cp, mv, cat)")
        print("  • System monitoring (cpu, memory, disk, ps)")
        print("  • Text processing (grep, find, sort)")
        print("  • Network utilities (ping, curl)")
        print("  • Command history and help")
        print()
        print("Type 'help' for available commands or 'exit' to quit.")
        print("-" * 40)

    def _process_command(self, command: str):
        """Process a user command."""
        # Handle special commands first
        if command.lower() in ['exit', 'quit']:
            self._handle_exit()
            return

        if command.lower() == 'clear':
            self._handle_clear()
            return

        # Execute command through terminal core
        output, exit_code, error = self.terminal_core.execute_command(command)

        # Display results
        if output:
            print(output)

        if error:
            print(f"❌ Error: {error}")

        if exit_code != 0 and not output and not error:
            print(f"Command exited with code: {exit_code}")

    def _handle_exit(self):
        """Handle exit command."""
        if self.command_count > 0:
            print(f"\n📊 Session Summary:")
            print(f"   Commands executed: {self.command_count}")
            print(f"   Current directory: {self.terminal_core.current_directory}")

        print("\n👋 Thank you for using Python Command Terminal!")
        print("Goodbye! ✨")
        self.running = False

    def _handle_clear(self):
        """Handle clear command."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _cleanup(self):
        """Cleanup resources before exit."""
        try:
            # Save command history if needed
            pass
        except:
            pass

    def stop(self):
        """Stop the terminal interface."""
        self.running = False
