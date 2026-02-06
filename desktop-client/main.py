import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QHBoxLayout, QFrame, QPushButton, QFileDialog, 
                             QMessageBox, QDialog, QStackedWidget, QTableWidget, 
                             QTableWidgetItem, QScrollArea)
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet

# Import Custom Modules
from workers import UploadWorker, DataFetchWorker
from api_client import APIClient
from login import LoginWindow
from charts import DashboardCharts 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(100, 100, 1366, 768)

        # Main Horizontal Layout (Sidebar + Content)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Sidebar Navigation
        self.setup_sidebar()

        # 2. Main Content Area (Stacked Tabs)
        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack)

        # 3. Footer / Status Bar
        self.statusBar = self.statusBar()
        self.status_label = QLabel("Ready.")
        self.status_label.setStyleSheet("color: #666; padding-left: 10px; font-weight: bold;")
        self.statusBar.addWidget(self.status_label)

        # Initialize Tab Views
        self.init_overview_tab()
        self.init_analytics_tab()
        self.init_data_tab()
        self.init_history_tab()

        # Load Data
        self.refresh_data()

    def setup_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("background-color: #1a2327; border-right: 1px solid #2c3e50;")
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Brand Header
        brand_box = QFrame()
        brand_box.setFixedHeight(80)
        brand_box.setStyleSheet("background-color: #0d1117; border-bottom: 1px solid #2c3e50;")
        brand_layout = QHBoxLayout(brand_box)
        brand_label = QLabel("CEV Desktop")
        brand_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold; letter-spacing: 1px;")
        brand_layout.addWidget(brand_label)
        layout.addWidget(brand_box)

        # Navigation Buttons
        self.nav_btns = []
        labels = ["Overview", "Analytics", "Data Logs", "History"]
        
        for i, label in enumerate(labels):
            btn = QPushButton(label)
            btn.setFixedHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left; padding-left: 25px; color: #90a4ae; 
                    background-color: transparent; border: none; font-size: 14px; font-weight: 500;
                }
                QPushButton:hover { background-color: #263238; color: white; }
                QPushButton:checked { background-color: #1976D2; color: white; border-left: 4px solid #64B5F6;}
            """)
            btn.setCheckable(True)
            if i == 0: btn.setChecked(True)
            btn.clicked.connect(lambda checked, idx=i: self.switch_tab(idx))
            self.nav_btns.append(btn)
            layout.addWidget(btn)

        layout.addStretch()
        
        # Logout Button
        btn_logout = QPushButton("Log Out")
        btn_logout.setStyleSheet("""
            QPushButton { color: #ef5350; background: transparent; border: none; padding: 20px; text-align: left; font-weight: bold; }
            QPushButton:hover { background-color: #2c1a1a; }
        """)
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.clicked.connect(self.handle_logout)
        layout.addWidget(btn_logout)

        self.main_layout.addWidget(sidebar)

    def switch_tab(self, index):
        for i, btn in enumerate(self.nav_btns):
            btn.setChecked(i == index)
        self.content_stack.setCurrentIndex(index)
        
        # Special case: If History tab is selected, fetch history
        if index == 3: 
            pass # TODO: Implement history fetch worker here if strictly separate

    def handle_logout(self):
        self.close()

    # --- TAB INITIALIZATION ---

    def init_overview_tab(self):
        self.overview_page = QWidget()
        layout = QVBoxLayout(self.overview_page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Title
        layout.addWidget(QLabel("Overview").setStyleSheet("font-size: 28px; font-weight: bold; color: #263238;"))

        # KPI Cards Area
        self.stats_container = QFrame()
        self.stats_layout = QHBoxLayout(self.stats_container)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stats_container)

        # Upload Section
        upload_box = QFrame()
        upload_box.setStyleSheet("background-color: #f8f9fa; border: 2px dashed #cfd8dc; border-radius: 12px;")
        upload_box.setFixedHeight(200)
        ul_layout = QVBoxLayout(upload_box)
        ul_layout.setAlignment(Qt.AlignCenter)
        
        ul_label = QLabel("Upload New Dataset")
        ul_label.setStyleSheet("color: #455a64; font-size: 16px; font-weight: bold;")
        
        btn_upload = QPushButton("Select CSV File")
        btn_upload.setFixedWidth(200)
        btn_upload.setCursor(Qt.PointingHandCursor)
        btn_upload.setStyleSheet("background-color: #1976D2; color: white; padding: 12px; font-weight: bold; border-radius: 6px;")
        btn_upload.clicked.connect(self.handle_upload_click)
        
        ul_layout.addWidget(ul_label)
        ul_layout.addWidget(btn_upload)
        layout.addWidget(upload_box)
        
        layout.addStretch()
        self.content_stack.addWidget(self.overview_page)

    def init_analytics_tab(self):
        self.analytics_page = QWidget()
        layout = QVBoxLayout(self.analytics_page)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("Analytics Dashboard")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #263238;")
        
        btn_pdf = QPushButton("Download Report")
        btn_pdf.setIcon(self.style().standardIcon(self.style().SP_DialogSaveButton))
        btn_pdf.setCursor(Qt.PointingHandCursor)
        btn_pdf.clicked.connect(self.handle_export)
        btn_pdf.setStyleSheet("background-color: #263238; color: white; padding: 10px 20px; border-radius: 6px; font-weight: bold;")
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(btn_pdf)
        layout.addLayout(header)

        # Charts Area
        self.charts_container = QVBoxLayout()
        layout.addLayout(self.charts_container)
        
        self.content_stack.addWidget(self.analytics_page)

    def init_data_tab(self):
        self.data_page = QWidget()
        layout = QVBoxLayout(self.data_page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.addWidget(QLabel("Raw Data Logs").setStyleSheet("font-size: 28px; font-weight: bold; color: #263238; margin-bottom: 20px;"))
        
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)
        
        self.content_stack.addWidget(self.data_page)

    def init_history_tab(self):
        self.history_page = QWidget()
        layout = QVBoxLayout(self.history_page)
        layout.setContentsMargins(40, 40, 40, 40)
        
        layout.addWidget(QLabel("Upload History").setStyleSheet("font-size: 28px; font-weight: bold; color: #263238; margin-bottom: 20px;"))
        
        # Scroll Area for History List
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: transparent;")
        
        self.history_content = QWidget()
        self.history_layout = QVBoxLayout(self.history_content)
        self.history_layout.setAlignment(Qt.AlignTop)
        
        scroll.setWidget(self.history_content)
        layout.addWidget(scroll)
        
        self.content_stack.addWidget(self.history_page)

    # --- LOGIC & WORKERS ---

    def refresh_data(self):
        self.status_label.setText("Syncing data with server...")
        self.data_worker = DataFetchWorker()
        self.data_worker.data_ready.connect(self.on_data_received)
        self.data_worker.error_occurred.connect(lambda msg: self.status_label.setText(f"Error: {msg}"))
        self.data_worker.start()

    def on_data_received(self, data):
        self.dashboard_data = data
        self.status_label.setText("Data Synced.")
        
        # 1. Update Stats
        self.update_stats(data['summary'])
        # 2. Update Charts
        self.update_charts(data)
        # 3. Update Table
        self.update_table(data['equipment_list'])
        # 4. Update History 
        self.update_history_simulated(data['summary'])

    def update_stats(self, summary):
        # Clear existing
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        metrics = [
            ("Total Records", summary['total_records'], "#1976D2"),
            ("Avg Flow", f"{summary['avg_flowrate']:.2f}", "#388E3C"),
            ("Avg Pressure", f"{summary['avg_pressure']:.2f}", "#FBC02D"),
            ("Avg Temp", f"{summary['avg_temperature']:.2f}", "#D32F2F")
        ]

        for label, value, color in metrics:
            card = QFrame()
            card.setStyleSheet(f"background-color: white; border-left: 5px solid {color}; border-radius: 8px; border: 1px solid #e0e0e0;")
            card.setFixedWidth(240)
            card.setFixedHeight(120)
            
            l = QVBoxLayout(card)
            l.setContentsMargins(20, 20, 20, 20)
            
            lbl_title = QLabel(label)
            lbl_title.setStyleSheet("color: #78909c; font-weight: bold; font-size: 14px;")
            
            lbl_val = QLabel(str(value))
            lbl_val.setStyleSheet("color: #263238; font-weight: bold; font-size: 28px;")
            
            l.addWidget(lbl_title)
            l.addWidget(lbl_val)
            self.stats_layout.addWidget(card)
        
        self.stats_layout.addStretch()

    def update_charts(self, data):
        # Clear previous charts
        while self.charts_container.count():
            item = self.charts_container.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        self.charts = DashboardCharts(data)
        self.charts_container.addWidget(self.charts)

    def update_table(self, equipment_list):
        cols = ["ID", "Name", "Type", "Flowrate", "Pressure", "Temp"]
        self.table_widget.setColumnCount(len(cols))
        self.table_widget.setHorizontalHeaderLabels(cols)
        self.table_widget.setRowCount(len(equipment_list))
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setStyleSheet("QHeaderView::section { background-color: #eceff1; padding: 4px; border: none; font-weight: bold; }")
        
        for row, item in enumerate(equipment_list):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(item['equipment_id'])))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(item['name'])))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(item['type'])))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(item['flowrate'])))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(item['pressure'])))
            self.table_widget.setItem(row, 5, QTableWidgetItem(str(item['temperature'])))

    def update_history_simulated(self, summary):
        
        # Clear
        while self.history_layout.count():
            item = self.history_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        # Create a card
        card = QFrame()
        card.setStyleSheet("background-color: white; border: 1px solid #e0e0e0; border-radius: 8px;")
        card.setFixedHeight(80)
        h_layout = QHBoxLayout(card)
        
        icon = QLabel("📄")
        icon.setStyleSheet("font-size: 24px;")
        
        info_layout = QVBoxLayout()
        fname = QLabel(summary['file_name'])
        fname.setStyleSheet("font-weight: bold; font-size: 16px;")
        fdate = QLabel(f"Uploaded: {summary['uploaded_at']}")
        fdate.setStyleSheet("color: #90a4ae;")
        info_layout.addWidget(fname)
        info_layout.addWidget(fdate)
        
        h_layout.addWidget(icon)
        h_layout.addLayout(info_layout)
        h_layout.addStretch()
        
        self.history_layout.addWidget(card)

    def handle_upload_click(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.status_label.setText(f"Uploading {file_path}...")
            self.upload_worker = UploadWorker(file_path)
            self.upload_worker.finished.connect(self.on_upload_finished)
            self.upload_worker.start()

    def on_upload_finished(self, success, message):
        if success:
            QMessageBox.information(self, "Success", message)
            self.refresh_data()
        else:
            QMessageBox.critical(self, "Error", message)
            self.status_label.setText("Upload Failed.")

    def handle_export(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Report", "report.pdf", "PDF Files (*.pdf)")
        if path:
            self.status_label.setText("Downloading PDF...")
            success, msg = APIClient.download_pdf(path)
            if success:
                QMessageBox.information(self, "Success", f"Report saved to {path}")
            else:
                QMessageBox.critical(self, "Error", msg)
            self.status_label.setText("Ready.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply Theme
    apply_stylesheet(app, theme='light_blue.xml')
    
    # Fix Icon Warnings
    os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.svg.warning=false"

    # Login Flow
    login = LoginWindow()
    if login.exec_() == QDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)