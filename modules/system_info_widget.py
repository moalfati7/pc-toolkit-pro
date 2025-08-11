"""System Information Widget for detailed hardware display."""

import psutil
import platform
import subprocess
import datetime
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QFrame,
    QScrollArea,
    QGridLayout,
    QGroupBox,
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap


class SystemInfoLoader(QThread):
    """Background thread for loading system information."""

    # Signals for different types of data
    uptime_updated = pyqtSignal(str)
    cpu_info_updated = pyqtSignal(dict)
    memory_info_updated = pyqtSignal(dict)
    disk_info_updated = pyqtSignal(dict)
    gpu_info_updated = pyqtSignal(dict)
    os_info_updated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._cpu_name_cache = None
        self._device_name_cache = None
        self._os_info_cache = {}
        self.running = True

    def stop(self):
        """Stop the background thread."""
        self.running = False
        self.quit()
        self.wait()

    def run(self):
        """Main thread loop for updating system information."""
        # Initial load of static information
        self.load_static_info()

        # Continuous updates for dynamic information
        while self.running:
            try:
                self.update_dynamic_info()
                self.msleep(2000)  # Update every 2 seconds
            except Exception as e:
                print(f"Error in system info loader: {e}")
                self.msleep(5000)  # Wait longer on error

    def load_static_info(self):
        """Load static system information that doesn't change."""
        try:
            # Load CPU info
            cpu_info = self.get_cpu_info()
            self.cpu_info_updated.emit(cpu_info)

            # Load OS info
            os_info = self.get_os_info_all()
            self.os_info_updated.emit(os_info)

        except Exception as e:
            print(f"Error loading static info: {e}")

    def update_dynamic_info(self):
        """Update dynamic system information."""
        try:
            # Update uptime
            uptime = self.get_uptime()
            self.uptime_updated.emit(uptime)

            # Update CPU usage
            cpu_usage = self.get_cpu_usage()
            self.cpu_info_updated.emit(cpu_usage)

            # Update memory info
            memory_info = self.get_memory_info()
            self.memory_info_updated.emit(memory_info)

            # Update disk info
            disk_info = self.get_disk_info()
            self.disk_info_updated.emit(disk_info)

            # Update GPU info
            gpu_info = self.get_gpu_info()
            self.gpu_info_updated.emit(gpu_info)

        except Exception as e:
            print(f"Error updating dynamic info: {e}")

    def get_uptime(self):
        """Get system uptime."""
        try:
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.datetime.now() - boot_time

            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            if days > 0:
                return f"{days} days, {hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except:
            return "Unknown"

    def get_cpu_info(self):
        """Get CPU information."""
        info = {"type": "static"}

        try:
            # CPU name (cached)
            if self._cpu_name_cache is None:
                self._cpu_name_cache = self._get_cpu_name()
            info["name"] = self._cpu_name_cache

            # Cores and threads
            physical_cores = psutil.cpu_count(logical=False)
            logical_cores = psutil.cpu_count(logical=True)
            info["cores"] = f"{physical_cores} cores, {logical_cores} threads"

            # Frequency
            try:
                freq = psutil.cpu_freq()
                if freq:
                    info["frequency"] = (
                        f"{freq.current:.0f} MHz (Max: {freq.max:.0f} MHz)"
                    )
                else:
                    info["frequency"] = "Unknown"
            except:
                info["frequency"] = "Unknown"

        except Exception as e:
            print(f"Error getting CPU info: {e}")
            info.update({"name": "Unknown", "cores": "Unknown", "frequency": "Unknown"})

        return info

    def get_cpu_usage(self):
        """Get CPU usage information."""
        try:
            cpu_percent = psutil.cpu_percent(interval=None)
            return {"type": "usage", "usage": cpu_percent}
        except:
            return {"type": "usage", "usage": 0}

    def _get_cpu_name(self):
        """Get CPU name using multiple methods."""
        cpu_name = "Unknown Processor"

        try:
            # Method 1: Try wmic
            try:
                result = subprocess.run(
                    ["wmic", "cpu", "get", "name", "/value"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )

                if result.returncode == 0 and result.stdout:
                    for line in result.stdout.split("\n"):
                        line = line.strip()
                        if line.startswith("Name=") and len(line) > 5:
                            cpu_name = line.split("=", 1)[1].strip()
                            if cpu_name and cpu_name != "Unknown Processor":
                                break
            except:
                pass

            # Method 2: Try PowerShell
            if cpu_name == "Unknown Processor":
                try:
                    result = subprocess.run(
                        [
                            "powershell",
                            "-Command",
                            "Get-WmiObject -Class Win32_Processor | Select-Object -ExpandProperty Name",
                        ],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )

                    if result.returncode == 0 and result.stdout.strip():
                        cpu_name = result.stdout.strip()
                except:
                    pass

            # Method 3: Try registry
            if cpu_name == "Unknown Processor":
                try:
                    import winreg

                    key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE,
                        r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
                    )
                    cpu_name = winreg.QueryValueEx(key, "ProcessorNameString")[
                        0
                    ].strip()
                    winreg.CloseKey(key)
                except:
                    pass

            # Method 4: Fallback
            if cpu_name == "Unknown Processor" or not cpu_name:
                cpu_name = platform.processor() or "Unknown Processor"

        except Exception as e:
            print(f"Error getting CPU name: {e}")
            cpu_name = platform.processor() or "Unknown Processor"

        return cpu_name

    def get_memory_info(self):
        """Get memory information."""
        try:
            memory = psutil.virtual_memory()

            return {
                "total_gb": memory.total / (1024**3),
                "percent": memory.percent,
                "used_gb": memory.used / (1024**3),
                "available_gb": memory.available / (1024**3),
            }
        except Exception as e:
            print(f"Error getting memory info: {e}")
            return {"total_gb": 0, "percent": 0, "used_gb": 0, "available_gb": 0}

    def get_disk_info(self):
        """Get disk information."""
        try:
            # Calculate total storage across all drives
            total_storage = 0
            try:
                partitions = psutil.disk_partitions()
                for partition in partitions:
                    try:
                        partition_usage = psutil.disk_usage(partition.mountpoint)
                        total_storage += partition_usage.total
                    except PermissionError:
                        continue
            except:
                pass

            # C: Drive specific information
            disk = psutil.disk_usage("C:\\")

            return {
                "total_storage": total_storage,
                "c_total_gb": disk.total / (1024**3),
                "c_usage_percent": (disk.used / disk.total) * 100,
                "c_used_gb": disk.used / (1024**3),
                "c_free_gb": disk.free / (1024**3),
            }
        except Exception as e:
            print(f"Error getting disk info: {e}")
            return {
                "total_storage": 0,
                "c_total_gb": 0,
                "c_usage_percent": 0,
                "c_used_gb": 0,
                "c_free_gb": 0,
            }

    def get_gpu_info(self):
        """Get GPU information."""
        try:
            # Try to get NVIDIA GPU info
            try:
                result = subprocess.run(
                    [
                        "nvidia-smi",
                        "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu",
                        "--format=csv,noheader,nounits",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )

                if result.returncode == 0 and result.stdout.strip():
                    gpu_data = result.stdout.strip().split(", ")
                    if len(gpu_data) >= 5:
                        return {
                            "available": True,
                            "name": gpu_data[0],
                            "usage": float(gpu_data[1]),
                            "memory_used_gb": float(gpu_data[2]) / 1024,
                            "memory_total_gb": float(gpu_data[3]) / 1024,
                            "temperature": float(gpu_data[4]),
                        }
            except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
                pass

            # No NVIDIA GPU found
            return {
                "available": False,
                "name": "No NVIDIA GPU detected",
                "usage": 0,
                "memory_used_gb": 0,
                "memory_total_gb": 0,
                "temperature": 0,
            }

        except Exception as e:
            print(f"Error getting GPU info: {e}")
            return {
                "available": False,
                "name": "Error",
                "usage": 0,
                "memory_used_gb": 0,
                "memory_total_gb": 0,
                "temperature": 0,
            }

    def get_os_info_all(self):
        """Get all OS information."""
        try:
            # Device name
            if self._device_name_cache is None:
                try:
                    import socket

                    self._device_name_cache = socket.gethostname()
                except:
                    self._device_name_cache = "Unknown"

            return {
                "device_name": self._device_name_cache,
                "user_name": self._get_os_info("user_name"),
                "edition": self._get_os_info("edition"),
                "version": self._get_os_info("version"),
                "build": self._get_os_info("build"),
                "install_date": self._get_os_info("install_date"),
                "experience": self._get_os_info("experience"),
                "arch": self._get_os_info("arch"),
            }
        except Exception as e:
            print(f"Error getting OS info: {e}")
            return {
                "device_name": "Unknown",
                "user_name": "Unknown",
                "edition": "Unknown",
                "version": "Unknown",
                "build": "Unknown",
                "install_date": "Unknown",
                "experience": "Unknown",
                "arch": "Unknown",
            }

    def _get_os_info(self, key):
        """Get specific OS information with caching."""
        if key in self._os_info_cache:
            return self._os_info_cache[key]

        try:
            if key == "user_name":
                try:
                    import getpass

                    value = getpass.getuser()
                except:
                    value = "Unknown"

            elif key == "edition":
                try:
                    # Get Windows edition and build number to determine correct version
                    edition_result = subprocess.run(
                        [
                            "powershell",
                            "-Command",
                            '(Get-ItemProperty "HKLM:SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion").ProductName',
                        ],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )

                    build_result = subprocess.run(
                        [
                            "powershell",
                            "-Command",
                            '(Get-ItemProperty "HKLM:SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion").CurrentBuild',
                        ],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )

                    if edition_result.returncode == 0 and edition_result.stdout.strip():
                        edition = edition_result.stdout.strip()

                        # Check build number to determine if it's Windows 11
                        if build_result.returncode == 0 and build_result.stdout.strip():
                            build_number = int(build_result.stdout.strip())
                            # Windows 11 starts from build 22000
                            if build_number >= 22000:
                                # Replace "Windows 10" with "Windows 11" if build indicates Windows 11
                                if "Windows 10" in edition:
                                    edition = edition.replace(
                                        "Windows 10", "Windows 11"
                                    )

                        value = edition
                    else:
                        value = f"{platform.system()} {platform.release()}"
                except:
                    value = f"{platform.system()} {platform.release()}"

            elif key == "version":
                try:
                    result = subprocess.run(
                        [
                            "powershell",
                            "-Command",
                            '(Get-ItemProperty "HKLM:SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion").DisplayVersion',
                        ],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )

                    if result.returncode == 0 and result.stdout.strip():
                        value = result.stdout.strip()
                    else:
                        value = platform.release()
                except:
                    value = platform.release()

            elif key == "build":
                try:
                    result = subprocess.run(
                        [
                            "powershell",
                            "-Command",
                            '(Get-ItemProperty "HKLM:SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion").CurrentBuild + "." + (Get-ItemProperty "HKLM:SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion").UBR',
                        ],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )

                    if result.returncode == 0 and result.stdout.strip():
                        value = result.stdout.strip()
                    else:
                        value = platform.version()
                except:
                    value = platform.version()

            elif key == "install_date":
                try:
                    result = subprocess.run(
                        [
                            "powershell",
                            "-Command",
                            '[DateTime]::FromFileTime((Get-ItemProperty "HKLM:SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion").InstallDate).ToString("MM/dd/yyyy")',
                        ],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )

                    if result.returncode == 0 and result.stdout.strip():
                        value = result.stdout.strip()
                    else:
                        value = "Unknown"
                except:
                    value = "Unknown"

            elif key == "experience":
                try:
                    result = subprocess.run(
                        [
                            "powershell",
                            "-Command",
                            'Get-AppxPackage -Name "MicrosoftWindows.Client.WebExperience" | Select-Object -ExpandProperty Version',
                        ],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )

                    if result.returncode == 0 and result.stdout.strip():
                        version = result.stdout.strip()
                        value = f"Windows Feature Experience Pack {version}"
                    else:
                        # Fallback method
                        result = subprocess.run(
                            [
                                "powershell",
                                "-Command",
                                '(Get-ItemProperty "HKLM:SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion").UBR',
                            ],
                            capture_output=True,
                            text=True,
                            timeout=5,
                            creationflags=subprocess.CREATE_NO_WINDOW,
                        )

                        if result.returncode == 0 and result.stdout.strip():
                            ubr = result.stdout.strip()
                            value = (
                                f"Windows Feature Experience Pack 1000.26100.{ubr}.0"
                            )
                        else:
                            value = "Windows Feature Experience Pack"
                except:
                    value = "Windows Feature Experience Pack"

            elif key == "arch":
                value = platform.architecture()[0]
            else:
                value = "Unknown"

            self._os_info_cache[key] = value
            return value
        except:
            self._os_info_cache[key] = "Unknown"
            return "Unknown"


class SystemInfoWidget(QWidget):
    """Widget for displaying detailed system information."""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_async_loader()
        self.show_loading_states()

    def setup_async_loader(self):
        """Setup the background thread for loading system information."""
        self.loader = SystemInfoLoader()

        # Connect signals
        self.loader.uptime_updated.connect(self.update_uptime_display)
        self.loader.cpu_info_updated.connect(self.update_cpu_display)
        self.loader.memory_info_updated.connect(self.update_memory_display)
        self.loader.disk_info_updated.connect(self.update_disk_display)
        self.loader.gpu_info_updated.connect(self.update_gpu_display)
        self.loader.os_info_updated.connect(self.update_os_display)

        # Start the loader
        self.loader.start()

    def show_loading_states(self):
        """Show loading states for all information."""
        # Set all labels to show "Loading..." initially
        self.uptime_label.setText("Loading...")

    def clear_cache(self):
        """Clear all cached system information to force refresh."""
        if hasattr(self, "loader"):
            self.loader._cpu_name_cache = None
            self.loader._device_name_cache = None
            self.loader._os_info_cache = {}

    def closeEvent(self, event):
        """Handle widget close event."""
        if hasattr(self, "loader"):
            self.loader.stop()
        super().closeEvent(event)

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Create scroll area for better handling of content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        # Main content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)

        # Add system information sections
        content_layout.addWidget(self.create_uptime_section())
        content_layout.addWidget(self.create_cpu_section())
        content_layout.addWidget(self.create_memory_section())
        content_layout.addWidget(self.create_disk_section())
        content_layout.addWidget(self.create_gpu_section())
        content_layout.addWidget(self.create_os_section())

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

    def create_section_frame(self, title, icon=""):
        """Create a styled frame for each section."""
        frame = QGroupBox(f"{icon} {title}")
        frame.setStyleSheet(
            """
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #e2e8f0;
                border: 2px solid #4a5568;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background: #2d3748;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #63b3ed;
                background: #2d3748;
            }
        """
        )
        return frame

    def create_info_row(self, label_text, value_text="", progress_value=None):
        """Create a row with label and value/progress bar."""
        row_widget = QWidget()
        layout = QHBoxLayout(row_widget)
        layout.setContentsMargins(0, 5, 0, 5)

        # Label
        label = QLabel(label_text)
        label.setStyleSheet("color: #cbd5e0; font-size: 12px; font-weight: normal;")
        label.setMinimumWidth(120)
        layout.addWidget(label)

        if progress_value is not None:
            # Progress bar
            progress = QProgressBar()
            progress.setValue(int(progress_value))
            progress.setStyleSheet(
                """
                QProgressBar {
                    border: 1px solid #4a5568;
                    border-radius: 4px;
                    text-align: center;
                    background: #1a202c;
                    color: #e2e8f0;
                    font-size: 11px;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #38a169, stop:0.5 #48bb78, stop:1 #68d391);
                    border-radius: 3px;
                }
            """
            )
            progress.setMaximumHeight(20)
            layout.addWidget(progress, 2)

            # Value label
            value_label = QLabel(value_text)
            value_label.setStyleSheet(
                "color: #e2e8f0; font-size: 12px; font-weight: bold;"
            )
            value_label.setMinimumWidth(80)
            value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            layout.addWidget(value_label)
        else:
            # Just value text
            value_label = QLabel(value_text)
            value_label.setStyleSheet("color: #e2e8f0; font-size: 12px;")
            value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            layout.addWidget(value_label, 1)

        return row_widget

    def create_uptime_section(self):
        """Create uptime information section."""
        frame = self.create_section_frame("System Uptime", "⏱️")
        layout = QVBoxLayout(frame)

        self.uptime_label = QLabel("Loading...")
        self.uptime_label.setStyleSheet(
            """
            color: #63b3ed; 
            font-size: 16px; 
            font-weight: bold; 
            padding: 10px;
            background: #1a202c;
            border-radius: 6px;
            border: 1px solid #4a5568;
        """
        )
        self.uptime_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.uptime_label)

        return frame

    def create_cpu_section(self):
        """Create CPU information section."""
        frame = self.create_section_frame("Processor Information", "🔥")
        layout = QVBoxLayout(frame)

        self.cpu_name_row = self.create_info_row("Processor:", "Loading...")
        self.cpu_cores_row = self.create_info_row("Cores/Threads:", "Loading...")
        self.cpu_freq_row = self.create_info_row("Base Frequency:", "Loading...")
        self.cpu_usage_row = self.create_info_row("Usage:", "0%", 0)

        layout.addWidget(self.cpu_name_row)
        layout.addWidget(self.cpu_cores_row)
        layout.addWidget(self.cpu_freq_row)
        layout.addWidget(self.cpu_usage_row)

        return frame

    def create_memory_section(self):
        """Create memory information section."""
        frame = self.create_section_frame("Memory Information", "💾")
        layout = QVBoxLayout(frame)

        self.memory_total_row = self.create_info_row("Total Memory:", "Loading...")
        self.memory_usage_row = self.create_info_row("Usage:", "0%", 0)
        self.memory_used_row = self.create_info_row("Used:", "Loading...")
        self.memory_available_row = self.create_info_row("Available:", "Loading...")

        layout.addWidget(self.memory_total_row)
        layout.addWidget(self.memory_usage_row)
        layout.addWidget(self.memory_used_row)
        layout.addWidget(self.memory_available_row)

        return frame

    def create_disk_section(self):
        """Create disk information section."""
        frame = self.create_section_frame("Storage Information", "💿")
        layout = QVBoxLayout(frame)

        self.total_storage_row = self.create_info_row("Total Storage:", "Loading...")
        self.disk_total_row = self.create_info_row("C: Drive Space:", "Loading...")
        self.disk_usage_row = self.create_info_row("C: Usage:", "0%", 0)
        self.disk_used_row = self.create_info_row("C: Used:", "Loading...")
        self.disk_free_row = self.create_info_row("C: Free:", "Loading...")

        layout.addWidget(self.total_storage_row)
        layout.addWidget(self.disk_total_row)
        layout.addWidget(self.disk_usage_row)
        layout.addWidget(self.disk_used_row)
        layout.addWidget(self.disk_free_row)

        return frame

    def create_gpu_section(self):
        """Create GPU information section."""
        frame = self.create_section_frame("Graphics Information", "🎮")
        layout = QVBoxLayout(frame)

        self.gpu_name_row = self.create_info_row("Graphics Card:", "Loading...")
        self.gpu_usage_row = self.create_info_row("Usage:", "0%", 0)
        self.gpu_memory_row = self.create_info_row("Memory:", "Loading...")
        self.gpu_temp_row = self.create_info_row("Temperature:", "Loading...")

        layout.addWidget(self.gpu_name_row)
        layout.addWidget(self.gpu_usage_row)
        layout.addWidget(self.gpu_memory_row)
        layout.addWidget(self.gpu_temp_row)

        return frame

    def create_os_section(self):
        """Create operating system information section."""
        frame = self.create_section_frame("Operating System", "🖥️")
        layout = QVBoxLayout(frame)

        self.device_name_row = self.create_info_row("Device Name:", "Loading...")
        self.user_name_row = self.create_info_row("User:", "Loading...")
        self.os_edition_row = self.create_info_row("Edition:", "Loading...")
        self.os_version_row = self.create_info_row("Version:", "Loading...")
        self.os_build_row = self.create_info_row("OS Build:", "Loading...")
        self.os_install_date_row = self.create_info_row("Installed on:", "Loading...")
        self.os_experience_row = self.create_info_row("Experience:", "Loading...")
        self.os_arch_row = self.create_info_row("Architecture:", "Loading...")

        layout.addWidget(self.device_name_row)
        layout.addWidget(self.user_name_row)
        layout.addWidget(self.os_edition_row)
        layout.addWidget(self.os_version_row)
        layout.addWidget(self.os_build_row)
        # layout.addWidget(self.os_install_date_row)
        layout.addWidget(self.os_experience_row)
        # layout.addWidget(self.os_arch_row)

        return frame

    # New async display update methods
    def update_uptime_display(self, uptime_str):
        """Update uptime display from background thread."""
        self.uptime_label.setText(uptime_str)

    def update_cpu_display(self, cpu_info):
        """Update CPU display from background thread."""
        try:
            if cpu_info.get("type") == "static":
                # Static CPU information
                self.cpu_name_row.findChildren(QLabel)[1].setText(
                    cpu_info.get("name", "Unknown")
                )
                self.cpu_cores_row.findChildren(QLabel)[1].setText(
                    cpu_info.get("cores", "Unknown")
                )
                self.cpu_freq_row.findChildren(QLabel)[1].setText(
                    cpu_info.get("frequency", "Unknown")
                )
            elif cpu_info.get("type") == "usage":
                # CPU usage information
                usage = cpu_info.get("usage", 0)
                self.cpu_usage_row.findChildren(QProgressBar)[0].setValue(int(usage))
                self.cpu_usage_row.findChildren(QLabel)[1].setText(f"{usage:.1f}%")
        except Exception as e:
            print(f"Error updating CPU display: {e}")

    def update_memory_display(self, memory_info):
        """Update memory display from background thread."""
        try:
            total_gb = memory_info.get("total_gb", 0)
            percent = memory_info.get("percent", 0)
            used_gb = memory_info.get("used_gb", 0)
            available_gb = memory_info.get("available_gb", 0)

            self.memory_total_row.findChildren(QLabel)[1].setText(f"{total_gb:.1f} GB")
            self.memory_usage_row.findChildren(QProgressBar)[0].setValue(int(percent))
            self.memory_usage_row.findChildren(QLabel)[1].setText(f"{percent:.1f}%")
            self.memory_used_row.findChildren(QLabel)[1].setText(f"{used_gb:.1f} GB")
            self.memory_available_row.findChildren(QLabel)[1].setText(
                f"{available_gb:.1f} GB"
            )
        except Exception as e:
            print(f"Error updating memory display: {e}")

    def update_disk_display(self, disk_info):
        """Update disk display from background thread."""
        try:
            total_storage = disk_info.get("total_storage", 0)
            c_total_gb = disk_info.get("c_total_gb", 0)
            c_usage_percent = disk_info.get("c_usage_percent", 0)
            c_used_gb = disk_info.get("c_used_gb", 0)
            c_free_gb = disk_info.get("c_free_gb", 0)

            # Format total storage
            if total_storage > 0:
                if total_storage >= 1024**4:  # TB
                    storage_text = f"{total_storage / (1024**4):.1f} TB"
                else:  # GB
                    storage_text = f"{total_storage / (1024**3):.0f} GB"
            else:
                storage_text = "Unknown"

            self.total_storage_row.findChildren(QLabel)[1].setText(storage_text)
            self.disk_total_row.findChildren(QLabel)[1].setText(f"{c_total_gb:.1f} GB")
            self.disk_usage_row.findChildren(QProgressBar)[0].setValue(
                int(c_usage_percent)
            )
            self.disk_usage_row.findChildren(QLabel)[1].setText(
                f"{c_usage_percent:.1f}%"
            )
            self.disk_used_row.findChildren(QLabel)[1].setText(f"{c_used_gb:.1f} GB")
            self.disk_free_row.findChildren(QLabel)[1].setText(f"{c_free_gb:.1f} GB")
        except Exception as e:
            print(f"Error updating disk display: {e}")

    def update_gpu_display(self, gpu_info):
        """Update GPU display from background thread."""
        try:
            if gpu_info.get("available", False):
                name = gpu_info.get("name", "Unknown")
                usage = gpu_info.get("usage", 0)
                memory_used_gb = gpu_info.get("memory_used_gb", 0)
                memory_total_gb = gpu_info.get("memory_total_gb", 0)
                temperature = gpu_info.get("temperature", 0)

                self.gpu_name_row.findChildren(QLabel)[1].setText(name)
                self.gpu_usage_row.findChildren(QProgressBar)[0].setValue(int(usage))
                self.gpu_usage_row.findChildren(QLabel)[1].setText(f"{usage:.1f}%")

                if memory_total_gb > 0:
                    memory_percent = (memory_used_gb / memory_total_gb) * 100
                    self.gpu_memory_row.findChildren(QLabel)[1].setText(
                        f"{memory_used_gb:.1f} GB / {memory_total_gb:.1f} GB"
                    )
                else:
                    memory_percent = 0
                    self.gpu_memory_row.findChildren(QLabel)[1].setText("Unknown")

                self.gpu_temp_row.findChildren(QLabel)[1].setText(
                    f"{temperature:.0f}°C"
                )
            else:
                self.gpu_name_row.findChildren(QLabel)[1].setText(
                    gpu_info.get("name", "No NVIDIA GPU detected")
                )
                self.gpu_usage_row.findChildren(QProgressBar)[0].setValue(0)
                self.gpu_usage_row.findChildren(QLabel)[1].setText("0%")
                self.gpu_memory_row.findChildren(QLabel)[1].setText("N/A")
                self.gpu_temp_row.findChildren(QLabel)[1].setText("N/A")
        except Exception as e:
            print(f"Error updating GPU display: {e}")

    def update_os_display(self, os_info):
        """Update OS display from background thread."""
        try:
            self.device_name_row.findChildren(QLabel)[1].setText(
                os_info.get("device_name", "Unknown")
            )
            self.user_name_row.findChildren(QLabel)[1].setText(
                os_info.get("user_name", "Unknown")
            )
            self.os_edition_row.findChildren(QLabel)[1].setText(
                os_info.get("edition", "Unknown")
            )
            self.os_version_row.findChildren(QLabel)[1].setText(
                os_info.get("version", "Unknown")
            )
            self.os_build_row.findChildren(QLabel)[1].setText(
                os_info.get("build", "Unknown")
            )
            self.os_experience_row.findChildren(QLabel)[1].setText(
                os_info.get("experience", "Unknown")
            )
        except Exception as e:
            print(f"Error updating OS display: {e}")
