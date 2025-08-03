# 🚀 PC Toolkit Pro - Advanced Windows System Manager

<div align="center">

![PC Toolkit Pro](https://img.shields.io/badge/PC%20Toolkit%20Pro-v2.0-blue?style=for-the-badge&logo=windows)
![Python](https://img.shields.io/badge/Python-3.11+-green?style=for-the-badge&logo=python)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-orange?style=for-the-badge&logo=qt)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-lightblue?style=for-the-badge&logo=windows)

**🔧 The Ultimate Windows System Management Tool with Modern GUI**

_Clean • Monitor • Optimize • Control_

## [![Download](https://img.shields.io/badge/Download-success?style=for-the-badge&logo=download)](https://github.com/SSujitX/pc-toolkit-pro/releases)

---

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-features)

</div>

---

## ⚠️ **Important: First Run**

> **🔑 Administrator Rights Required**  
> For full functionality (especially system cleaning features), **right-click** the application and select **"Run as administrator"** on your first launch. The application will automatically prompt for UAC elevation when needed.

---

## 🌟 Overview

**PC Toolkit Pro** is the ultimate Windows system optimizer and cleaner that transforms your PC performance with advanced system cleaning, real-time monitoring, and smart power management. This free Windows utility combines disk cleanup, temp file removal, memory optimization, and CPU monitoring in one powerful desktop application. Built with modern PyQt6 technology, PC Toolkit Pro delivers professional-grade system maintenance tools for Windows 10/11 users who demand peak performance, enhanced security, and streamlined PC management in an intuitive, user-friendly interface.

### 🎯 Why Choose PC Toolkit Pro?

- ⚡ **Lightning Fast**: Optimized performance with real-time monitoring
- 🎨 **Modern UI**: Beautiful dark theme with professional design
- 🔒 **Safe & Secure**: Built-in safety checks and confirmations
- 🛠️ **All-in-One**: System cleaning, monitoring, and power management
- 📊 **Real-time Data**: Live system metrics and performance tracking
- 🎛️ **Advanced Controls**: Quick access to Windows system tools

---

## ✨ Features

### 🧹 **Advanced System Cleaner**

| Feature                         | Description                                       | Benefits                                    |
| ------------------------------- | ------------------------------------------------- | ------------------------------------------- |
| 🗑️ **Smart Temp Cleanup**       | Removes temporary files, prefetch data, and cache | Frees up disk space, improves performance   |
| 🔄 **Disk Cleanup Integration** | Full Windows Disk Cleanup with advanced options   | Deep system cleaning with Microsoft tools   |
| ♻️ **Recycle Bin Manager**      | Individual or bulk recycle bin cleaning           | Quick space recovery and privacy protection |
| 📊 **Real-time Progress**       | Live cleaning progress with file size reporting   | Transparent operation tracking              |
| 📝 **Detailed Logging**         | Comprehensive logs of all cleaning operations     | Audit trail and troubleshooting support     |

### 📊 **Real-time System Monitor**

| Metric               | Monitoring                         | Visualization                           |
| -------------------- | ---------------------------------- | --------------------------------------- |
| 🖥️ **CPU Usage**     | Real-time processor utilization    | Animated progress bars with percentages |
| 💾 **Memory Stats**  | RAM usage (used/total/percentage)  | Live memory consumption tracking        |
| 💿 **Disk Space**    | C: drive storage monitoring        | Space usage with GB/TB display          |
| ⏱️ **System Uptime** | Precise uptime tracking            | Days, hours, minutes, seconds format    |
| 🖥️ **System Info**   | OS version, architecture details   | Complete system specifications          |
| 🔧 **Quick Tools**   | Direct access to Windows utilities | One-click system tool launching         |

### ⚡ **Power Management Suite**

#### 🚨 **Immediate Actions**

- 🔴 **Shutdown Now** - Instant system shutdown with confirmation
- 🔄 **Restart Now** - Quick system restart with safety checks
- 😴 **Sleep Mode** - Low-power standby mode
- 🛌 **Hibernate** - Save session to disk and power off
- 🔒 **Lock Screen** - Secure workstation instantly
- 👤 **Sign Out** - Log out current user safely

#### ⏰ **Scheduled Operations**

- 📅 **Flexible Scheduling** - Set shutdown timers (1-1440 minutes)
- ⏱️ **Multiple Time Units** - Minutes or hours selection
- ❌ **Cancel Anytime** - Abort scheduled operations
- 🔔 **Smart Notifications** - System tray alerts and confirmations

### 🎨 **Premium User Interface**

- 🌙 **Modern Dark Theme** - Professional dark mode with gradient accents
- 🎭 **Responsive Design** - Adaptive layout for different screen sizes
- 🎨 **Color-coded Elements** - Intuitive color system for different actions
- ✨ **Smooth Animations** - Polished transitions and hover effects
- 📱 **Tabbed Interface** - Organized feature access with clean navigation
- 🔤 **Premium Typography** - Segoe UI font family for Windows consistency

---

## 🚀 Quick Start

### 📋 **Prerequisites**

- **Operating System**: Windows 10/11 (64-bit recommended)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 1GB free space
- **Permissions**: Administrator rights (recommended)

### 📥 **Installation**

#### **Method 1: Using UV (Recommended)**

```bash
# Clone the repository
git clone https://github.com/yourusername/pc-toolkit-pro.git
cd pc-toolkit-pro

# Install dependencies with UV
uv sync

# Run the application
uv run pc_toolkit_pro.py
```

#### **Method 2: Using Pip**

```bash
# Clone the repository
git clone https://github.com/yourusername/pc-toolkit-pro.git
cd pc-toolkit-pro

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python pc_toolkit_pro.py
```

#### **Method 3: Direct Download**

1. Download the latest release from [Release](https://github.com/SSujitX/pc-toolkit-pro/releases)
2. Extract the ZIP file
3. Run `PC-Toolkit-Pro.exe` (no installation required)

---

## 🛠️ Building Executable

### **Create Standalone EXE**

```bash
# Install PyInstaller
uv add pyinstaller

# Build executable with icon
uv run python -m PyInstaller --noconfirm --windowed --onefile --icon "icon.ico" --add-data "icon.ico;." --name "PC-Toolkit-Pro" pc_toolkit_pro.py

# Find your executable in dist/ folder
```

### **Advanced Build Options**

```bash
# Build with additional optimizations
uv run python -m pyinstaller --noconfirm --windowed --onefile --icon "icon.ico" --add-data "icon.ico;." --add-data "ui;ui" --add-data "modules;modules" --name "PC-Toolkit-Pro" --optimize 2 --strip pc_toolkit_pro.py
```

---

## 📖 Usage Guide

### 🖥️ **System Monitor Tab**

1. **Real-time Metrics**: View live CPU, memory, and disk usage
2. **System Information**: Check OS details and hardware specs
3. **Quick Tools**: Access Windows utilities with one click
4. **Performance Tracking**: Monitor system health over time

### 🧹 **System Cleaner Tab**

1. **Select Cleaning Type**: Choose from three cleaning options
2. **Monitor Progress**: Watch real-time cleaning progress
3. **Review Logs**: Check detailed cleaning reports
4. **Verify Results**: See freed space and cleaned files

### ⚡ **Power Management Tab**

1. **Immediate Actions**: Use instant power controls
2. **Schedule Operations**: Set timed shutdowns
3. **Safety Confirmations**: Confirm destructive actions
4. **Cancel Scheduled**: Abort pending operations

---

## 🔧 Configuration

### **System Requirements**

| Component | Minimum    | Recommended |
| --------- | ---------- | ----------- |
| **OS**    | Windows 10 | Windows 11  |

### **Permissions**

- **Standard User**: Basic monitoring and power functions
- **Administrator**: Full cleaning capabilities and system access
- **UAC**: Automatic elevation prompts for protected operations

---

## 🛡️ Security & Safety

### **Built-in Protections**

- ✅ **Confirmation Dialogs** - Prevent accidental destructive actions
- ✅ **Safe File Deletion** - Only removes temporary and cache files
- ✅ **System File Protection** - Avoids critical Windows files
- ✅ **Backup Recommendations** - Suggests data backup before cleaning
- ✅ **Error Handling** - Graceful failure recovery

### **Best Practices**

1. **Run as Administrator** for full functionality
2. **Close Important Applications** before power operations
3. **Save Work** before using shutdown features
4. **Regular Monitoring** for optimal system health
5. **Backup Data** before major cleaning operations

---

## 🔗 Dependencies

### **Core Libraries**

```python
PyQt6>=6.9.1          # Modern GUI framework
psutil>=7.0.0          # System monitoring and process management
humanize>=4.12.3        # Human-readable file sizes and numbers
```

---

## 🤝 Contributing

### **How to Contribute**

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## 📊 Project Stats

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/yourusername/pc-toolkit-pro?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/pc-toolkit-pro?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/pc-toolkit-pro)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/pc-toolkit-pro)
![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/pc-toolkit-pro)

</div>

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **PyQt6 Team** - For the excellent GUI framework
- **psutil Contributors** - For system monitoring capabilities
- **Windows Community** - For feedback and testing
- **Open Source Community** - For inspiration and support

---

## 📞 Support

### **Get Help**

- 🐛 **Issues**: [GitHub Issues](https://github.com/SSujitX/pc-toolkit-pro/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/SSujitX/pc-toolkit-pro/discussions)
- 📖 **Wiki**: [Project Wiki](https://github.com/SSujitX/pc-toolkit-pro/wiki)

### **Stay Updated**

- ⭐ **Star** this repository for updates
- 👀 **Watch** for new releases
- 🔔 **Follow** for announcements

---

<div align="center">

**Made with ❤️ for the Windows Community**

_PC Toolkit Pro - Empowering Windows Users Since 2025_

[⬆️ Back to Top](#-pc-toolkit-pro---advanced-windows-system-manager)

</div>
