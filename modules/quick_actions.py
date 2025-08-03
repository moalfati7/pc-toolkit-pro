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
    
    def open_volume_mixer(self):
        """Open Windows Volume Mixer."""
        try:
            subprocess.Popen("sndvol", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Volume Mixer: {e}")
    
    def open_calculator(self):
        """Open Windows Calculator."""
        try:
            subprocess.Popen("calc", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Calculator: {e}")
    
    def open_notepad(self):
        """Open Windows Notepad."""
        try:
            subprocess.Popen("notepad", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Notepad: {e}")
    
    def open_paint(self):
        """Open Windows Paint."""
        try:
            subprocess.Popen("mspaint", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Paint: {e}")
    
    def open_snipping_tool(self):
        """Open Windows Snipping Tool."""
        try:
            subprocess.Popen("snippingtool", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Snipping Tool: {e}")
    
    def open_character_map(self):
        """Open Windows Character Map."""
        try:
            subprocess.Popen("charmap", shell=True)
        except Exception as e:
            self.show_error("Error", f"Failed to open Character Map: {e}")