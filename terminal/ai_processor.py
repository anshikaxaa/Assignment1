"""
AI command processor for intelligent command suggestions and processing.
Provides AI-powered assistance for terminal commands.
"""

import re
import os
from typing import List, Dict, Optional, Tuple
from .core import TerminalCore


class AICommandProcessor:
    """
    AI-powered command processor that provides intelligent suggestions
    and command processing capabilities.
    """

    def __init__(self, terminal_core: TerminalCore):
        self.terminal_core = terminal_core
        self.command_patterns = self._initialize_command_patterns()

    def _initialize_command_patterns(self) -> Dict[str, Dict[str, any]]:
        """Initialize command patterns for AI processing."""
        return {
            'file_operations': {
                'patterns': [
                    r'list\s+(files?|contents?|directory)',
                    r'show\s+(files?|contents?)',
                    r'what\'?s?\s+in\s+(this\s+)?(folder|directory)',
                    r'display\s+(files?|contents?)',
                ],
                'suggestions': ['ls', 'ls -la', 'dir'],
                'description': 'List files and directories'
            },
            'navigation': {
                'patterns': [
                    r'go\s+to\s+(.+)',
                    r'change\s+(to\s+)?(.+)',
                    r'cd\s+(.+)',
                    r'navigate\s+to\s+(.+)',
                ],
                'suggestions': ['cd'],
                'description': 'Change directory'
            },
            'create_file': {
                'patterns': [
                    r'create\s+(file|document)\s+(.+)',
                    r'make\s+(file|document)\s+(.+)',
                    r'new\s+(file|document)\s+(.+)',
                    r'touch\s+(.+)',
                ],
                'suggestions': ['touch'],
                'description': 'Create new file'
            },
            'create_directory': {
                'patterns': [
                    r'create\s+(folder|directory)\s+(.+)',
                    r'make\s+(folder|directory)\s+(.+)',
                    r'new\s+(folder|directory)\s+(.+)',
                    r'mkdir\s+(.+)',
                ],
                'suggestions': ['mkdir'],
                'description': 'Create new directory'
            },
            'copy': {
                'patterns': [
                    r'copy\s+(.+)\s+to\s+(.+)',
                    r'duplicate\s+(.+)',
                    r'cp\s+(.+)',
                ],
                'suggestions': ['cp'],
                'description': 'Copy files or directories'
            },
            'move': {
                'patterns': [
                    r'move\s+(.+)\s+to\s+(.+)',
                    r'rename\s+(.+)\s+to\s+(.+)',
                    r'mv\s+(.+)',
                ],
                'suggestions': ['mv'],
                'description': 'Move or rename files'
            },
            'delete': {
                'patterns': [
                    r'delete\s+(.+)',
                    r'remove\s+(.+)',
                    r'rm\s+(.+)',
                    r'get\s+rid\s+of\s+(.+)',
                ],
                'suggestions': ['rm', 'rm -rf'],
                'description': 'Delete files or directories'
            },
            'search': {
                'patterns': [
                    r'find\s+(.+)',
                    r'search\s+for\s+(.+)',
                    r'look\s+for\s+(.+)',
                ],
                'suggestions': ['find', 'grep'],
                'description': 'Search for files or content'
            },
            'system_info': {
                'patterns': [
                    r'system\s+info',
                    r'computer\s+info',
                    r'machine\s+info',
                    r'what\'?s?\s+my\s+system',
                ],
                'suggestions': ['uname -a', 'systeminfo'],
                'description': 'Get system information'
            },
            'cpu_info': {
                'patterns': [
                    r'cpu\s+(info|usage|status)',
                    r'processor\s+(info|usage)',
                    r'how\'?s?\s+the\s+cpu',
                ],
                'suggestions': ['cpu'],
                'description': 'Get CPU information'
            },
            'memory_info': {
                'patterns': [
                    r'memory\s+(info|usage)',
                    r'ram\s+(info|usage)',
                    r'how\s+much\s+memory',
                ],
                'suggestions': ['memory'],
                'description': 'Get memory information'
            },
            'disk_info': {
                'patterns': [
                    r'disk\s+(info|usage|space)',
                    r'storage\s+(info|usage)',
                    r'how\s+much\s+space',
                ],
                'suggestions': ['disk'],
                'description': 'Get disk usage information'
            },
            'processes': {
                'patterns': [
                    r'running\s+processes',
                    r'what\'?s?\s+running',
                    r'process\s+list',
                    r'task\s+manager',
                ],
                'suggestions': ['ps', 'ps aux'],
                'description': 'List running processes'
            },
            'network': {
                'patterns': [
                    r'network\s+(info|status)',
                    r'internet\s+(info|status)',
                    r'connection\s+status',
                ],
                'suggestions': ['ping', 'curl'],
                'description': 'Get network information'
            },
            'help': {
                'patterns': [
                    r'help\s+me',
                    r'how\s+to\s+(.+)',
                    r'what\s+can\s+i\s+do',
                    r'show\s+commands',
                ],
                'suggestions': ['help'],
                'description': 'Get help information'
            }
        }

    def process_natural_language(self, text: str) -> Dict[str, any]:
        """
        Process natural language input and suggest commands.

        Args:
            text: Natural language text input

        Returns:
            Dictionary containing suggestions and analysis
        """
        text = text.lower().strip()

        # Check for exact command matches first
        if text in self.terminal_core.supported_commands:
            return {
                'type': 'exact_match',
                'command': text,
                'description': self.terminal_core.supported_commands[text],
                'confidence': 1.0
            }

        # Analyze text against patterns
        best_match = None
        best_confidence = 0.0

        for category, data in self.command_patterns.items():
            for pattern in data['patterns']:
                match = re.search(pattern, text)
                if match:
                    confidence = len(match.group()) / len(text) if text else 0
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = {
                            'type': 'pattern_match',
                            'category': category,
                            'pattern': pattern,
                            'matches': match.groups(),
                            'suggestions': data['suggestions'],
                            'description': data['description'],
                            'confidence': confidence
                        }

        if best_match and best_confidence > 0.3:
            return best_match

        # No good match found
        return {
            'type': 'no_match',
            'suggestions': ['help'],
            'description': 'No matching command found',
            'confidence': 0.0
        }

    def suggest_corrections(self, command: str) -> List[str]:
        """
        Suggest corrections for typos in commands.

        Args:
            command: Command with potential typos

        Returns:
            List of suggested corrections
        """
        suggestions = []
        command_lower = command.lower()

        # Check for similar commands
        for cmd in self.terminal_core.supported_commands.keys():
            if self._calculate_similarity(command_lower, cmd) > 0.6:
                suggestions.append(cmd)

        # Add common corrections
        corrections = {
            'sl': 'ls',
            'cd..': 'cd ..',
            'cd-': 'cd -',
            'ls-l': 'ls -l',
            'ls-a': 'ls -a',
            'ps-aux': 'ps aux',
        }

        if command_lower in corrections:
            suggestions.append(corrections[command_lower])

        return list(set(suggestions))  # Remove duplicates

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings."""
        if len(str1) == 0 or len(str2) == 0:
            return 0.0

        # Simple Levenshtein distance-based similarity
        matrix = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]

        for i in range(len(str1) + 1):
            matrix[i][0] = i
        for j in range(len(str2) + 1):
            matrix[0][j] = j

        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                cost = 0 if str1[i-1] == str2[j-1] else 1
                matrix[i][j] = min(
                    matrix[i-1][j] + 1,      # deletion
                    matrix[i][j-1] + 1,      # insertion
                    matrix[i-1][j-1] + cost  # substitution
                )

        max_len = max(len(str1), len(str2))
        return 1.0 - (matrix[len(str1)][len(str2)] / max_len)

    def explain_command(self, command: str) -> Optional[str]:
        """
        Provide explanation for a command.

        Args:
            command: Command to explain

        Returns:
            Explanation string or None if not found
        """
        command = command.strip().split()[0].lower()

        if command in self.terminal_core.supported_commands:
            return self.terminal_core.supported_commands[command]

        return None

    def get_command_examples(self, command: str) -> List[str]:
        """
        Get usage examples for a command.

        Args:
            command: Command to get examples for

        Returns:
            List of example usage strings
        """
        examples = {
            'ls': ['ls', 'ls -la', 'ls -l', 'ls -a', 'ls *.py'],
            'cd': ['cd', 'cd ..', 'cd /home', 'cd Documents'],
            'mkdir': ['mkdir new_folder', 'mkdir -p parent/child'],
            'cp': ['cp file1.txt file2.txt', 'cp -r folder1 folder2'],
            'mv': ['mv old_name.txt new_name.txt', 'mv file.txt Documents/'],
            'rm': ['rm file.txt', 'rm -rf folder'],
            'cat': ['cat file.txt', 'cat file1.txt file2.txt'],
            'grep': ['grep "search_term" file.txt', 'grep -r "pattern" .'],
            'find': ['find . -name "*.py"', 'find /home -type f -name "*.txt"'],
            'ps': ['ps', 'ps aux', 'ps -ef'],
            'cpu': ['cpu'],
            'memory': ['memory'],
            'disk': ['disk'],
            'help': ['help', 'help ls', 'help cd'],
        }

        return examples.get(command, [command])

    def validate_command(self, command: str) -> Tuple[bool, str]:
        """
        Validate a command and provide feedback.

        Args:
            command: Command to validate

        Returns:
            Tuple of (is_valid, feedback_message)
        """
        if not command.strip():
            return False, "Empty command"

        parts = command.strip().split()
        cmd = parts[0].lower()

        if cmd in self.terminal_core.supported_commands:
            return True, f"Valid command: {self.terminal_core.supported_commands[cmd]}"

        # Check for potential typos
        suggestions = self.suggest_corrections(command)
        if suggestions:
            return False, f"Command not found. Did you mean: {', '.join(suggestions[:3])}?"

        return False, "Unknown command. Type 'help' for available commands."

    def get_command_completion(self, partial_command: str) -> List[str]:
        """
        Get command completions for partial input.

        Args:
            partial_command: Partial command to complete

        Returns:
            List of possible completions
        """
        completions = []

        # Complete command names
        for cmd in self.terminal_core.supported_commands.keys():
            if cmd.startswith(partial_command.lower()):
                completions.append(cmd)

        # Complete file/directory names if applicable
        if partial_command and not partial_command.endswith(' '):
            try:
                parts = partial_command.split()
                if len(parts) > 1:
                    prefix = parts[-1]
                    directory = self.terminal_core.current_directory

                    # Try to complete file/directory names
                    try:
                        items = os.listdir(directory)
                        for item in items:
                            if item.startswith(prefix):
                                full_completion = ' '.join(parts[:-1] + [item])
                                completions.append(full_completion)
                    except:
                        pass
            except:
                pass

        return completions
