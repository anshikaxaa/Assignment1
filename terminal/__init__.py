"""
Terminal package for Python Command Terminal.
Contains all terminal-related modules and functionality.
"""

from .core import TerminalCore
from .interface import TerminalInterface
from .system_monitor import SystemMonitor
from .ai_processor import AICommandProcessor

__version__ = "1.0.0"
__all__ = ['TerminalCore', 'TerminalInterface', 'SystemMonitor', 'AICommandProcessor']
