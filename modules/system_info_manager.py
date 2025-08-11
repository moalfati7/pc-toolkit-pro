from PyQt6.QtWidgets import QSystemTrayIcon


class SystemInfoManager:
    def __init__(self, tray_instance):
        self.tray = tray_instance
        self.system_info = {}

    def update_system_info(self, info):
        self.system_info = info
        self._update_menu_items(info)

    def _update_menu_items(self, info):
        try:
            # Uptime
            uptime = info.get("uptime", "Unknown")
            uptime_str = self._format_compact_uptime(uptime)
            self.tray.uptime_action.setText(f"⏱️ Uptime: {uptime_str}")
            
            # CPU
            cpu_percent = info.get("cpu", 0)
            self.tray.cpu_action.setText(f"🔥 CPU: {cpu_percent:.1f}%")
            
            # CPU Cores and Threads
            import psutil
            try:
                physical_cores = psutil.cpu_count(logical=False)
                logical_cores = psutil.cpu_count(logical=True)
                self.tray.cpu_cores_action.setText(f"   — {physical_cores} cores | {logical_cores} threads")
            except:
                self.tray.cpu_cores_action.setText("   — Cores: N/A")
            
            # RAM
            memory_percent = info.get("memory_percent", 0)
            memory_used_gb = info.get("memory_used", 0) / (1024**3)
            memory_total_gb = info.get("memory_total", 0) / (1024**3)
            self.tray.memory_action.setText(f"💾 RAM: {memory_percent:.1f}%")
            self.tray.memory_details_action.setText(f"   — Used/Total: {memory_used_gb:.1f}GB | {memory_total_gb:.1f}GB")
            
            # Disk
            disk_percent = info.get("disk_percent", 0)
            disk_used_gb = info.get("disk_used", 0) / (1024**3)
            disk_total_gb = info.get("disk_total", 0) / (1024**3)
            self.tray.disk_action.setText(f"💿 Disk: {disk_percent:.1f}%")
            self.tray.disk_size_action.setText(f"   — Size: {disk_used_gb:.0f}GB | {disk_total_gb:.0f}GB")
            
            # GPU
            if info.get("gpu_available", False):
                gpu_utilization = info.get("gpu_utilization", 0)
                gpu_temp = info.get("gpu_temperature", 0)
                gpu_memory_used = info.get("gpu_memory_used", 0) / 1024  # Convert MB to GB
                gpu_memory_total = info.get("gpu_memory_total", 0) / 1024
                self.tray.gpu_action.setText(f"🎮 GPU: {gpu_utilization:.1f}% | {gpu_temp:.0f}°C")
                self.tray.gpu_details_action.setText(f"   — Memory: {gpu_memory_used:.1f}GB | {gpu_memory_total:.1f}GB")
            else:
                self.tray.gpu_action.setText("🎮 GPU: Not Available")
                self.tray.gpu_details_action.setText("   — Memory: N/A")

        except Exception:
            pass

    def update_tooltip(self):
        if not self.system_info:
            return

        try:
            cpu = self.system_info.get("cpu", 0)
            memory = self.system_info.get("memory_percent", 0)
            disk = self.system_info.get("disk_percent", 0)
            uptime = self.system_info.get("uptime", "Unknown")
            gpu_available = self.system_info.get("gpu_available", False)

            # Format uptime to be more compact
            uptime_formatted = self._format_compact_uptime(uptime)

            # Get additional details
            memory_used_gb = self.system_info.get("memory_used", 0) / (1024**3)
            memory_total_gb = self.system_info.get("memory_total", 0) / (1024**3)

            # Build GPU info if available
            gpu_line = ""
            if gpu_available:
                gpu_util = self.system_info.get("gpu_utilization", 0)
                gpu_temp = self.system_info.get("gpu_temperature", 0)
                gpu_mem_used = (
                    self.system_info.get("gpu_memory_used", 0) / 1024
                )  # Convert MB to GB
                gpu_mem_total = self.system_info.get("gpu_memory_total", 0) / 1024
                gpu_line = f"GPU: {gpu_util:.1f}%/{gpu_mem_total:.1f}GB"
                # gpu_line = f"GPU: {gpu_util:.1f}% | {gpu_temp:.0f}°C | {gpu_mem_used:.1f}/{gpu_mem_total:.1f}GB"

            # Create line-by-line tooltip
            if gpu_available:
                tooltip = f"""PC Toolkit Pro
Uptime: {uptime_formatted}

CPU: {cpu:.1f}%
RAM: {memory:.1f}% ({memory_used_gb:.1f}/{memory_total_gb:.1f}GB)
Disk: {disk:.1f}%
{gpu_line}

Right-click for menu"""
            else:
                tooltip = f"""PC Toolkit Pro
Uptime: {uptime_formatted}

CPU: {cpu:.1f}%
RAM: {memory:.1f}% ({memory_used_gb:.1f}/{memory_total_gb:.1f}GB)
Disk: {disk:.1f}%

Right-click for menu"""

            self.tray.setToolTip(tooltip)
        except Exception:
            self.tray.setToolTip("PC Toolkit Pro")

    def _format_compact_uptime(self, uptime_str):
        """Format uptime to a compact single-line format."""
        try:
            if not uptime_str or uptime_str == "Unknown":
                return "Unknown"

            # Handle format like "1 day, 5:36:57" or "2 days, 5:36:57"
            if "day" in uptime_str:
                if ", " in uptime_str:
                    day_part, time_part = uptime_str.split(", ")
                    if "days" in day_part:
                        days = int(day_part.split(" ")[0])
                    else:  # "day" singular
                        days = 1
                    time_str = time_part
                else:
                    return uptime_str  # Return as-is if format is unexpected
            else:
                # Handle format like "5:36:57" (no days)
                days = 0
                time_str = uptime_str

            # Parse time part (hours:minutes:seconds)
            time_parts = time_str.split(":")
            if len(time_parts) == 3:
                hours = int(time_parts[0])
                minutes = int(time_parts[1])
                seconds = int(time_parts[2])
            else:
                return uptime_str  # Return as-is if format is unexpected

            # Create compact format
            result_parts = []
            if days > 0:
                result_parts.append(f"{days}d")
            if hours > 0:
                result_parts.append(f"{hours}h")
            if minutes > 0:
                result_parts.append(f"{minutes}m")
            if seconds > 0 and days == 0:  # Only show seconds if less than a day
                result_parts.append(f"{seconds}s")

            if not result_parts:
                return "0s"

            return " ".join(result_parts)
        except Exception:
            return uptime_str

    def show_system_info_notification(self):
        if not self.system_info:
            return

        try:
            cpu = self.system_info.get("cpu", 0)
            memory = self.system_info.get("memory_percent", 0)
            disk = self.system_info.get("disk_percent", 0)

            message = f"CPU: {cpu:.1f}% | Memory: {memory:.1f}% | Disk: {disk:.1f}%"

            self.tray.showMessage(
                "PC Toolkit Pro - System Status",
                message,
                QSystemTrayIcon.MessageIcon.Information,
                3000,
            )
        except Exception:
            pass
