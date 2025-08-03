import os
import sys
import shutil
import ctypes
import subprocess
import humanize
import psutil
import platform
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QTabWidget,
    QProgressBar,
    QGroupBox,
    QSpinBox,
    QMessageBox,
    QFrame,
)
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon, QPixmap
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class SystemInfoThread(QThread):
    info_updated = pyqtSignal(dict)
    
    def run(self):
        while True:
            try:
                info = {
                    'cpu_percent': psutil.cpu_percent(interval=1),
                    'memory': psutil.virtual_memory(),
                    'disk': psutil.disk_usage('C:\\'),
                    'uptime': datetime.now() - datetime.fromtimestamp(psutil.boot_time())
                }
                self.info_updated.emit(info)
            except:
                pass
            self.msleep(2000)


class PCToolkit(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔧 PC Tool - Advanced System Manager")
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        self.setFixedSize(600, 500)
        self.set_dark_theme()
        
        # Start system info thread
        self.info_thread = SystemInfoThread()
        self.info_thread.info_updated.connect(self.update_system_info)
        self.info_thread.start()
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #3a3a4a;
                border-radius: 8px;
                background-color: rgba(25, 25, 35, 0.95);
                margin-top: 8px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a4a5a, stop:1 #3a3a4a);
                color: #e0e0e8;
                padding: 12px 20px;
                margin-right: 3px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 600;
                font-size: 10pt;
                min-width: 80px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #005a9e);
                color: white;
                font-weight: 700;
            }
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a5a6a, stop:1 #4a4a5a);
            }
        """)
        
        # System Info Tab
        self.create_system_tab()
        
        # Cleaner Tab
        self.create_cleaner_tab()
        
        # Power Management Tab
        self.create_power_tab()
        
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def create_system_tab(self):
        system_widget = QWidget()
        layout = QVBoxLayout()
        
        # System Info Group
        info_group = QGroupBox("💻 System Information")
        info_layout = QGridLayout()
        
        self.cpu_label = QLabel("CPU: Loading...")
        self.memory_label = QLabel("Memory: Loading...")
        self.disk_label = QLabel("Disk C: Loading...")
        self.uptime_label = QLabel("Uptime: Loading...")
        self.os_label = QLabel(f"OS: {platform.system()} {platform.release()}")
        
        info_layout.addWidget(self.cpu_label, 0, 0)
        info_layout.addWidget(self.memory_label, 1, 0)
        info_layout.addWidget(self.disk_label, 2, 0)
        info_layout.addWidget(self.uptime_label, 3, 0)
        info_layout.addWidget(self.os_label, 4, 0)
        
        # Progress bars
        self.cpu_progress = QProgressBar()
        self.memory_progress = QProgressBar()
        self.disk_progress = QProgressBar()
        
        info_layout.addWidget(self.cpu_progress, 0, 1)
        info_layout.addWidget(self.memory_progress, 1, 1)
        info_layout.addWidget(self.disk_progress, 2, 1)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Quick Actions
        actions_group = QGroupBox("⚡ Quick Actions")
        actions_layout = QHBoxLayout()
        
        task_mgr_btn = QPushButton("📊 Task Manager")
        task_mgr_btn.clicked.connect(lambda: subprocess.Popen("taskmgr"))
        
        device_mgr_btn = QPushButton("🔧 Device Manager")
        device_mgr_btn.clicked.connect(lambda: subprocess.Popen("devmgmt.msc", shell=True))
        
        control_panel_btn = QPushButton("⚙️ Control Panel")
        control_panel_btn.clicked.connect(lambda: subprocess.Popen("control"))
        
        actions_layout.addWidget(task_mgr_btn)
        actions_layout.addWidget(device_mgr_btn)
        actions_layout.addWidget(control_panel_btn)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        layout.addStretch()
        system_widget.setLayout(layout)
        self.tabs.addTab(system_widget, "📊 System")

    def create_cleaner_tab(self):
        cleaner_widget = QWidget()
        layout = QVBoxLayout()
        
        self.status = QLabel("Ready")
        self.status.setFont(QFont("Segoe UI", 10))
        self.status.setStyleSheet("""
            color: #00d4aa;
            font-weight: 700;
            font-size: 11pt;
            padding: 8px 12px;
            background-color: rgba(0, 212, 170, 0.1);
            border: 1px solid rgba(0, 212, 170, 0.3);
            border-radius: 6px;
        """)
        layout.addWidget(self.status)
        
        self.log = QTextEdit()
        self.log.setFont(QFont("Consolas", 9))
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(150)
        layout.addWidget(self.log)
        
        # Cleaning buttons
        clean_group = QGroupBox("🧹 Cleaning Options")
        clean_layout = QVBoxLayout()
        
        btn1 = QPushButton("🧹 Clean Temp, Prefetch, Recycle Bin")
        btn1.clicked.connect(self.clean_temp)
        btn1.setStyleSheet(self.get_button_style("#28a745"))
        
        btn2 = QPushButton("🧼 Full Disk Cleanup (Drive C)")
        btn2.clicked.connect(self.full_disk_cleanup)
        btn2.setStyleSheet(self.get_button_style("#007bff"))
        
        btn3 = QPushButton("🗑️ Empty Recycle Bin Only")
        btn3.clicked.connect(self.empty_recycle_bin_only)
        btn3.setStyleSheet(self.get_button_style("#ffc107"))
        
        clean_layout.addWidget(btn1)
        clean_layout.addWidget(btn2)
        clean_layout.addWidget(btn3)
        
        clean_group.setLayout(clean_layout)
        layout.addWidget(clean_group)
        
        cleaner_widget.setLayout(layout)
        self.tabs.addTab(cleaner_widget, "🧹 Cleaner")

    def create_power_tab(self):
        power_widget = QWidget()
        layout = QVBoxLayout()
        
        # Power Options Group
        power_group = QGroupBox("⚡ Power Management")
        power_layout = QGridLayout()
        
        # Immediate actions
        shutdown_btn = QPushButton("🔴 Shutdown Now")
        shutdown_btn.clicked.connect(self.shutdown_now)
        shutdown_btn.setStyleSheet(self.get_button_style("#dc3545"))
        
        restart_btn = QPushButton("🔄 Restart Now")
        restart_btn.clicked.connect(self.restart_now)
        restart_btn.setStyleSheet(self.get_button_style("#fd7e14"))
        
        sleep_btn = QPushButton("😴 Sleep")
        sleep_btn.clicked.connect(self.sleep_now)
        sleep_btn.setStyleSheet(self.get_button_style("#6f42c1"))
        
        hibernate_btn = QPushButton("🛌 Hibernate")
        hibernate_btn.clicked.connect(self.hibernate_now)
        hibernate_btn.setStyleSheet(self.get_button_style("#20c997"))
        
        lock_btn = QPushButton("🔒 Lock Screen")
        lock_btn.clicked.connect(self.lock_screen)
        lock_btn.setStyleSheet(self.get_button_style("#6c757d"))
        
        signout_btn = QPushButton("👤 Sign Out")
        signout_btn.clicked.connect(self.sign_out)
        signout_btn.setStyleSheet(self.get_button_style("#17a2b8"))
        
        power_layout.addWidget(shutdown_btn, 0, 0)
        power_layout.addWidget(restart_btn, 0, 1)
        power_layout.addWidget(sleep_btn, 1, 0)
        power_layout.addWidget(hibernate_btn, 1, 1)
        power_layout.addWidget(lock_btn, 2, 0)
        power_layout.addWidget(signout_btn, 2, 1)
        
        power_group.setLayout(power_layout)
        layout.addWidget(power_group)
        
        # Scheduled Actions Group
        scheduled_group = QGroupBox("⏰ Scheduled Actions")
        scheduled_layout = QVBoxLayout()
        
        timer_layout = QHBoxLayout()
        timer_layout.addWidget(QLabel("Minutes:"))
        
        self.timer_spinbox = QSpinBox()
        self.timer_spinbox.setRange(1, 1440)  # 1 minute to 24 hours
        self.timer_spinbox.setValue(60)
        timer_layout.addWidget(self.timer_spinbox)
        
        scheduled_shutdown_btn = QPushButton("⏰ Schedule Shutdown")
        scheduled_shutdown_btn.clicked.connect(self.schedule_shutdown)
        scheduled_shutdown_btn.setStyleSheet(self.get_button_style("#e83e8c"))
        
        cancel_scheduled_btn = QPushButton("❌ Cancel Scheduled")
        cancel_scheduled_btn.clicked.connect(self.cancel_scheduled)
        cancel_scheduled_btn.setStyleSheet(self.get_button_style("#6c757d"))
        
        timer_layout.addWidget(scheduled_shutdown_btn)
        timer_layout.addWidget(cancel_scheduled_btn)
        
        scheduled_layout.addLayout(timer_layout)
        scheduled_group.setLayout(scheduled_layout)
        layout.addWidget(scheduled_group)
        
        # Warning label with better styling
        warning_label = QLabel("⚠️ Warning: These actions will affect your system immediately!")
        warning_label.setStyleSheet("""
            color: #ffb347;
            font-weight: 700;
            font-size: 10pt;
            text-align: center;
            padding: 10px;
            background-color: rgba(255, 179, 71, 0.1);
            border: 1px solid rgba(255, 179, 71, 0.3);
            border-radius: 6px;
            margin: 8px 0;
        """)
        warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(warning_label)
        
        layout.addStretch()
        power_widget.setLayout(layout)
        self.tabs.addTab(power_widget, "⚡ Power")

    def get_button_style(self, color):
        # Convert hex to RGB for gradient calculations
        color_rgb = color.lstrip('#')
        r, g, b = tuple(int(color_rgb[i:i+2], 16) for i in (0, 2, 4))
        darker_r, darker_g, darker_b = max(0, r-30), max(0, g-30), max(0, b-30)
        lighter_r, lighter_g, lighter_b = min(255, r+20), min(255, g+20), min(255, b+20)
        
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb({lighter_r}, {lighter_g}, {lighter_b}),
                    stop:1 rgb({r}, {g}, {b}));
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 12px 16px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 11pt;
                font-family: 'Segoe UI', sans-serif;
                text-align: center;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb({min(255, lighter_r+15)}, {min(255, lighter_g+15)}, {min(255, lighter_b+15)}),
                    stop:1 rgb({min(255, r+15)}, {min(255, g+15)}, {min(255, b+15)}));
                border: 1px solid rgba(255, 255, 255, 0.2);
                transform: translateY(-1px);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb({darker_r}, {darker_g}, {darker_b}),
                    stop:1 rgb({max(0, r-15)}, {max(0, g-15)}, {max(0, b-15)}));
                border: 1px solid rgba(0, 0, 0, 0.3);
                transform: translateY(1px);
            }}
        """

    def update_system_info(self, info):
        try:
            # Update CPU
            cpu_percent = info['cpu_percent']
            self.cpu_label.setText(f"CPU Usage: {cpu_percent:.1f}%")
            self.cpu_progress.setValue(int(cpu_percent))
            
            # Update Memory
            memory = info['memory']
            memory_percent = memory.percent
            memory_used = humanize.naturalsize(memory.used, binary=True)
            memory_total = humanize.naturalsize(memory.total, binary=True)
            self.memory_label.setText(f"Memory: {memory_used}/{memory_total} ({memory_percent:.1f}%)")
            self.memory_progress.setValue(int(memory_percent))
            
            # Update Disk
            disk = info['disk']
            disk_percent = (disk.used / disk.total) * 100
            disk_used = humanize.naturalsize(disk.used, binary=True)
            disk_total = humanize.naturalsize(disk.total, binary=True)
            self.disk_label.setText(f"Disk C: {disk_used}/{disk_total} ({disk_percent:.1f}%)")
            self.disk_progress.setValue(int(disk_percent))
            
            # Update Uptime
            uptime = info['uptime']
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            self.uptime_label.setText(f"Uptime: {days}d {hours}h {minutes}m")
            
        except Exception as e:
            pass

    def set_dark_theme(self):
        # Modern dark theme with better colors
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(25, 25, 35))  # Deep blue-gray
        palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 245))  # Soft white
        palette.setColor(QPalette.ColorRole.Base, QColor(18, 18, 25))  # Darker blue-gray
        palette.setColor(QPalette.ColorRole.Text, QColor(240, 240, 245))  # Soft white
        palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 60))  # Medium blue-gray
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(240, 240, 245))  # Soft white
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))  # Windows blue
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        self.setPalette(palette)
        
        # Apply global stylesheet for better appearance
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                font-size: 10pt;
                color: #f0f0f5;
            }
            QGroupBox {
                font-weight: 600;
                font-size: 11pt;
                color: #e0e0e8;
                border: 2px solid #3a3a4a;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 8px;
                background-color: rgba(35, 35, 45, 0.6);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: #ffffff;
                font-weight: 700;
            }
            QLabel {
                color: #e8e8ed;
                font-weight: 500;
            }
            QProgressBar {
                border: 1px solid #4a4a5a;
                border-radius: 6px;
                text-align: center;
                font-weight: 600;
                background-color: #2a2a3a;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0078d4, stop:0.5 #106ebe, stop:1 #005a9e);
                border-radius: 5px;
            }
            QTextEdit {
                background-color: #1e1e28;
                border: 1px solid #3a3a4a;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', 'SF Mono', 'Monaco', monospace;
                font-size: 9pt;
                color: #e8e8ed;
            }
            QSpinBox {
                background-color: #2a2a3a;
                border: 1px solid #4a4a5a;
                border-radius: 4px;
                padding: 4px 8px;
                font-weight: 500;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #3a3a4a;
                border: none;
                width: 16px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #4a4a5a;
            }
        """)

    def log_message(self, msg):
        self.log.append(msg)
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())

    def clean_temp(self):
        if not self.ensure_admin():
            return

        self.status.setText("🧹 Cleaning...")
        self.log.clear()

        folders = [os.getenv("TEMP"), r"C:\Windows\Temp", r"C:\Windows\Prefetch"]
        total_size = 0

        for folder in folders:
            if not os.path.exists(folder):
                continue
            for item in os.listdir(folder):
                full_path = os.path.join(folder, item)
                try:
                    if os.path.isfile(full_path):
                        size = os.path.getsize(full_path)
                        os.remove(full_path)
                        total_size += size
                    elif os.path.isdir(full_path):
                        size = self.dir_size(full_path)
                        shutil.rmtree(full_path, ignore_errors=True)
                        total_size += size
                    self.log_message(f"✔ {item}")
                except Exception as e:
                    self.log_message(f"✖ {item}: {e}")

        self.empty_recycle_bin()
        human_readable = humanize.naturalsize(total_size, binary=True)
        self.status.setText(f"✅ Temp Cleaned: {human_readable}")

    def full_disk_cleanup(self):
        if not self.ensure_admin():
            return

        self.status.setText("🧼 Running full Disk Cleanup...")
        self.log_message("Launching: cleanmgr /sagerun:1337")
        try:
            subprocess.Popen("cleanmgr /sagerun:1337", shell=True)
        except Exception as e:
            self.log_message(f"Error running disk cleanup: {e}")

    def dir_size(self, path):
        total = 0
        for root, dirs, files in os.walk(path):
            for f in files:
                try:
                    total += os.path.getsize(os.path.join(root, f))
                except:
                    pass
        return total

    def empty_recycle_bin(self):
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000007)
            self.log_message("🗑️ Recycle Bin emptied.")
        except Exception as e:
            self.log_message(f"❌ Recycle Bin: {e}")
    
    def empty_recycle_bin_only(self):
        """Empty only the recycle bin"""
        self.status.setText("🗑️ Emptying Recycle Bin...")
        self.log.clear()
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000007)
            self.log_message("✅ Recycle Bin emptied successfully.")
            self.status.setText("✅ Recycle Bin Emptied")
        except Exception as e:
            self.log_message(f"❌ Error emptying Recycle Bin: {e}")
            self.status.setText("❌ Error emptying Recycle Bin")
    
    # Power Management Methods
    def confirm_action(self, action_name):
        """Show confirmation dialog for power actions"""
        reply = QMessageBox.question(
            self, 
            f'Confirm {action_name}',
            f'Are you sure you want to {action_name.lower()} your computer?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
    
    def shutdown_now(self):
        """Immediate shutdown"""
        if self.confirm_action("Shutdown"):
            try:
                subprocess.run(["shutdown", "/s", "/f", "/t", "0"], check=True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to shutdown: {e}")
    
    def restart_now(self):
        """Immediate restart"""
        if self.confirm_action("Restart"):
            try:
                subprocess.run(["shutdown", "/r", "/f", "/t", "0"], check=True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to restart: {e}")
    
    def sleep_now(self):
        """Put computer to sleep"""
        try:
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to sleep: {e}")
    
    def hibernate_now(self):
        """Hibernate computer"""
        try:
            subprocess.run(["shutdown", "/h"], check=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to hibernate: {e}")
    
    def lock_screen(self):
        """Lock the screen"""
        try:
            ctypes.windll.user32.LockWorkStation()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to lock screen: {e}")
    
    def sign_out(self):
        """Sign out current user"""
        if self.confirm_action("Sign Out"):
            try:
                subprocess.run(["shutdown", "/l"], check=True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to sign out: {e}")
    
    def schedule_shutdown(self):
        """Schedule a shutdown"""
        minutes = self.timer_spinbox.value()
        seconds = minutes * 60
        
        reply = QMessageBox.question(
            self,
            'Schedule Shutdown',
            f'Schedule shutdown in {minutes} minutes?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                subprocess.run(["shutdown", "/s", "/f", "/t", str(seconds)], check=True)
                QMessageBox.information(
                    self, 
                    "Scheduled", 
                    f"Shutdown scheduled in {minutes} minutes.\nUse 'Cancel Scheduled' to abort."
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to schedule shutdown: {e}")
    
    def cancel_scheduled(self):
        """Cancel any scheduled shutdown"""
        try:
            subprocess.run(["shutdown", "/a"], check=True)
            QMessageBox.information(self, "Cancelled", "Scheduled shutdown cancelled.")
        except Exception as e:
            QMessageBox.information(self, "Info", "No scheduled shutdown to cancel.")

    def ensure_admin(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            self.status.setText("❌ Run as Administrator")
            return False
        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("PC Tool")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("PC Tool Suite")
    
    # Create and show the main window
    win = PCToolkit()
    win.show()
    
    sys.exit(app.exec())
