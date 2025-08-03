import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QPushButton,
    QTextEdit,
    QLabel,
    QTabWidget,
    QProgressBar,
    QGroupBox,
    QSpinBox,
    QComboBox,
    QMessageBox,
    QFrame,
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QFont, QDesktopServices, QCursor

from modules.system_monitor import SystemInfoThread, SystemMonitor
from modules.system_cleaner import SystemCleaner
from modules.power_manager import PowerManager
from modules.quick_actions import QuickActions
from ui.themes import ModernDarkTheme


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class PCToolkit(QMainWindow):
    """Main application window for PC Tool - Advanced System Manager."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PC Toolkit Pro - Advanced System Manager")
        self.setGeometry(100, 100, 650, 480)
        self.setMinimumSize(600, 550)
        self.setMaximumSize(800, 800)
        self.setWindowIcon(QIcon(resource_path("icon.ico")))

        self.system_cleaner = SystemCleaner(self.log_message, self.update_status)
        self.power_manager = PowerManager(self)
        self.quick_actions = QuickActions(self)

        ModernDarkTheme.apply_theme(self)

        self.system_thread = SystemInfoThread()
        self.system_thread.info_updated.connect(self.update_system_info)
        self.system_thread.start()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.init_ui(central_widget)

    def init_ui(self, central_widget):
        """Initialize the user interface with tabbed layout."""
        layout = QVBoxLayout(central_widget)

        self.uptime_widget = QWidget()
        uptime_layout = QHBoxLayout(self.uptime_widget)
        uptime_layout.setContentsMargins(15, 8, 15, 8)

        uptime_layout.addWidget(QLabel("PC Up Time :"))
        uptime_layout.addStretch()

        self.uptime_display = QLabel("0 hours 0 mins")
        self.uptime_display.setStyleSheet(
            """
            QLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
                font-weight: normal;
                color: #ffffff;
            }
        """
        )
        uptime_layout.addWidget(self.uptime_display)

        self.uptime_widget.setStyleSheet(
            """
            QWidget {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 5px;
            }
        """
        )

        layout.addWidget(self.uptime_widget)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(ModernDarkTheme.get_tab_style())

        self.create_system_tab()
        self.create_cleaner_tab()
        self.create_power_tab()

        layout.addWidget(self.tabs)

        # Add clickable copyright notice at the bottom
        copyright_label = QLabel(
            "Developed by SSujitX | <a href='https://github.com/SSujitX' style='color: #4a9eff; text-decoration: none;'>github.com/SSujitX</a> | © 2025"
        )
        copyright_label.setStyleSheet(
            """
            QLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 9px;
                color: #666666;
                background-color: transparent;
                border: none;
                padding: 8px;
                margin: 2px;
            }
        """
        )
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_label.setOpenExternalLinks(True)
        copyright_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addWidget(copyright_label)

        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

    def create_system_tab(self):
        """Create the system monitoring tab."""
        system_widget = QWidget()
        layout = QVBoxLayout()

        info_group = QGroupBox("💻 System Information")
        info_layout = QGridLayout()

        self.cpu_label = QLabel("CPU: Loading...")
        self.memory_label = QLabel("Memory: Loading...")
        self.disk_label = QLabel("Disk C: Loading...")

        system_info = SystemMonitor.get_system_info()
        self.os_label = QLabel(f"OS: {system_info['os']}")

        info_layout.addWidget(self.cpu_label, 0, 0)
        info_layout.addWidget(self.memory_label, 1, 0)
        info_layout.addWidget(self.disk_label, 2, 0)
        info_layout.addWidget(self.os_label, 3, 0)

        self.cpu_progress = QProgressBar()
        self.cpu_progress.setStyleSheet(ModernDarkTheme.get_progress_bar_style())
        self.memory_progress = QProgressBar()
        self.memory_progress.setStyleSheet(ModernDarkTheme.get_progress_bar_style())
        self.disk_progress = QProgressBar()
        self.disk_progress.setStyleSheet(ModernDarkTheme.get_progress_bar_style())

        info_layout.addWidget(self.cpu_progress, 0, 1)
        info_layout.addWidget(self.memory_progress, 1, 1)
        info_layout.addWidget(self.disk_progress, 2, 1)

        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        actions_group = QGroupBox("⚡ Quick Actions")
        actions_layout = QGridLayout()

        task_mgr_btn = QPushButton("📊 Task Manager")
        task_mgr_btn.setStyleSheet(ModernDarkTheme.get_button_style("default"))
        task_mgr_btn.clicked.connect(self.quick_actions.open_task_manager)
        actions_layout.addWidget(task_mgr_btn, 0, 0)

        device_mgr_btn = QPushButton("🔧 Device Manager")
        device_mgr_btn.setStyleSheet(ModernDarkTheme.get_button_style("default"))
        device_mgr_btn.clicked.connect(self.quick_actions.open_device_manager)
        actions_layout.addWidget(device_mgr_btn, 0, 1)

        control_panel_btn = QPushButton("⚙️ Control Panel")
        control_panel_btn.setStyleSheet(ModernDarkTheme.get_button_style("default"))
        control_panel_btn.clicked.connect(self.quick_actions.open_control_panel)
        actions_layout.addWidget(control_panel_btn, 0, 2)

        system_info_btn = QPushButton("📋 System Info")
        system_info_btn.setStyleSheet(ModernDarkTheme.get_button_style("default"))
        system_info_btn.clicked.connect(self.quick_actions.open_system_info)
        actions_layout.addWidget(system_info_btn, 1, 0)

        disk_mgmt_btn = QPushButton("💾 Disk Management")
        disk_mgmt_btn.setStyleSheet(ModernDarkTheme.get_button_style("default"))
        disk_mgmt_btn.clicked.connect(self.quick_actions.open_disk_management)
        actions_layout.addWidget(disk_mgmt_btn, 1, 1)

        services_btn = QPushButton("🔧 Services")
        services_btn.setStyleSheet(ModernDarkTheme.get_button_style("default"))
        services_btn.clicked.connect(self.quick_actions.open_services)
        actions_layout.addWidget(services_btn, 1, 2)

        registry_btn = QPushButton("📝 Registry Editor")
        registry_btn.setStyleSheet(ModernDarkTheme.get_button_style("default"))
        registry_btn.clicked.connect(self.quick_actions.open_registry_editor)
        actions_layout.addWidget(registry_btn, 2, 0)

        event_viewer_btn = QPushButton("📊 Event Viewer")
        event_viewer_btn.setStyleSheet(ModernDarkTheme.get_button_style("default"))
        event_viewer_btn.clicked.connect(self.quick_actions.open_event_viewer)
        actions_layout.addWidget(event_viewer_btn, 2, 1)

        cmd_btn = QPushButton("💻 Command Prompt")
        cmd_btn.setStyleSheet(ModernDarkTheme.get_button_style("default"))
        cmd_btn.clicked.connect(self.quick_actions.open_command_prompt)
        actions_layout.addWidget(cmd_btn, 2, 2)

        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)

        layout.addStretch()
        system_widget.setLayout(layout)
        self.tabs.addTab(system_widget, "📊 System")

    def create_cleaner_tab(self):
        """Create the system cleaner tab."""
        cleaner_widget = QWidget()
        layout = QVBoxLayout()

        self.status = QLabel("Ready")
        self.status.setStyleSheet(ModernDarkTheme.get_status_label_style("default"))
        layout.addWidget(self.status)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(120)
        self.log.setStyleSheet(ModernDarkTheme.get_text_edit_style())
        layout.addWidget(self.log)

        clean_group = QGroupBox("🧹 Cleaning Options")
        clean_layout = QVBoxLayout()

        btn1 = QPushButton("🧹 Clean Temp, Prefetch, Recycle Bin")
        btn1.clicked.connect(self.system_cleaner.clean_temp_files)
        btn1.setStyleSheet(ModernDarkTheme.get_button_style("success"))

        btn2 = QPushButton("🧼 Full Disk Cleanup (Drive C)")
        btn2.clicked.connect(self.system_cleaner.run_disk_cleanup)
        btn2.setStyleSheet(ModernDarkTheme.get_button_style("primary"))

        btn3 = QPushButton("🗑️ Empty Recycle Bin Only")
        btn3.clicked.connect(self.system_cleaner.empty_recycle_bin_only)
        btn3.setStyleSheet(ModernDarkTheme.get_button_style("special"))

        clean_layout.addWidget(btn1)
        clean_layout.addWidget(btn2)
        clean_layout.addWidget(btn3)

        clean_group.setLayout(clean_layout)
        layout.addWidget(clean_group)

        layout.addStretch()
        cleaner_widget.setLayout(layout)
        self.tabs.addTab(cleaner_widget, "🧹 Cleaner")

    def create_power_tab(self):
        """Create the power management tab."""
        power_widget = QWidget()
        layout = QVBoxLayout()

        power_group = QGroupBox("⚡ Power Management")
        power_layout = QGridLayout()

        shutdown_btn = QPushButton("🔴 Shutdown Now")
        shutdown_btn.clicked.connect(self.power_manager.shutdown_now)
        shutdown_btn.setStyleSheet(ModernDarkTheme.get_button_style("danger"))

        restart_btn = QPushButton("🔄 Restart Now")
        restart_btn.clicked.connect(self.power_manager.restart_now)
        restart_btn.setStyleSheet(ModernDarkTheme.get_button_style("warning"))

        sleep_btn = QPushButton("😴 Sleep")
        sleep_btn.clicked.connect(self.power_manager.sleep_now)
        sleep_btn.setStyleSheet(ModernDarkTheme.get_button_style("special"))

        hibernate_btn = QPushButton("🛌 Hibernate")
        hibernate_btn.clicked.connect(self.power_manager.hibernate_now)
        hibernate_btn.setStyleSheet(ModernDarkTheme.get_button_style("success"))

        lock_btn = QPushButton("🔒 Lock Screen")
        lock_btn.clicked.connect(self.power_manager.lock_screen)
        lock_btn.setStyleSheet(ModernDarkTheme.get_button_style("default"))

        signout_btn = QPushButton("👤 Sign Out")
        signout_btn.clicked.connect(self.power_manager.sign_out)
        signout_btn.setStyleSheet(ModernDarkTheme.get_button_style("primary"))

        power_layout.addWidget(shutdown_btn, 0, 0)
        power_layout.addWidget(restart_btn, 0, 1)
        power_layout.addWidget(sleep_btn, 1, 0)
        power_layout.addWidget(hibernate_btn, 1, 1)
        power_layout.addWidget(lock_btn, 2, 0)
        power_layout.addWidget(signout_btn, 2, 1)

        power_group.setLayout(power_layout)
        layout.addWidget(power_group)

        scheduled_group = QGroupBox("⏰ Scheduled Actions")
        scheduled_layout = QVBoxLayout()

        timer_layout = QHBoxLayout()

        timer_layout.addWidget(QLabel("Time:"))
        self.timer_spinbox = QSpinBox()
        self.timer_spinbox.setRange(1, 24)
        self.timer_spinbox.setValue(1)
        self.timer_spinbox.setStyleSheet(ModernDarkTheme.get_spinbox_style())
        timer_layout.addWidget(self.timer_spinbox)

        self.time_unit_combo = QComboBox()
        self.time_unit_combo.addItems(["Minutes", "Hours"])
        self.time_unit_combo.setStyleSheet(ModernDarkTheme.get_combobox_style())
        self.time_unit_combo.currentTextChanged.connect(self.update_timer_range)
        timer_layout.addWidget(self.time_unit_combo)

        scheduled_layout.addLayout(timer_layout)

        action_layout = QHBoxLayout()

        scheduled_shutdown_btn = QPushButton("⏰ Schedule Shutdown")
        scheduled_shutdown_btn.clicked.connect(self.schedule_shutdown)
        scheduled_shutdown_btn.setStyleSheet(ModernDarkTheme.get_button_style("danger"))

        cancel_scheduled_btn = QPushButton("❌ Cancel Scheduled")
        cancel_scheduled_btn.clicked.connect(self.power_manager.cancel_scheduled)
        cancel_scheduled_btn.setStyleSheet(ModernDarkTheme.get_button_style("default"))

        action_layout.addWidget(scheduled_shutdown_btn)
        action_layout.addWidget(cancel_scheduled_btn)

        scheduled_layout.addLayout(action_layout)
        scheduled_group.setLayout(scheduled_layout)
        layout.addWidget(scheduled_group)

        warning_label = QLabel(
            "⚠️ Warning: These actions will affect your system immediately!"
        )
        warning_label.setStyleSheet(ModernDarkTheme.get_status_label_style("warning"))
        warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(warning_label)

        layout.addStretch()
        power_widget.setLayout(layout)
        self.tabs.addTab(power_widget, "⚡ Power")

    def update_timer_range(self, unit):
        """Update the timer spinbox range based on selected unit."""
        if unit == "Minutes":
            self.timer_spinbox.setRange(1, 1440)
            self.timer_spinbox.setValue(60)
        else:
            self.timer_spinbox.setRange(1, 24)
            self.timer_spinbox.setValue(1)

    def schedule_shutdown(self):
        """Schedule a shutdown with the selected time and unit."""
        time_value = self.timer_spinbox.value()
        time_unit = self.time_unit_combo.currentText().lower()
        self.power_manager.schedule_shutdown(time_value, time_unit)

    def update_system_info(self, info):
        """Update system information display."""
        try:
            cpu_percent = info["cpu"]
            self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")
            self.cpu_progress.setValue(int(cpu_percent))

            memory_percent = info["memory_percent"]
            memory_used_gb = info["memory_used"] / (1024**3)
            memory_total_gb = info["memory_total"] / (1024**3)
            self.memory_label.setText(
                f"Memory: {memory_used_gb:.1f}GB/{memory_total_gb:.1f}GB ({memory_percent:.1f}%)"
            )
            self.memory_progress.setValue(int(memory_percent))

            disk_percent = info["disk_percent"]
            disk_used_gb = info["disk_used"] / (1024**3)
            disk_total_gb = info["disk_total"] / (1024**3)
            self.disk_label.setText(
                f"Disk C: {disk_used_gb:.1f}GB/{disk_total_gb:.1f}GB ({disk_percent:.1f}%)"
            )
            self.disk_progress.setValue(int(disk_percent))

            uptime_str = info["uptime"]
            self.uptime_display.setText(self.format_uptime(uptime_str))

        except Exception as e:
            pass

    def format_uptime(self, uptime_str):
        """Convert uptime from various formats to '5 days 5 hours 40 mins 2 secs'."""
        try:
            days = 0
            hours = 0
            minutes = 0
            seconds = 0

            # Handle format like "1 day, 5:36:57" or "2 days, 5:36:57"
            if "day" in uptime_str:
                day_part, time_part = uptime_str.split(", ")
                if "days" in day_part:
                    days = int(day_part.split(" ")[0])
                else:  # "day" singular
                    days = 1
                time_str = time_part
            else:
                # Handle format like "5:36:57" (no days)
                time_str = uptime_str

            # Parse the time part (hours:minutes:seconds)
            time_parts = time_str.split(":")
            if len(time_parts) == 3:
                hours, minutes, seconds = map(int, time_parts)

            # Build the result string
            result_parts = []

            if days > 0:
                if days == 1:
                    result_parts.append(f"{days} day")
                else:
                    result_parts.append(f"{days} days")

            if hours > 0:
                if hours == 1:
                    result_parts.append(f"{hours} hour")
                else:
                    result_parts.append(f"{hours} hours")

            if minutes > 0:
                if minutes == 1:
                    result_parts.append(f"{minutes} min")
                else:
                    result_parts.append(f"{minutes} mins")

            if seconds > 0:
                if seconds == 1:
                    result_parts.append(f"{seconds} sec")
                else:
                    result_parts.append(f"{seconds} secs")

            if not result_parts:
                return "Just started"

            return " ".join(result_parts)
        except Exception as e:
            return uptime_str

    def log_message(self, msg):
        """Add a message to the log."""
        self.log.append(msg)
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())

    def update_status(self, msg):
        """Update the status label."""
        self.status.setText(msg)


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
