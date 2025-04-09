# Qtのテキストに色付きのログをだしたい
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of using logkiss with Qt text widgets.
This example shows how to output colored logs to a Qt text widget.
"""

import sys
import logging
import logkiss
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QColor, QTextCharFormat, QBrush, QFont
from PyQt5.QtCore import Qt


class QtTextEditHandler(logging.Handler):
    """
    Custom logging handler that outputs log messages to a QTextEdit widget with colors.
    Supports light and dark themes.
    """
    def __init__(self, text_edit, theme="light"):
        super().__init__()
        self.text_edit = text_edit
        self.formatter = logkiss.ColoredFormatter()
        self.theme = theme
        self.set_theme(theme)
    
    def set_theme(self, theme):
        """
        Set color theme (light or dark)
        """
        self.theme = theme
        if theme == "light":
            self.text_edit.setStyleSheet("background-color: white; color: black;")
            # Colors for light theme (darker colors for better visibility)
            self.level_colors = {
                logging.DEBUG: QColor(0, 130, 130),   # dark cyan
                logging.INFO: QColor(0, 0, 0),        # black
                logging.WARNING: QColor(180, 90, 0),   # dark orange
                logging.ERROR: QColor(200, 0, 0),      # dark red
                logging.CRITICAL: QColor(200, 0, 0),   # dark red (with background)
            }
            self.level_backgrounds = {
                logging.CRITICAL: QColor(255, 210, 210),  # light red background
            }
        else:  # dark theme
            self.text_edit.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0;")
            # Colors for dark theme (brighter colors)
            self.level_colors = {
                logging.DEBUG: QColor(0, 255, 255),      # cyan
                logging.INFO: QColor(255, 255, 255),     # white
                logging.WARNING: QColor(255, 255, 0),    # yellow
                logging.ERROR: QColor(255, 100, 100),    # light red
                logging.CRITICAL: QColor(255, 100, 100), # light red (with background)
            }
            self.level_backgrounds = {
                logging.CRITICAL: QColor(100, 0, 0),     # dark red background
            }
        
        # Font styles are the same for both themes
        self.level_styles = {
            logging.WARNING: QFont.Bold,
            logging.ERROR: QFont.Bold,
            logging.CRITICAL: QFont.Bold,
        }

    def emit(self, record):
        """
        Emit a log record to the QTextEdit widget with color formatting.
        """
        # Get formatted message
        msg = self.format(record)
        
        # Create text format
        text_format = QTextCharFormat()
        text_format.setForeground(QBrush(self.level_colors.get(record.levelno, QColor(255, 255, 255))))
        
        # Apply background color if specified for the level
        if record.levelno in self.level_backgrounds:
            text_format.setBackground(QBrush(self.level_backgrounds[record.levelno]))
        
        # Apply font style if specified for the level
        if record.levelno in self.level_styles:
            font = text_format.font()
            font.setWeight(self.level_styles[record.levelno])
            text_format.setFont(font)
        
        # Insert text with formatting
        cursor = self.text_edit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(msg + '\n', text_format)
        
        # Auto-scroll to bottom
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()


class LoggingDemo(QMainWindow):
    """
    Demo application showing colored logs in a Qt text widget.
    """
    def __init__(self):
        super().__init__()
        self.current_theme = "light"  # Default to light theme
        self.init_ui()
        self.setup_logger()
        
    def init_ui(self):
        """Initialize the UI components."""
        self.setWindowTitle('Logkiss Qt Colored Logging Demo')
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create text edit for logs
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setFont(QFont("Courier New", 10))
        layout.addWidget(self.log_text_edit)
        
        # Create buttons for different log levels
        self.debug_button = QPushButton('Log DEBUG')
        self.debug_button.clicked.connect(lambda: self.logger.debug("これはDEBUGメッセージです"))
        layout.addWidget(self.debug_button)
        
        self.info_button = QPushButton('Log INFO')
        self.info_button.clicked.connect(lambda: self.logger.info("これはINFOメッセージです"))
        layout.addWidget(self.info_button)
        
        self.warning_button = QPushButton('Log WARNING')
        self.warning_button.clicked.connect(lambda: self.logger.warning("これはWARNINGメッセージです"))
        layout.addWidget(self.warning_button)
        
        self.error_button = QPushButton('Log ERROR')
        self.error_button.clicked.connect(lambda: self.logger.error("これはERRORメッセージです"))
        layout.addWidget(self.error_button)
        
        self.critical_button = QPushButton('Log CRITICAL')
        self.critical_button.clicked.connect(lambda: self.logger.critical("これはCRITICALメッセージです"))
        layout.addWidget(self.critical_button)
        
        # Create button for structured logging
        self.structured_button = QPushButton('Log Structured Data')
        self.structured_button.clicked.connect(self.log_structured_data)
        layout.addWidget(self.structured_button)
        
        # Create theme toggle button
        self.theme_button = QPushButton('Switch to Dark Theme')
        self.theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_button)
        
    def setup_logger(self):
        """Set up the logger with our custom handler."""
        # Get logger
        self.logger = logkiss.getLogger("qtdemo")
        self.logger.setLevel(logging.DEBUG)
        
        # Create custom handler for QTextEdit with theme
        self.qt_handler = QtTextEditHandler(self.log_text_edit, theme=self.current_theme)
        self.qt_handler.setLevel(logging.DEBUG)
        
        # Remove any existing handlers (to avoid duplicates)
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Add our custom handler
        self.logger.addHandler(self.qt_handler)
        
        # Log initial message
        self.logger.info("ロギングが初期化されました。ボタンをクリックしてログを生成してください。")
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.current_theme == "light":
            self.current_theme = "dark"
            self.theme_button.setText("Switch to Light Theme")
        else:
            self.current_theme = "light"
            self.theme_button.setText("Switch to Dark Theme")
        
        # Update handler theme
        self.qt_handler.set_theme(self.current_theme)
        
        # Clear text edit to show color changes properly
        self.log_text_edit.clear()
        
        # Log theme change message
        self.logger.info(f"テーマを {self.current_theme} に変更しました")
    
    def log_structured_data(self):
        """Log a message with structured data."""
        self.logger.info(
            "構造化データを含むログメッセージ",
            extra={
                "json_fields": {
                    "user_id": "1234",
                    "action": "button_click",
                    "timestamp": "2025-04-07T09:25:38+09:00"
                }
            }
        )


def main():
    app = QApplication(sys.argv)
    demo = LoggingDemo()
    demo.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()