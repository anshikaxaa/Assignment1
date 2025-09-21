"""
Core terminal functionality for command execution and processing.
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from datetime import datetime


class TerminalCore:
    """
    Core terminal functionality that handles command execution.
    """

    def __init__(self):
        self.current_directory = os.getcwd()
        self.command_history = []
        self.environment = os.environ.copy()
        self.supported_commands = self._get_supported_commands()

    def _get_supported_commands(self) -> Dict[str, str]:
        """Get dictionary of supported commands and their descriptions."""
        return {
            # File operations
            'ls': 'List directory contents',
            'dir': 'List directory contents (Windows)',
            'cd': 'Change directory',
            'pwd': 'Print working directory',
            'mkdir': 'Create directory',
            'rmdir': 'Remove directory',
            'rm': 'Remove files or directories',
            'cp': 'Copy files or directories',
            'mv': 'Move/rename files or directories',
            'cat': 'Display file contents',
            'head': 'Display first lines of file',
            'tail': 'Display last lines of file',
            'touch': 'Create empty file or update timestamp',

            # System information
            'whoami': 'Display current user',
            'hostname': 'Display system hostname',
            'date': 'Display current date and time',
            'echo': 'Display text or variables',
            'env': 'Display environment variables',

            # Process management
            'ps': 'Display process information',
            'kill': 'Terminate processes',
            'jobs': 'Display background jobs',
            'bg': 'Resume job in background',
            'fg': 'Resume job in foreground',

            # System monitoring
            'cpu': 'Display CPU information',
            'memory': 'Display memory usage',
            'disk': 'Display disk usage',
            'top': 'Display system processes (top-like)',

            # Terminal utilities
            'clear': 'Clear terminal screen',
            'history': 'Show command history',
            'help': 'Display help information',
            'exit': 'Exit terminal',
            'quit': 'Exit terminal',

            # Text processing
            'grep': 'Search text in files',
            'find': 'Find files and directories',
            'sort': 'Sort lines in files',
            'uniq': 'Remove duplicate lines',
            'wc': 'Count lines, words, characters',

            # Archive and compression
            'tar': 'Archive files',
            'zip': 'Create zip archives',
            'unzip': 'Extract zip archives',

            # Network utilities
            'ping': 'Test network connectivity',
            'curl': 'Transfer data from servers',
            'wget': 'Download files from web',
        }

    def execute_command(self, command: str) -> Tuple[str, int, str]:
        """
        Execute a command and return output, exit code, and error message.

        Args:
            command: The command string to execute

        Returns:
            Tuple of (output, exit_code, error_message)
        """
        if not command.strip():
            return "", 0, ""

        # Add to history
        self.command_history.append({
            'command': command,
            'timestamp': datetime.now(),
            'directory': self.current_directory
        })

        # Parse command and arguments
        parts = command.strip().split()
        cmd = parts[0].lower()
        args = parts[1:]

        try:
            # Handle built-in commands
            if cmd in ['exit', 'quit']:
                return "Goodbye!", 0, ""

            elif cmd == 'help':
                return self._handle_help(args), 0, ""

            elif cmd == 'clear':
                return self._handle_clear(), 0, ""

            elif cmd == 'history':
                return self._handle_history(args), 0, ""

            elif cmd == 'cd':
                return self._handle_cd(args), 0, ""

            elif cmd == 'pwd':
                return self._handle_pwd(), 0, ""

            elif cmd == 'ls' or cmd == 'dir':
                return self._handle_ls(args), 0, ""

            elif cmd == 'mkdir':
                return self._handle_mkdir(args), 0, ""

            elif cmd == 'rmdir':
                return self._handle_rmdir(args), 0, ""

            elif cmd == 'rm':
                return self._handle_rm(args), 0, ""

            elif cmd == 'cp':
                return self._handle_cp(args), 0, ""

            elif cmd == 'mv':
                return self._handle_mv(args), 0, ""

            elif cmd == 'cat':
                return self._handle_cat(args), 0, ""

            elif cmd == 'touch':
                return self._handle_touch(args), 0, ""

            elif cmd == 'echo':
                return self._handle_echo(args), 0, ""

            elif cmd == 'whoami':
                return self._handle_whoami(), 0, ""

            elif cmd == 'hostname':
                return self._handle_hostname(), 0, ""

            elif cmd == 'date':
                return self._handle_date(args), 0, ""

            elif cmd == 'env':
                return self._handle_env(args), 0, ""

            elif cmd == 'cpu':
                return self._handle_cpu(), 0, ""

            elif cmd == 'memory':
                return self._handle_memory(), 0, ""

            elif cmd == 'disk':
                return self._handle_disk(), 0, ""

            elif cmd == 'ps':
                return self._handle_ps(), 0, ""

            elif cmd == 'grep':
                return self._handle_grep(args), 0, ""

            elif cmd == 'find':
                return self._handle_find(args), 0, ""

            # Handle external commands
            else:
                return self._execute_external_command(command)

        except Exception as e:
            return "", 1, str(e)

    def _execute_external_command(self, command: str) -> Tuple[str, int, str]:
        """Execute external system command."""
        try:
            # Use subprocess to execute external commands
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.current_directory,
                env=self.environment
            )

            output = result.stdout.strip()
            if result.stderr:
                output += "\n" + result.stderr.strip()

            return output, result.returncode, ""

        except Exception as e:
            return "", 1, f"Failed to execute command: {str(e)}"

    # Command handlers
    def _handle_help(self, args: List[str]) -> str:
        """Handle help command."""
        if not args:
            # Show general help
            help_text = "Available commands:\n"
            help_text += "=" * 50 + "\n"

            for cmd, desc in self.supported_commands.items():
                help_text += f"{cmd:<15} - {desc}\n"

            help_text += "\nFor more information on a specific command, type: help <command>"
            return help_text

        else:
            # Show specific command help
            cmd = args[0].lower()
            if cmd in self.supported_commands:
                return f"{cmd}: {self.supported_commands[cmd]}"
            else:
                return f"No help available for '{cmd}'. Type 'help' for available commands."

    def _handle_clear(self) -> str:
        """Handle clear command."""
        os.system('cls' if platform.system() == 'Windows' else 'clear')
        return ""

    def _handle_history(self, args: List[str]) -> str:
        """Handle history command."""
        if not self.command_history:
            return "No command history available."

        history_text = "Command History:\n"
        history_text += "=" * 30 + "\n"

        for i, entry in enumerate(self.command_history[-20:], 1):  # Show last 20 commands
            timestamp = entry['timestamp'].strftime('%H:%M:%S')
            cmd = entry['command']
            history_text += f"{i:3d}  {timestamp}  {cmd}\n"

        return history_text

    def _handle_cd(self, args: List[str]) -> str:
        """Handle cd command."""
        if not args:
            return "cd: missing argument"

        target_dir = args[0]

        # Handle special cases
        if target_dir == "~":
            target_dir = os.path.expanduser("~")
        elif target_dir == "-":
            # Go back to previous directory (if we had one)
            return "Previous directory not tracked"

        try:
            new_dir = os.path.abspath(os.path.join(self.current_directory, target_dir))
            if os.path.isdir(new_dir):
                self.current_directory = new_dir
                return ""
            else:
                return f"cd: {target_dir}: No such file or directory"
        except Exception as e:
            return f"cd: {str(e)}"

    def _handle_pwd(self) -> str:
        """Handle pwd command."""
        return self.current_directory

    def _handle_ls(self, args: List[str]) -> str:
        """Handle ls/dir command."""
        target_dir = self.current_directory
        show_hidden = '-a' in args or '--all' in args
        long_format = '-l' in args or '--long' in args

        try:
            items = os.listdir(target_dir)
            if not show_hidden:
                items = [item for item in items if not item.startswith('.')]

            if long_format:
                # Long format (similar to ls -l)
                result = []
                for item in sorted(items):
                    item_path = os.path.join(target_dir, item)
                    try:
                        stat_info = os.stat(item_path)
                        permissions = self._get_permissions(stat_info.st_mode)
                        size = stat_info.st_size
                        mtime = datetime.fromtimestamp(stat_info.st_mtime).strftime('%b %d %H:%M')
                        result.append(f"{permissions} {size:8d} {mtime} {item}")
                    except:
                        result.append(item)
                return "\n".join(result)
            else:
                # Simple format
                return "\n".join(sorted(items))

        except Exception as e:
            return f"ls: {str(e)}"

    def _handle_mkdir(self, args: List[str]) -> str:
        """Handle mkdir command."""
        if not args:
            return "mkdir: missing operand"

        for dir_name in args:
            try:
                os.makedirs(os.path.join(self.current_directory, dir_name), exist_ok=True)
            except Exception as e:
                return f"mkdir: cannot create directory '{dir_name}': {str(e)}"

        return ""

    def _handle_rmdir(self, args: List[str]) -> str:
        """Handle rmdir command."""
        if not args:
            return "rmdir: missing operand"

        for dir_name in args:
            try:
                target = os.path.join(self.current_directory, dir_name)
                os.rmdir(target)
            except Exception as e:
                return f"rmdir: failed to remove '{dir_name}': {str(e)}"

        return ""

    def _handle_rm(self, args: List[str]) -> str:
        """Handle rm command."""
        if not args:
            return "rm: missing operand"

        recursive = '-r' in args
        args = [arg for arg in args if arg not in ['-r']]

        for file_name in args:
            try:
                target = os.path.join(self.current_directory, file_name)
                if recursive and os.path.isdir(target):
                    shutil.rmtree(target)
                else:
                    os.remove(target)
            except Exception as e:
                return f"rm: cannot remove '{file_name}': {str(e)}"

        return ""

    def _handle_cp(self, args: List[str]) -> str:
        """Handle cp command."""
        if len(args) < 2:
            return "cp: missing destination file operand"

        recursive = '-r' in args
        args = [arg for arg in args if arg not in ['-r']]

        sources = args[:-1]
        destination = args[-1]

        try:
            dest_path = os.path.join(self.current_directory, destination)

            for source in sources:
                src_path = os.path.join(self.current_directory, source)

                if recursive and os.path.isdir(src_path):
                    shutil.copytree(src_path, dest_path)
                else:
                    shutil.copy2(src_path, dest_path)

        except Exception as e:
            return f"cp: {str(e)}"

        return ""

    def _handle_mv(self, args: List[str]) -> str:
        """Handle mv command."""
        if len(args) < 2:
            return "mv: missing destination file operand"

        sources = args[:-1]
        destination = args[-1]

        try:
            dest_path = os.path.join(self.current_directory, destination)

            for source in sources:
                src_path = os.path.join(self.current_directory, source)
                shutil.move(src_path, dest_path)

        except Exception as e:
            return f"mv: {str(e)}"

        return ""

    def _handle_cat(self, args: List[str]) -> str:
        """Handle cat command."""
        if not args:
            return "cat: missing file operand"

        result = []
        for file_name in args:
            try:
                file_path = os.path.join(self.current_directory, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    result.append(f.read())
            except Exception as e:
                return f"cat: {file_name}: {str(e)}"

        return "\n".join(result)

    def _handle_touch(self, args: List[str]) -> str:
        """Handle touch command."""
        if not args:
            return "touch: missing file operand"

        for file_name in args:
            try:
                file_path = os.path.join(self.current_directory, file_name)
                Path(file_path).touch()
            except Exception as e:
                return f"touch: cannot touch '{file_name}': {str(e)}"

        return ""

    def _handle_echo(self, args: List[str]) -> str:
        """Handle echo command."""
        return " ".join(args)

    def _handle_whoami(self) -> str:
        """Handle whoami command."""
        return os.environ.get('USERNAME', 'Unknown')

    def _handle_hostname(self) -> str:
        """Handle hostname command."""
        return platform.node()

    def _handle_date(self, args: List[str]) -> str:
        """Handle date command."""
        format_str = "%a %b %d %H:%M:%S %Z %Y" if not args else " ".join(args)
        return datetime.now().strftime(format_str)

    def _handle_env(self, args: List[str]) -> str:
        """Handle env command."""
        if args:
            # Show specific environment variables
            result = []
            for var in args:
                value = os.environ.get(var, f"{var}: undefined variable")
                result.append(value)
            return "\n".join(result)
        else:
            # Show all environment variables
            return "\n".join(f"{k}={v}" for k, v in sorted(os.environ.items()))

    def _handle_cpu(self) -> str:
        """Handle cpu command."""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()

            result = f"CPU Usage: {cpu_percent}%\n"
            result += f"CPU Cores: {cpu_count}\n"
            if cpu_freq:
                result += f"CPU Frequency: {cpu_freq.current:.2f} MHz\n"

            return result.strip()
        except ImportError:
            return "psutil not installed. Install with: pip install psutil"

    def _handle_memory(self) -> str:
        """Handle memory command."""
        try:
            import psutil
            memory = psutil.virtual_memory()

            result = f"Total Memory: {memory.total / (1024**3):.2f} GB\n"
            result += f"Available Memory: {memory.available / (1024**3):.2f} GB\n"
            result += f"Used Memory: {memory.used / (1024**3):.2f} GB\n"
            result += f"Memory Usage: {memory.percent}%\n"

            return result.strip()
        except ImportError:
            return "psutil not installed. Install with: pip install psutil"

    def _handle_disk(self) -> str:
        """Handle disk command."""
        try:
            import psutil
            disk = psutil.disk_usage('/')

            result = f"Total Disk Space: {disk.total / (1024**3):.2f} GB\n"
            result += f"Used Disk Space: {disk.used / (1024**3):.2f} GB\n"
            result += f"Free Disk Space: {disk.free / (1024**3):.2f} GB\n"
            result += f"Disk Usage: {disk.percent}%\n"

            return result.strip()
        except ImportError:
            return "psutil not installed. Install with: pip install psutil"

    def _handle_ps(self) -> str:
        """Handle ps command."""
        try:
            import psutil
            processes = []

            for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)

            result = f"{'PID':<8} {'NAME':<20} {'STATUS':<10} {'CPU%':<8} {'MEM%':<8}\n"
            result += "-" * 60 + "\n"

            for proc in processes[:20]:  # Show top 20 processes
                result += f"{proc['pid']:<8} {proc['name']:<20} {proc['status']:<10} "
                result += f"{proc['cpu_percent']:<8.1f} {proc['memory_percent']:<8.1f}\n"

            return result.strip()
        except ImportError:
            return "psutil not installed. Install with: pip install psutil"

    def _handle_grep(self, args: List[str]) -> str:
        """Handle grep command."""
        if len(args) < 2:
            return "grep: missing arguments"

        pattern = args[0]
        files = args[1:]

        try:
            import re
            results = []

            for file_name in files:
                file_path = os.path.join(self.current_directory, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if re.search(pattern, line):
                                results.append(f"{file_name}:{line_num}:{line.strip()}")
                except Exception as e:
                    results.append(f"grep: {file_name}: {str(e)}")

            return "\n".join(results) if results else ""
        except ImportError:
            return "re module not available"

    def _handle_find(self, args: List[str]) -> str:
        """Handle find command."""
        if not args:
            return "find: missing arguments"

        path = args[0] if args else '.'
        name_pattern = args[1] if len(args) > 1 else '*'

        try:
            results = []
            search_path = os.path.join(self.current_directory, path)

            for root, dirs, files in os.walk(search_path):
                # Filter directories and files based on pattern
                for item in dirs + files:
                    if name_pattern == '*' or name_pattern in item:
                        rel_path = os.path.relpath(os.path.join(root, item), self.current_directory)
                        results.append(rel_path)

            return "\n".join(results) if results else ""
        except Exception as e:
            return f"find: {str(e)}"

    def _get_permissions(self, mode: int) -> str:
        """Convert file mode to permissions string."""
        permissions = ['r', 'w', 'x'] * 3 + ['r', 'w', 'x']
        result = []

        for i in range(9):
            if mode & (1 << (8 - i)):
                result.append(permissions[i])
            else:
                result.append('-')

        return ''.join(result)
