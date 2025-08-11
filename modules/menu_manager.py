from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QAction, QFont


class MenuManager:
    def __init__(self, tray_manager):
        self.tray = tray_manager
        self.context_menu = QMenu()
        self._setup_menu_style()
        
    def _setup_menu_style(self):
        self.context_menu.setStyleSheet("""
            QMenu {
                background: #2d3748;
                border: 1px solid #4a5568;
                border-radius: 6px;
                padding: 4px;
                min-width: 180px;
            }
            QMenu::item {
                background: transparent;
                color: #e2e8f0;
                padding: 6px 12px;
                border-radius: 3px;
                margin: 1px;
                font-size: 11px;
                font-weight: normal;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            QMenu::item:selected {
                background: #4299e1;
                color: #ffffff;
            }
            QMenu::separator {
                height: 1px;
                background: #4a5568;
                margin: 2px 8px;
            }
            QMenu::item:disabled {
                color: #718096;
                background: transparent;
            }
        """)
        
    def create_menu(self):
        self.context_menu.clear()
        
        show_action = QAction("🖥️ Show PC Toolkit Pro", self.tray)
        show_action.triggered.connect(self.tray.show_main_window.emit)
        show_action.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.context_menu.addAction(show_action)
        
        self.context_menu.addSeparator()
        
        self._add_power_menu()
        self._add_system_info_menu()
        self._add_quick_actions_menu()
        
        self.context_menu.addSeparator()
        
        exit_action = QAction("❌ Exit PC Toolkit Pro", self.tray)
        exit_action.triggered.connect(self.tray.exit_application)
        exit_action.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.context_menu.addAction(exit_action)
        
        return self.context_menu
    
    def _add_power_menu(self):
        power_menu = self.context_menu.addMenu("⚡ Power Options")
        power_menu.setStyleSheet("""
            QMenu {
                background: #2d3748;
                border: 1px solid #4a5568;
                border-radius: 6px;
                padding: 4px;
                min-width: 160px;
            }
            QMenu::item {
                background: transparent;
                color: #e2e8f0;
                padding: 6px 12px;
                border-radius: 3px;
                margin: 1px;
                font-size: 11px;
                font-weight: normal;
            }
            QMenu::item:selected {
                background: #e53e3e;
                color: #ffffff;
            }
        """)
        
        shutdown_action = QAction("🔴 Shutdown", self.tray)
        shutdown_action.triggered.connect(self.tray.quick_shutdown.emit)
        shutdown_action.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        power_menu.addAction(shutdown_action)
        
        restart_action = QAction("🔄 Restart", self.tray)
        restart_action.triggered.connect(self.tray.quick_restart.emit)
        power_menu.addAction(restart_action)
        
        power_menu.addSeparator()
        
        sleep_action = QAction("😴 Sleep", self.tray)
        sleep_action.triggered.connect(self.tray.quick_sleep.emit)
        power_menu.addAction(sleep_action)
        
        lock_action = QAction("🔒 Lock Screen", self.tray)
        lock_action.triggered.connect(self.tray.quick_lock.emit)
        power_menu.addAction(lock_action)
    
    def _add_system_info_menu(self):
        system_menu = self.context_menu.addMenu("📊 System Info")
        system_menu.setStyleSheet("""
            QMenu {
                background: #2d3748;
                border: 1px solid #4a5568;
                border-radius: 6px;
                padding: 6px;
                min-width: 280px;
            }
            QMenu::item {
                background: transparent;
                color: #e2e8f0;
                padding: 8px 14px;
                border-radius: 3px;
                margin: 1px;
                font-size: 11px;
                font-weight: normal;
            }
            QMenu::item:selected {
                background: #38a169;
                color: #ffffff;
            }
        """)
        
        # Uptime at the top
        self.tray.uptime_action = QAction("⏱️ Uptime: Loading...", self.tray)
        self.tray.uptime_action.setEnabled(False)
        self.tray.uptime_action.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        system_menu.addAction(self.tray.uptime_action)
        
        system_menu.addSeparator()
        
        # CPU with cores info
        self.tray.cpu_action = QAction("🔥 CPU: Loading...", self.tray)
        self.tray.cpu_action.setEnabled(False)
        system_menu.addAction(self.tray.cpu_action)
        
        self.tray.cpu_cores_action = QAction("   Cores: Loading...", self.tray)
        self.tray.cpu_cores_action.setEnabled(False)
        system_menu.addAction(self.tray.cpu_cores_action)
        
        # RAM with detailed info
        self.tray.memory_action = QAction("💾 RAM: Loading...", self.tray)
        self.tray.memory_action.setEnabled(False)
        system_menu.addAction(self.tray.memory_action)
        
        self.tray.memory_details_action = QAction("   Used/Total: Loading...", self.tray)
        self.tray.memory_details_action.setEnabled(False)
        system_menu.addAction(self.tray.memory_details_action)
        
        # Disk with size info
        self.tray.disk_action = QAction("💿 Disk: Loading...", self.tray)
        self.tray.disk_action.setEnabled(False)
        system_menu.addAction(self.tray.disk_action)
        
        self.tray.disk_size_action = QAction("   Size: Loading...", self.tray)
        self.tray.disk_size_action.setEnabled(False)
        system_menu.addAction(self.tray.disk_size_action)
        
        # GPU with detailed info
        self.tray.gpu_action = QAction("🎮 GPU: Checking...", self.tray)
        self.tray.gpu_action.setEnabled(False)
        system_menu.addAction(self.tray.gpu_action)
        
        self.tray.gpu_details_action = QAction("   Memory: Loading...", self.tray)
        self.tray.gpu_details_action.setEnabled(False)
        system_menu.addAction(self.tray.gpu_details_action)
    
    def _add_quick_actions_menu(self):
        quick_menu = self.context_menu.addMenu("⚡ Quick Actions")
        quick_menu.setStyleSheet("""
            QMenu {
                background: #2d3748;
                border: 1px solid #4a5568;
                border-radius: 6px;
                padding: 4px;
                min-width: 160px;
            }
            QMenu::item {
                background: transparent;
                color: #e2e8f0;
                padding: 6px 12px;
                border-radius: 3px;
                margin: 1px;
                font-size: 11px;
                font-weight: normal;
            }
            QMenu::item:selected {
                background: #805ad5;
                color: #ffffff;
            }
        """)
        
        task_manager_action = QAction("📊 Task Manager", self.tray)
        task_manager_action.triggered.connect(self.tray.open_task_manager.emit)
        quick_menu.addAction(task_manager_action)
        
        cleaner_action = QAction("🧹 System Cleaner", self.tray)
        cleaner_action.triggered.connect(self.tray.open_system_cleaner.emit)
        quick_menu.addAction(cleaner_action)