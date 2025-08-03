"""UI themes and styling for PC Tool."""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt


class ModernDarkTheme:
    """Sophisticated dark theme with neon accents and modern effects."""
    
    @staticmethod
    def apply_theme(widget: QWidget):
        """Apply the modern dark theme to the main widget."""
        widget.setStyleSheet("""
            /* Main Window */
            QWidget {
                background-color: #0a0a0f;
                color: #e2e8f0;
                font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                font-size: 9pt;
                font-weight: 400;
            }
            
            /* Group Boxes */
            QGroupBox {
                font-weight: 600;
                font-size: 10pt;
                color: #f1f5f9;
                border: 2px solid #1e293b;
                border-radius: 12px;
                margin-top: 10px;
                padding-top: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(26, 26, 36, 0.8),
                    stop:1 rgba(15, 15, 20, 0.9));
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: #00d4ff;
                font-weight: 700;
                background-color: transparent;
            }
            
            /* Labels */
            QLabel {
                color: #cbd5e0;
                font-weight: 500;
                padding: 2px;
                background-color: transparent;
            }
            
            /* Progress Bars */
            QProgressBar {
                border: 1px solid #334155;
                border-radius: 8px;
                text-align: center;
                font-weight: 600;
                font-size: 9pt;
                color: #e2e8f0;
                background-color: #1e293b;
                min-height: 20px;
            }
            
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:0.5 #0ea5e9, stop:1 #0284c7);
                border-radius: 7px;
                margin: 1px;
            }
            
            /* Text Edit */
            QTextEdit {
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px;
                background-color: #0f172a;
                color: #e2e8f0;
                font-family: 'Consolas', 'SF Mono', 'Monaco', monospace;
                font-size: 8pt;
                selection-background-color: #00d4ff;
                selection-color: #0a0a0f;
            }
            
            QTextEdit:focus {
                border-color: #00d4ff;
            }
            
            /* Spin Box */
            QSpinBox {
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 4px 8px;
                background-color: #1e293b;
                color: #e2e8f0;
                font-weight: 500;
                min-height: 20px;
            }
            
            QSpinBox:focus {
                border-color: #00d4ff;
            }
            
            QSpinBox::up-button, QSpinBox::down-button {
                border: none;
                background-color: #334155;
                border-radius: 3px;
                width: 14px;
            }
            
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #475569;
            }
            
            /* Combo Box */
            QComboBox {
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 4px 8px;
                background-color: #1e293b;
                color: #e2e8f0;
                font-weight: 500;
                min-height: 20px;
            }
            
            QComboBox:focus {
                border-color: #00d4ff;
            }
            
            QComboBox::drop-down {
                border: none;
                background-color: #334155;
                border-radius: 3px;
                width: 18px;
            }
            
            QComboBox::drop-down:hover {
                background-color: #475569;
            }
            
            QComboBox QAbstractItemView {
                border: 1px solid #334155;
                border-radius: 6px;
                background-color: #1e293b;
                selection-background-color: #00d4ff;
                selection-color: #0a0a0f;
            }
        """)
    
    @staticmethod
    def get_tab_style():
        """Get tab widget styling."""
        return """
            QTabWidget::pane {
                border: 1px solid #334155;
                border-radius: 12px;
                background-color: #0f172a;
                margin-top: -1px;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e293b, stop:1 #0f172a);
                border: 1px solid #334155;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 12px 20px;
                margin-right: 2px;
                color: #cbd5e0;
                font-weight: 600;
                font-size: 10pt;
                min-width: 80px;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f172a, stop:1 #1e293b);
                border-color: #00d4ff;
                color: #00d4ff;
                font-weight: 700;
            }
            
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #334155, stop:1 #1e293b);
                border-color: #0ea5e9;
                color: #0ea5e9;
            }
        """
    
    @staticmethod
    def get_button_style(button_type="default"):
        """Get button styling based on type."""
        styles = {
            "default": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #334155, stop:1 #1e293b);
                    border: 1px solid #475569;
                    border-radius: 10px;
                    padding: 12px 20px;
                    font-weight: 600;
                    font-size: 10pt;
                    color: #e2e8f0;
                    min-height: 20px;
                }
                
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #475569, stop:1 #334155);
                    border-color: #00d4ff;
                    color: #00d4ff;
                }
                
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1e293b, stop:1 #0f172a);
                    border-color: #0ea5e9;
                }
            """,
            
            "primary": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #00d4ff, stop:1 #0ea5e9);
                    border: 1px solid #0ea5e9;
                    border-radius: 10px;
                    padding: 12px 20px;
                    font-weight: 700;
                    font-size: 10pt;
                    color: #0a0a0f;
                    min-height: 20px;
                }
                
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #38bdf8, stop:1 #00d4ff);
                    border-color: #00d4ff;
                }
                
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #0ea5e9, stop:1 #0284c7);
                }
            """,
            
            "success": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #10b981, stop:1 #059669);
                    border: 1px solid #059669;
                    border-radius: 10px;
                    padding: 12px 20px;
                    font-weight: 700;
                    font-size: 10pt;
                    color: #0a0a0f;
                    min-height: 20px;
                }
                
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #34d399, stop:1 #10b981);
                    border-color: #10b981;
                }
                
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #059669, stop:1 #047857);
                }
            """,
            
            "warning": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #f59e0b, stop:1 #d97706);
                    border: 1px solid #d97706;
                    border-radius: 10px;
                    padding: 12px 20px;
                    font-weight: 700;
                    font-size: 10pt;
                    color: #0a0a0f;
                    min-height: 20px;
                }
                
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #fbbf24, stop:1 #f59e0b);
                    border-color: #f59e0b;
                }
                
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #d97706, stop:1 #b45309);
                }
            """,
            
            "danger": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #ef4444, stop:1 #dc2626);
                    border: 1px solid #dc2626;
                    border-radius: 10px;
                    padding: 12px 20px;
                    font-weight: 700;
                    font-size: 10pt;
                    color: #ffffff;
                    min-height: 20px;
                }
                
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #f87171, stop:1 #ef4444);
                    border-color: #ef4444;
                }
                
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #dc2626, stop:1 #b91c1c);
                }
            """,
            
            "special": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #8b5cf6, stop:1 #7c3aed);
                    border: 1px solid #7c3aed;
                    border-radius: 10px;
                    padding: 12px 20px;
                    font-weight: 700;
                    font-size: 10pt;
                    color: #ffffff;
                    min-height: 20px;
                }
                
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #a78bfa, stop:1 #8b5cf6);
                    border-color: #8b5cf6;
                }
                
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #7c3aed, stop:1 #6d28d9);
                }
            """
        }
        return styles.get(button_type, styles["default"])
    
    @staticmethod
    def get_status_label_style(status_type="default"):
        """Get status label styling based on type."""
        styles = {
            "default": """
                QLabel {
                    background-color: #1e293b;
                    border: 1px solid #334155;
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-weight: 600;
                    color: #e2e8f0;
                }
            """,
            
            "success": """
                QLabel {
                    background-color: rgba(16, 185, 129, 0.2);
                    border: 1px solid #10b981;
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-weight: 600;
                    color: #34d399;
                }
            """,
            
            "error": """
                QLabel {
                    background-color: rgba(239, 68, 68, 0.2);
                    border: 1px solid #ef4444;
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-weight: 600;
                    color: #f87171;
                }
            """,
            
            "warning": """
                QLabel {
                    background-color: rgba(245, 158, 11, 0.2);
                    border: 1px solid #f59e0b;
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-weight: 600;
                    color: #fbbf24;
                }
            """
        }
        return styles.get(status_type, styles["default"])
    
    @staticmethod
    def get_progress_bar_style():
        """Get progress bar styling."""
        return """
            QProgressBar {
                border: 1px solid #334155;
                border-radius: 8px;
                text-align: center;
                font-weight: 600;
                font-size: 9pt;
                color: #e2e8f0;
                background-color: #1e293b;
                min-height: 20px;
            }
            
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:0.5 #0ea5e9, stop:1 #0284c7);
                border-radius: 7px;
                margin: 1px;
            }
        """
    
    @staticmethod
    def get_text_edit_style():
        """Get text edit styling."""
        return """
            QTextEdit {
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px;
                background-color: #0f172a;
                color: #e2e8f0;
                font-family: 'Consolas', 'SF Mono', 'Monaco', monospace;
                font-size: 8pt;
                selection-background-color: #00d4ff;
                selection-color: #0a0a0f;
            }
            
            QTextEdit:focus {
                border-color: #00d4ff;
            }
        """
    
    @staticmethod
    def get_spinbox_style():
        """Get spinbox styling."""
        return """
            QSpinBox {
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 4px 8px;
                background-color: #1e293b;
                color: #e2e8f0;
                font-weight: 500;
                min-height: 20px;
            }
            
            QSpinBox:focus {
                border-color: #00d4ff;
            }
            
            QSpinBox::up-button, QSpinBox::down-button {
                border: none;
                background-color: #334155;
                border-radius: 3px;
                width: 14px;
            }
            
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #475569;
            }
        """
    
    @staticmethod
    def get_combobox_style():
        """Get combobox styling."""
        return """
            QComboBox {
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 4px 8px;
                background-color: #1e293b;
                color: #e2e8f0;
                font-weight: 500;
                min-height: 20px;
            }
            
            QComboBox:focus {
                border-color: #00d4ff;
            }
            
            QComboBox::drop-down {
                border: none;
                background-color: #334155;
                border-radius: 3px;
                width: 18px;
            }
            
            QComboBox::drop-down:hover {
                background-color: #475569;
            }
            
            QComboBox QAbstractItemView {
                border: 1px solid #334155;
                border-radius: 6px;
                background-color: #1e293b;
                selection-background-color: #00d4ff;
                selection-color: #0a0a0f;
            }
        """

from PyQt6.QtWidgets import QWidget


class ModernLightTheme:
    """Modern light theme with clean white background and professional styling."""
    
    @staticmethod
    def apply_theme(widget: QWidget):
        """Apply the modern light theme to the main widget."""
        widget.setStyleSheet("""
            /* Main Window */
            QWidget {
                background-color: #ffffff;
                color: #2c3e50;
                font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                font-size: 10pt;
                font-weight: 400;
            }
            
            /* Group Boxes */
            QGroupBox {
                font-weight: 600;
                font-size: 11pt;
                color: #34495e;
                border: 2px solid #e8f4fd;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 8px;
                background-color: #f8fbff;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #2980b9;
                font-weight: 700;
                background-color: transparent;
            }
            
            /* Labels */
            QLabel {
                color: #2c3e50;
                font-weight: 500;
                padding: 2px;
                background-color: transparent;
            }
            
            /* Progress Bars */
            QProgressBar {
                border: 2px solid #e8f4fd;
                border-radius: 8px;
                text-align: center;
                font-weight: 600;
                font-size: 9pt;
                color: #2c3e50;
                background-color: #f8fbff;
                min-height: 20px;
            }
            
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:0.5 #2980b9, stop:1 #1abc9c);
                border-radius: 6px;
                margin: 1px;
            }
            
            /* Text Edit */
            QTextEdit {
                border: 2px solid #e8f4fd;
                border-radius: 8px;
                padding: 8px;
                background-color: #ffffff;
                color: #2c3e50;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 9pt;
                selection-background-color: #3498db;
                selection-color: white;
            }
            
            QTextEdit:focus {
                border-color: #3498db;
            }
            
            /* Spin Box */
            QSpinBox {
                border: 2px solid #e8f4fd;
                border-radius: 6px;
                padding: 6px 8px;
                background-color: #ffffff;
                color: #2c3e50;
                font-weight: 500;
                min-height: 20px;
            }
            
            QSpinBox:focus {
                border-color: #3498db;
            }
            
            QSpinBox::up-button, QSpinBox::down-button {
                border: none;
                background-color: #f8fbff;
                border-radius: 3px;
                width: 16px;
            }
            
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #e8f4fd;
            }
            
            /* Combo Box */
            QComboBox {
                border: 2px solid #e8f4fd;
                border-radius: 6px;
                padding: 6px 8px;
                background-color: #ffffff;
                color: #2c3e50;
                font-weight: 500;
                min-height: 20px;
            }
            
            QComboBox:focus {
                border-color: #3498db;
            }
            
            QComboBox::drop-down {
                border: none;
                background-color: #f8fbff;
                border-radius: 3px;
                width: 20px;
            }
            
            QComboBox::drop-down:hover {
                background-color: #e8f4fd;
            }
            
            QComboBox QAbstractItemView {
                border: 2px solid #e8f4fd;
                border-radius: 6px;
                background-color: #ffffff;
                selection-background-color: #3498db;
                selection-color: white;
            }
        """)
    
    @staticmethod
    def get_tab_style():
        """Get tab widget styling."""
        return """
            QTabWidget::pane {
                border: 2px solid #bdc3c7;
                background-color: #ffffff;
                border-radius: 8px;
                margin-top: -1px;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ecf0f1, stop:1 #d5dbdb);
                color: #2c3e50;
                padding: 12px 20px;
                margin-right: 2px;
                border: 2px solid #bdc3c7;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border-bottom: 2px solid #ffffff;
                color: #2980b9;
            }
            
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #ecf0f1);
            }
        """
    
    @staticmethod
    def get_button_style():
        """Get button styling."""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
                color: #2c3e50;
                border: 2px solid #95a5a6;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 10pt;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d5dbdb, stop:1 #95a5a6);
                border: 2px solid #7f8c8d;
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                border: 2px solid #34495e;
            }
        """
    
    @staticmethod
    def get_special_button_style(color_scheme):
        """Get special button styling for specific actions."""
        colors = {
            'danger': {
                'normal': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e74c3c, stop:1 #c0392b)',
                'hover': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #c0392b, stop:1 #a93226)',
                'pressed': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a93226, stop:1 #922b21)',
                'border': '#a93226'
            },
            'warning': {
                'normal': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f39c12, stop:1 #e67e22)',
                'hover': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e67e22, stop:1 #d35400)',
                'pressed': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d35400, stop:1 #ba4a00)',
                'border': '#d35400'
            },
            'success': {
                'normal': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #27ae60, stop:1 #229954)',
                'hover': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #229954, stop:1 #1e8449)',
                'pressed': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1e8449, stop:1 #196f3d)',
                'border': '#1e8449'
            },
            'info': {
                'normal': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3498db, stop:1 #2980b9)',
                'hover': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2980b9, stop:1 #2471a3)',
                'pressed': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2471a3, stop:1 #1f618d)',
                'border': '#2471a3'
            },
            'recycle': {
                'normal': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8e44ad, stop:1 #7d3c98)',
                'hover': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7d3c98, stop:1 #6c3483)',
                'pressed': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6c3483, stop:1 #5b2c6f)',
                'border': '#6c3483'
            }
        }
        
        scheme = colors.get(color_scheme, colors['info'])
        
        return f"""
            QPushButton {{
                background: {scheme['normal']};
                color: #ffffff;
                border: 2px solid {scheme['border']};
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 10pt;
            }}
            
            QPushButton:hover {{
                background: {scheme['hover']};
            }}
            
            QPushButton:pressed {{
                background: {scheme['pressed']};
            }}
        """