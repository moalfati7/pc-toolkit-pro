from PyQt6.QtWidgets import QSystemTrayIcon, QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont

from modules.menu_manager import MenuManager
from modules.tray_icon_manager import TrayIconManager
from modules.system_info_manager import SystemInfoManager


class SystemTrayManager(QSystemTrayIcon):
    show_main_window = pyqtSignal()
    quick_shutdown = pyqtSignal()
    quick_restart = pyqtSignal()
    quick_sleep = pyqtSignal()
    quick_lock = pyqtSignal()
    open_task_manager = pyqtSignal()
    open_system_cleaner = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        TrayIconManager.setup_icon(self)

        self.menu_manager = MenuManager(self)
        self.info_manager = SystemInfoManager(self)

        self.setContextMenu(self.menu_manager.create_menu())

        self.tooltip_timer = QTimer()
        self.tooltip_timer.timeout.connect(self.info_manager.update_tooltip)
        self.tooltip_timer.start(2000)

        self.activated.connect(self.on_tray_activated)
        self.setToolTip("PC Toolkit Pro")

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_main_window.emit()

    def update_system_info(self, info):
        self.info_manager.update_system_info(info)

    def show_notification(self, title, message, icon=None, duration=3000):
        if icon is None:
            icon = QSystemTrayIcon.MessageIcon.Information
        self.showMessage(title, message, icon, duration)

    def exit_application(self):
        QApplication.quit()
