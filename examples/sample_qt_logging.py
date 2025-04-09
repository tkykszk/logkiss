#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example of using logkiss QtTextEditHandler.
This example shows how to use the QtTextEditHandler to display colored logs in a Qt application.
"""

import sys
import logging
import logkiss

# Check if Qt is available
if not logkiss.QT_AVAILABLE:
    print("Qt modules not available. Please install PyQt5, PySide2, or PySide6 to run this example.")
    sys.exit(1)

# Import Qt modules - we've already checked that one of them is available via QT_AVAILABLE
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
    from PyQt5.QtGui import QFont
except ImportError:
    try:
        from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
        from PySide2.QtGui import QFont
    except ImportError:
        from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
        from PySide6.QtGui import QFont


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
        self.qt_handler = logkiss.QtTextEditHandler(self.log_text_edit, theme=self.current_theme)
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
    """Main function to run the demo application."""
    app = QApplication(sys.argv)
    demo = LoggingDemo()
    demo.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
