"""Power management functionality for PC Tool."""

import subprocess
import ctypes
from PyQt6.QtWidgets import QMessageBox


class PowerManager:
    """Handles all power management operations."""
    
    def __init__(self, parent=None):
        self.parent = parent
    
    def confirm_action(self, action_name):
        """Show confirmation dialog for destructive power actions."""
        reply = QMessageBox.question(
            self.parent, 
            f'Confirm {action_name}',
            f'Are you sure you want to {action_name.lower()} your computer?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
    
    def shutdown_now(self):
        """Immediately shutdown the computer."""
        if self.confirm_action("Shutdown"):
            try:
                subprocess.run(["shutdown", "/s", "/f", "/t", "0"], check=True)
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"Failed to shutdown: {e}")
    
    def restart_now(self):
        """Immediately restart the computer."""
        if self.confirm_action("Restart"):
            try:
                subprocess.run(["shutdown", "/r", "/f", "/t", "0"], check=True)
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"Failed to restart: {e}")
    
    def sleep_now(self):
        """Put computer to sleep mode."""
        try:
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True)
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Failed to sleep: {e}")
    
    def hibernate_now(self):
        """Hibernate the computer."""
        try:
            subprocess.run(["shutdown", "/h"], check=True)
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Failed to hibernate: {e}")
    
    def lock_screen(self):
        """Lock the current user session."""
        try:
            ctypes.windll.user32.LockWorkStation()
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Failed to lock screen: {e}")
    
    def sign_out(self):
        """Sign out the current user."""
        if self.confirm_action("Sign Out"):
            try:
                subprocess.run(["shutdown", "/l"], check=True)
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"Failed to sign out: {e}")
    
    def schedule_shutdown(self, time_value, time_unit):
        """Schedule a shutdown after specified time."""
        if time_unit == "Minutes":
            seconds = time_value * 60
            time_text = f"{time_value} minute{'s' if time_value != 1 else ''}"
        else:  # Hours
            seconds = time_value * 3600
            time_text = f"{time_value} hour{'s' if time_value != 1 else ''}"
        
        reply = QMessageBox.question(
            self.parent,
            'Schedule Shutdown',
            f'Schedule shutdown in {time_text}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                subprocess.run(["shutdown", "/s", "/f", "/t", str(seconds)], check=True)
                QMessageBox.information(
                    self.parent, 
                    "Scheduled", 
                    f"Shutdown scheduled in {time_text}.\nUse 'Cancel Scheduled' to abort."
                )
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"Failed to schedule shutdown: {e}")
    
    def cancel_scheduled(self):
        """Cancel any scheduled shutdown operation."""
        try:
            subprocess.run(["shutdown", "/a"], check=True)
            QMessageBox.information(self.parent, "Cancelled", "Scheduled shutdown cancelled.")
        except Exception as e:
            QMessageBox.information(self.parent, "Info", "No scheduled shutdown to cancel.")