"""Quick actions functionality for PC Tool."""

import subprocess
import os
from PyQt6.QtWidgets import QMessageBox


class QuickActions:
    """Handles quick system utility actions."""
    
    def __init__(self, parent=None):
        self.parent = parent
    
    def show_error(self, title, message):
        """Show error message dialog."""
        if self.parent:
            QMessageBox.critical(self.parent, title, message)
    
    def open_task_manager(self):
        """Open Windows Task Manager."""
        try:
            subprocess.Popen("taskmgr", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Task Manager: {e}")
    
    def open_device_manager(self):
        """Open Windows Device Manager."""
        try:
            subprocess.Popen("devmgmt.msc", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Device Manager: {e}")
    
    def open_control_panel(self):
        """Open Windows Control Panel."""
        try:
            subprocess.Popen("control", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Control Panel: {e}")
    
    def open_system_info(self):
        """Open Windows System Information."""
        try:
            subprocess.Popen("msinfo32", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open System Information: {e}")
    
    def open_disk_management(self):
        """Open Windows Disk Management."""
        try:
            subprocess.Popen("diskmgmt.msc", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Disk Management: {e}")
    
    def open_services(self):
        """Open Windows Services."""
        try:
            subprocess.Popen("services.msc", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Services: {e}")
    
    def open_registry_editor(self):
        """Open Windows Registry Editor."""
        try:
            subprocess.Popen("regedit", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Registry Editor: {e}")
    
    def open_event_viewer(self):
        """Open Windows Event Viewer."""
        try:
            subprocess.Popen("eventvwr.msc", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Event Viewer: {e}")
    
    def open_command_prompt(self):
        """Open Command Prompt as Administrator."""
        try:
            subprocess.Popen("powershell Start-Process cmd -Verb RunAs", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Command Prompt: {e}")
    
    def open_powershell(self):
        """Open PowerShell as Administrator."""
        try:
            subprocess.Popen("powershell Start-Process powershell -Verb RunAs", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open PowerShell: {e}")
    
    def open_file_explorer(self):
        """Open Windows File Explorer."""
        try:
            subprocess.Popen("explorer", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open File Explorer: {e}")
    
    def open_network_connections(self):
        """Open Network Connections."""
        try:
            subprocess.Popen("ncpa.cpl", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Network Connections: {e}")