import sys
import os
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import Qt


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class TrayIconManager:
    @staticmethod
    def setup_icon(tray_instance):
        try:
            icon_path = resource_path("icon.ico")
            if os.path.exists(icon_path):
                tray_instance.setIcon(QIcon(icon_path))
            else:
                TrayIconManager.create_fallback_icon(tray_instance)
        except Exception:
            TrayIconManager.create_fallback_icon(tray_instance)
    
    @staticmethod
    def create_fallback_icon(tray_instance):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setBrush(Qt.GlobalColor.blue)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawRoundedRect(4, 8, 24, 16, 2, 2)
        painter.drawRoundedRect(12, 24, 8, 4, 1, 1)
        painter.drawLine(8, 28, 24, 28)
        
        painter.end()
        tray_instance.setIcon(QIcon(pixmap))