import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(100, 100, 1280, 800) # HD Resolution start

        # Main Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Setup Header (To mimic the Web Navbar)
        self.setup_header()

        # 2. Content Area (Placeholder)
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Placeholder text
        welcome_label = QLabel("Welcome to the Desktop Dashboard")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; color: #555; font-weight: bold;")
        self.content_layout.addWidget(welcome_label)
        
        self.main_layout.addWidget(self.content_area)

    def setup_header(self):
        """Creates a custom header bar to match the Web UI."""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        header.setFixedHeight(70)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        # Logo/Title Area
        title_label = QLabel("Chemical Visualizer")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #1976D2;  /* Match Web Blue */
        """)
        
        subtitle_label = QLabel("Hybrid Desktop Client")
        subtitle_label.setStyleSheet("color: #757575; font-size: 14px;")

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(subtitle_label)

        self.main_layout.addWidget(header)

if __name__ == "__main__":
    # Create the App
    app = QApplication(sys.argv)

    # Apply Material Theme
    apply_stylesheet(app, theme='light_blue.xml')

    # Custom tweaks to fix any theme oddities
    app.setStyleSheet(app.styleSheet() + """
        QMainWindow { background-color: #f5f5f5; }
    """)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())