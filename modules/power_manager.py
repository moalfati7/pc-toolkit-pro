"""Power management functionality for PC Tool."""

import subprocess
import ctypes
from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class MinimalConfirmDialog(QDialog):
    """Minimal confirmation dialog with dark theme styling."""
    
    def __init__(self, parent, title, message, confirm_text="Yes", cancel_text="No"):
        super().__init__(parent)
        self.result = False
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(320, 140)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                border: 2px solid #334155;
                border-radius: 12px;
            }
            QLabel {
                color: #e2e8f0;
                font-family: 'Segoe UI';
                font-size: 11pt;
                font-weight: 500;
                background-color: transparent;
                padding: 8px;
            }
            QPushButton {
                border: 1px solid #475569;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 10pt;
                min-width: 60px;
                min-height: 24px;
            }
            QPushButton#confirmBtn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ef4444, stop:1 #dc2626);
                border-color: #dc2626;
                color: #ffffff;
            }
            QPushButton#confirmBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f87171, stop:1 #ef4444);
            }
            QPushButton#cancelBtn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #334155, stop:1 #1e293b);
                border-color: #475569;
                color: #e2e8f0;
            }
            QPushButton#cancelBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #475569, stop:1 #334155);
                border-color: #00d4ff;
                color: #00d4ff;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Message label
        msg_label = QLabel(message)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setWordWrap(True)
        layout.addWidget(msg_label)
        
        # Button layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        # Cancel button
        cancel_btn = QPushButton(cancel_text)
        cancel_btn.setObjectName("cancelBtn")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        # Confirm button
        confirm_btn = QPushButton(confirm_text)
        confirm_btn.setObjectName("confirmBtn")
        confirm_btn.clicked.connect(self.accept)
        btn_layout.addWidget(confirm_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        # Set focus to cancel button by default
        cancel_btn.setFocus()
    
    def accept(self):
        self.result = True
        super().accept()
    
    def reject(self):
        self.result = False
        super().reject()


class MinimalInfoDialog(QDialog):
    """Minimal info dialog with dark theme styling."""
    
    def __init__(self, parent, title, message, dialog_type="info"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(300, 120)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        
        # Color scheme based on dialog type
        if dialog_type == "error":
            border_color = "#ef4444"
            btn_color = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ef4444, stop:1 #dc2626);"
            btn_hover = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f87171, stop:1 #ef4444);"
        elif dialog_type == "success":
            border_color = "#10b981"
            btn_color = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #10b981, stop:1 #059669);"
            btn_hover = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #34d399, stop:1 #10b981);"
        else:  # info
            border_color = "#00d4ff"
            btn_color = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00d4ff, stop:1 #0ea5e9);"
            btn_hover = "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #38bdf8, stop:1 #00d4ff);"
        
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #0f172a;
                border: 2px solid {border_color};
                border-radius: 12px;
            }}
            QLabel {{
                color: #e2e8f0;
                font-family: 'Segoe UI';
                font-size: 11pt;
                font-weight: 500;
                background-color: transparent;
                padding: 8px;
            }}
            QPushButton {{
                {btn_color}
                border: 1px solid {border_color};
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 10pt;
                color: #ffffff;
                min-width: 60px;
                min-height: 24px;
            }}
            QPushButton:hover {{
                {btn_hover}
            }}
        """)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Message label
        msg_label = QLabel(message)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setWordWrap(True)
        layout.addWidget(msg_label)
        
        # OK button
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(ok_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        ok_btn.setFocus()


class PowerManager:
    """Handles all power management operations."""

    def __init__(self, parent=None):
        self.parent = parent

    def confirm_action(self, action_name):
        """Show minimal confirmation dialog for destructive power actions."""
        dialog = MinimalConfirmDialog(
            self.parent,
            f"Confirm {action_name}",
            f"Are you sure you want to {action_name.lower()} your computer?"
        )
        dialog.exec()
        return dialog.result

    def shutdown_now(self):
        """Immediately shutdown the computer."""
        if self.confirm_action("Shutdown"):
            try:
                subprocess.run(["shutdown", "/s", "/f", "/t", "0"], check=True)
            except Exception as e:
                dialog = MinimalInfoDialog(self.parent, "Error", f"Failed to shutdown: {e}", "error")
                dialog.exec()

    def restart_now(self):
        """Immediately restart the computer."""
        if self.confirm_action("Restart"):
            try:
                subprocess.run(["shutdown", "/r", "/f", "/t", "0"], check=True)
            except Exception as e:
                dialog = MinimalInfoDialog(self.parent, "Error", f"Failed to restart: {e}", "error")
                dialog.exec()

    def sleep_now(self):
        """Put computer to sleep mode."""
        try:
            subprocess.run(
                ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True
            )
        except Exception as e:
            dialog = MinimalInfoDialog(self.parent, "Error", f"Failed to sleep: {e}", "error")
            dialog.exec()

    def hibernate_now(self):
        """Hibernate the computer."""
        try:
            subprocess.run(["shutdown", "/h"], check=True)
        except Exception as e:
            dialog = MinimalInfoDialog(self.parent, "Error", f"Failed to hibernate: {e}", "error")
            dialog.exec()

    def lock_screen(self):
        """Lock the current user session."""
        try:
            ctypes.windll.user32.LockWorkStation()
        except Exception as e:
            dialog = MinimalInfoDialog(self.parent, "Error", f"Failed to lock screen: {e}", "error")
            dialog.exec()

    def sign_out(self):
        """Sign out the current user."""
        if self.confirm_action("Sign Out"):
            try:
                subprocess.run(["shutdown", "/l"], check=True)
            except Exception as e:
                dialog = MinimalInfoDialog(self.parent, "Error", f"Failed to sign out: {e}", "error")
                dialog.exec()

    def schedule_shutdown(self, time_value, time_unit):
        """Schedule a shutdown after specified time."""
        if time_unit == "Minutes":
            seconds = time_value * 60
            time_text = f"{time_value} minute{'s' if time_value != 1 else ''}"
        else:  # Hours
            seconds = time_value * 3600
            time_text = f"{time_value} hour{'s' if time_value != 1 else ''}"

        dialog = MinimalConfirmDialog(
            self.parent,
            "Schedule Shutdown",
            f"Schedule shutdown in {time_text}?",
            "Schedule",
            "Cancel"
        )
        dialog.exec()

        if dialog.result:
            try:
                subprocess.run(["shutdown", "/s", "/f", "/t", str(seconds)], check=True)
                dialog = MinimalInfoDialog(
                    self.parent,
                    "Scheduled",
                    f"Shutdown scheduled in {time_text}.\nUse 'Cancel Scheduled' to abort.",
                    "success"
                )
                dialog.exec()
            except Exception as e:
                dialog = MinimalInfoDialog(
                    self.parent, "Error", f"Failed to schedule shutdown: {e}", "error"
                )
                dialog.exec()

    def cancel_scheduled(self):
        """Cancel any scheduled shutdown operation."""
        try:
            subprocess.run(["shutdown", "/a"], check=True)
            dialog = MinimalInfoDialog(
                self.parent, "Cancelled", "Scheduled shutdown cancelled.", "success"
            )
            dialog.exec()
        except Exception as e:
            dialog = MinimalInfoDialog(
                self.parent, "Info", "No scheduled shutdown to cancel."
            )
            dialog.exec()
