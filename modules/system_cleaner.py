"""System cleaning functionality for PC Tool."""

import os
import shutil
import ctypes
import subprocess
import humanize


class SystemCleaner:
    """Handles all system cleaning operations."""
    
    def __init__(self, log_callback=None, status_callback=None):
        self.log_callback = log_callback
        self.status_callback = status_callback
    
    def log_message(self, message):
        """Log a message if callback is available."""
        if self.log_callback:
            self.log_callback(message)
    
    def update_status(self, status):
        """Update status if callback is available."""
        if self.status_callback:
            self.status_callback(status)
    
    def ensure_admin(self):
        """Check if running with administrator privileges."""
        if not ctypes.windll.shell32.IsUserAnAdmin():
            self.update_status("❌ Run as Administrator")
            return False
        return True
    
    def get_directory_size(self, path):
        """Calculate total size of directory."""
        total = 0
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    try:
                        total += os.path.getsize(os.path.join(root, file))
                    except (OSError, IOError):
                        pass
        except (OSError, IOError):
            pass
        return total
    
    def empty_recycle_bin(self):
        """Empty the Windows recycle bin."""
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000007)
            self.log_message("🗑️ Recycle Bin emptied.")
        except Exception as e:
            self.log_message(f"❌ Recycle Bin: {e}")
    
    def empty_recycle_bin_only(self):
        """Empty only the recycle bin with status updates."""
        self.update_status("🗑️ Emptying Recycle Bin...")
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000007)
            self.log_message("✅ Recycle Bin emptied successfully.")
            self.update_status("✅ Recycle Bin Emptied")
        except Exception as e:
            self.log_message(f"❌ Error emptying Recycle Bin: {e}")
            self.update_status("❌ Error emptying Recycle Bin")
    
    def clean_temp_files(self):
        """Clean temporary files, prefetch, and recycle bin."""
        if not self.ensure_admin():
            return
        
        self.update_status("🧹 Cleaning...")
        
        # Comprehensive list of temp directories to clean
        folders = [
            os.getenv("TEMP"),                    # Current user's temp directory (auto-detected)
            os.getenv("TMP"),                     # Alternative user temp (auto-detected)
            r"C:\Windows\Temp",                   # System temp directory
            r"C:\Windows\Prefetch",               # Windows prefetch files
            os.path.expandvars(r"%USERPROFILE%\AppData\Local\Temp"),  # User temp via profile variable
        ]
        
        # Remove duplicates and None values
        folders = list(set(filter(None, folders)))
        
        total_size = 0
        cleaned_count = 0
        
        for folder in folders:
            if not os.path.exists(folder):
                self.log_message(f"⚠️ Directory not found: {folder}")
                continue
            
            self.log_message(f"🧹 Cleaning: {folder}")
            folder_size = 0
            folder_count = 0
            
            try:
                items = os.listdir(folder)
                for item in items:
                    full_path = os.path.join(folder, item)
                    try:
                        if os.path.isfile(full_path):
                            size = os.path.getsize(full_path)
                            os.remove(full_path)
                            folder_size += size
                            folder_count += 1
                        elif os.path.isdir(full_path):
                            size = self.get_directory_size(full_path)
                            shutil.rmtree(full_path, ignore_errors=True)
                            folder_size += size
                            folder_count += 1
                    except Exception as e:
                        self.log_message(f"✖ {item}: {str(e)[:50]}...")
                
                if folder_count > 0:
                    folder_readable = humanize.naturalsize(folder_size, binary=True)
                    self.log_message(f"✅ {folder}: {folder_count} items, {folder_readable}")
                    total_size += folder_size
                    cleaned_count += folder_count
                else:
                    self.log_message(f"✅ {folder}: Already clean")
                    
            except PermissionError:
                self.log_message(f"❌ Access denied: {folder}")
            except Exception as e:
                self.log_message(f"❌ Error accessing {folder}: {e}")
        
        # Empty recycle bin
        self.empty_recycle_bin()
        
        # Final status update
        human_readable = humanize.naturalsize(total_size, binary=True)
        self.log_message(f"🎉 Cleanup complete: {cleaned_count} items removed, {human_readable} freed")
        self.update_status(f"✅ Cleaned: {human_readable} ({cleaned_count} items)")
    
    def run_disk_cleanup(self):
        """Launch Windows Disk Cleanup utility."""
        if not self.ensure_admin():
            return
        
        self.update_status("🧼 Running full Disk Cleanup...")
        self.log_message("Launching: cleanmgr /sagerun:1337")
        try:
            subprocess.Popen("cleanmgr /sagerun:1337", shell=True)
        except Exception as e:
            self.log_message(f"Error running disk cleanup: {e}")