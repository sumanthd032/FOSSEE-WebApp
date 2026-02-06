import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QHBoxLayout, QFrame, QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet

# Import our custom modules
from workers import UploadWorker, DataFetchWorker
from api_client import APIClient
from charts import DashboardCharts 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(100, 100, 1280, 800)

        # 1. Main Layout Setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 2. Add Permanent Header
        self.setup_header()
        
        # 3. Add Permanent Controls
        self.setup_controls() 
        
        # 4. Add Dynamic Content Area 
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.main_layout.addWidget(self.content_area)
        
        # 5. Add Permanent Status Bar 
        self.footer_bar = QFrame()
        self.footer_layout = QHBoxLayout(self.footer_bar)
        self.status_label = QLabel("Ready. Click 'Upload CSV' to begin.")
        self.status_label.setStyleSheet("color: #666; font-weight: bold;")
        self.footer_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.footer_bar)

        # Initial instruction in content area
        self.placeholder_label = QLabel("No Data Loaded.\nPlease upload a CSV file.")
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setStyleSheet("font-size: 18px; color: #888;")
        self.content_layout.addWidget(self.placeholder_label)

    def setup_header(self):
        header = QFrame()
        header.setStyleSheet("background-color: #ffffff; border-bottom: 1px solid #e0e0e0;")
        header.setFixedHeight(70)
        layout = QHBoxLayout(header)
        title = QLabel("Chemical Visualizer")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1976D2;")
        layout.addWidget(title)
        self.main_layout.addWidget(header)

    def setup_controls(self):
        controls = QFrame()
        layout = QHBoxLayout(controls)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Upload Button
        self.btn_upload = QPushButton("Upload CSV")
        self.btn_upload.setCursor(Qt.PointingHandCursor)
        self.btn_upload.clicked.connect(self.handle_upload_click)
        self.btn_upload.setProperty('class', 'success')
        
        # Refresh Button
        self.btn_refresh = QPushButton("Refresh Data")
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.refresh_data)

        # Export Button
        self.btn_export = QPushButton("Export PDF")
        self.btn_export.setCursor(Qt.PointingHandCursor)
        self.btn_export.clicked.connect(self.handle_export)
        self.btn_export.setProperty('class', 'warning')
        
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.btn_refresh)
        layout.addWidget(self.btn_export)
        layout.addStretch()
        
        self.main_layout.addWidget(controls)

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

    def refresh_data(self):
        self.status_label.setText("Fetching data from server...")
        self.data_worker = DataFetchWorker()
        self.data_worker.data_ready.connect(self.on_data_received)
        self.data_worker.error_occurred.connect(lambda msg: self.status_label.setText(msg))
        self.data_worker.start()

    def on_data_received(self, data):
        # 1. Clear content area
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 2. Add Summary Text
        summary = data['summary']
        stats_text = (f"Total Records: {summary['total_records']} | "
                      f"Avg Flow: {summary['avg_flowrate']:.2f} | "
                      f"Avg Pressure: {summary['avg_pressure']:.2f}")
        
        stats_label = QLabel(stats_text)
        stats_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; padding: 10px;")
        stats_label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(stats_label)

        # 3. Add Charts
        self.charts_widget = DashboardCharts(data)
        self.content_layout.addWidget(self.charts_widget)
        
        self.status_label.setText("Dashboard Updated successfully.")

    def handle_export(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Report", "report.pdf", "PDF Files (*.pdf)")
        if path:
            self.status_label.setText("Downloading PDF...")
            # For large files, use a Worker thread (like UploadWorker) to prevent freezing.
            success, msg = APIClient.download_pdf(path)
            if success:
                self.status_label.setText(f"Report saved to {path}")
                QMessageBox.information(self, "Success", f"Report saved to {path}")
            else:
                self.status_label.setText("Download failed.")
                QMessageBox.critical(self, "Error", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')
    
    # Fix for missing icons warning in terminal
    import os
    os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.svg.warning=false"

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())