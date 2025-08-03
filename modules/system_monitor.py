"""System monitoring functionality for PC Tool."""

import psutil
import platform
import datetime
from PyQt6.QtCore import QThread, pyqtSignal


class SystemInfoThread(QThread):
    """Thread for continuously monitoring system information."""
    
    info_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = True
    
    def run(self):
        """Main thread loop for system monitoring."""
        while self.running:
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('C:\\')
                boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
                uptime = datetime.datetime.now() - boot_time
                
                info = {
                    'cpu': cpu_percent,
                    'memory_percent': memory.percent,
                    'memory_used': memory.used,
                    'memory_total': memory.total,
                    'disk_percent': (disk.used / disk.total) * 100,
                    'disk_used': disk.used,
                    'disk_total': disk.total,
                    'uptime': str(uptime).split('.')[0]
                }
                
                self.info_updated.emit(info)
                
            except Exception as e:
                print(f"System monitoring error: {e}")
                
            self.msleep(2000)
    
    def stop(self):
        """Stop the monitoring thread."""
        self.running = False
        self.quit()
        self.wait()


class SystemMonitor:
    """Handles system monitoring operations."""
    
    @staticmethod
    def get_system_info():
        """Get static system information."""
        return {
            'os': f"{platform.system()} {platform.release()}",
            'processor': platform.processor(),
            'architecture': platform.architecture()[0],
            'machine': platform.machine(),
            'python_version': platform.python_version()
        }