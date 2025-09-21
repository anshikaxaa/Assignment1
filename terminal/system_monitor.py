"""
System monitoring functionality for the terminal.
Provides real-time system information and performance metrics.
"""

import os
import psutil
import platform
import time
from typing import Dict, Any, Optional
from datetime import datetime


class SystemMonitor:
    """
    System monitoring class that provides real-time system information.
    """

    def __init__(self):
        self.system_info = self._get_system_info()
        self.start_time = time.time()

    def _get_system_info(self) -> Dict[str, Any]:
        """Get basic system information."""
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'hostname': platform.node(),
            'username': os.environ.get('USERNAME', 'Unknown'),
        }

    def get_cpu_info(self) -> Dict[str, Any]:
        """Get CPU information and usage."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()

            info = {
                'usage_percent': cpu_percent,
                'physical_cores': cpu_count,
                'logical_cores': cpu_count_logical,
            }

            if cpu_freq:
                info['current_freq'] = cpu_freq.current
                info['min_freq'] = cpu_freq.min
                info['max_freq'] = cpu_freq.max

            return info
        except Exception as e:
            return {'error': str(e)}

    def get_memory_info(self) -> Dict[str, Any]:
        """Get memory information and usage."""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()

            return {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'free': memory.free,
                'usage_percent': memory.percent,
                'swap_total': swap.total,
                'swap_used': swap.used,
                'swap_free': swap.free,
                'swap_percent': swap.percent,
            }
        except Exception as e:
            return {'error': str(e)}

    def get_disk_info(self, path: str = '/') -> Dict[str, Any]:
        """Get disk usage information."""
        try:
            disk = psutil.disk_usage(path)

            return {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'usage_percent': disk.percent,
            }
        except Exception as e:
            return {'error': str(e)}

    def get_network_info(self) -> Dict[str, Any]:
        """Get network information."""
        try:
            network = psutil.net_io_counters()

            return {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv,
                'errin': network.errin,
                'errout': network.errout,
                'dropin': network.dropin,
                'dropout': network.dropout,
            }
        except Exception as e:
            return {'error': str(e)}

    def get_process_info(self, limit: int = 10) -> list:
        """Get information about running processes."""
        try:
            processes = []

            for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)

            return processes[:limit]
        except Exception as e:
            return [{'error': str(e)}]

    def get_system_uptime(self) -> float:
        """Get system uptime in seconds."""
        try:
            return time.time() - psutil.boot_time()
        except:
            return time.time() - self.start_time

    def get_temperature_info(self) -> Dict[str, Any]:
        """Get system temperature information."""
        try:
            temps = psutil.sensors_temperatures()

            if temps:
                return temps
            else:
                return {'message': 'Temperature sensors not available'}
        except Exception as e:
            return {'error': str(e)}

    def get_fan_info(self) -> Dict[str, Any]:
        """Get fan speed information."""
        try:
            fans = psutil.sensors_fans()

            if fans:
                return fans
            else:
                return {'message': 'Fan sensors not available'}
        except Exception as e:
            return {'error': str(e)}

    def get_battery_info(self) -> Dict[str, Any]:
        """Get battery information if available."""
        try:
            battery = psutil.sensors_battery()

            if battery:
                return {
                    'percent': battery.percent,
                    'secsleft': battery.secsleft,
                    'power_plugged': battery.power_plugged,
                }
            else:
                return {'message': 'No battery found'}
        except Exception as e:
            return {'error': str(e)}

    def get_detailed_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information."""
        return {
            'system': self.system_info,
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disk': self.get_disk_info(),
            'network': self.get_network_info(),
            'uptime': self.get_system_uptime(),
            'processes': self.get_process_info(5),
            'timestamp': datetime.now().isoformat(),
        }

    def format_bytes(self, bytes_value: int) -> str:
        """Format bytes into human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"

    def format_uptime(self, seconds: float) -> str:
        """Format uptime seconds into human readable format."""
        days, remainder = divmod(int(seconds), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if seconds or not parts:
            parts.append(f"{seconds}s")

        return ' '.join(parts)

    def display_system_status(self):
        """Display formatted system status."""
        print("📊 System Status")
        print("=" * 30)

        # CPU Info
        cpu_info = self.get_cpu_info()
        if 'error' not in cpu_info:
            print(f"CPU Usage: {cpu_info['usage_percent']}%")
            print(f"CPU Cores: {cpu_info.get('physical_cores', 'N/A')}")

        # Memory Info
        memory_info = self.get_memory_info()
        if 'error' not in memory_info:
            print(f"Memory Usage: {memory_info['usage_percent']}%")
            print(f"Memory Used: {self.format_bytes(memory_info['used'])} / {self.format_bytes(memory_info['total'])}")

        # Disk Info
        disk_info = self.get_disk_info()
        if 'error' not in disk_info:
            print(f"Disk Usage: {disk_info['usage_percent']}%")
            print(f"Disk Used: {self.format_bytes(disk_info['used'])} / {self.format_bytes(disk_info['total'])}")

        # Uptime
        uptime = self.get_system_uptime()
        print(f"System Uptime: {self.format_uptime(uptime)}")

        print("-" * 30)
