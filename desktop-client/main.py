import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QHBoxLayout, QFrame, QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet
from workers import UploadWorker, DataFetchWorker
from charts import DashboardCharts

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(100, 100, 1280, 800)

        # Main Layout Setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.setup_header()
        self.setup_controls() # New Control Bar
        
        # Content Area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.main_layout.addWidget(self.content_area)
        
        # Initial Placeholder
        self.status_label = QLabel("Ready. Click 'Upload CSV' to begin.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(self.status_label)

    def setup_header(self):
        # (Same as Step 6)
        header = QFrame()
        header.setStyleSheet("background-color: #ffffff; border-bottom: 1px solid #e0e0e0;")
        header.setFixedHeight(70)
        layout = QHBoxLayout(header)
        title = QLabel("Chemical Visualizer")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1976D2;")
        layout.addWidget(title)
        self.main_layout.addWidget(header)

    def setup_controls(self):
        """Creates the toolbar with action buttons."""
        controls = QFrame()
        layout = QHBoxLayout(controls)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Upload Button
        self.btn_upload = QPushButton("Upload CSV")
        self.btn_upload.setCursor(Qt.PointingHandCursor)
        self.btn_upload.clicked.connect(self.handle_upload_click)
        
        # Refresh Button
        self.btn_refresh = QPushButton("Refresh Data")
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.refresh_data)

        # Styling buttons slightly differently
        self.btn_upload.setProperty('class', 'success')
        
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.btn_refresh)
        layout.addStretch()
        
        self.main_layout.addWidget(controls)

    def handle_upload_click(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.status_label.setText(f"Uploading {file_path}...")
            
            # Start Background Thread
            self.upload_worker = UploadWorker(file_path)
            self.upload_worker.finished.connect(self.on_upload_finished)
            self.upload_worker.start()

    def on_upload_finished(self, success, message):
        if success:
            QMessageBox.information(self, "Success", message)
            self.refresh_data() # Auto-refresh after upload
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
        count = data['summary']['total_records']
        self.status_label.setText(f"Data Loaded! Total Records: {count}\n(Charts coming in Step 8)")
        print("Data Received:", data['summary'])

    def on_data_received(self, data):
        # Clear current content in content_layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Create Summary Text 
        summary = data['summary']
        stats_text = (f"Total Records: {summary['total_records']} | "
                      f"Avg Flow: {summary['avg_flowrate']:.2f} | "
                      f"Avg Pressure: {summary['avg_pressure']:.2f}")
        
        stats_label = QLabel(stats_text)
        stats_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; padding: 10px;")
        stats_label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(stats_label)

        # Add Charts Widget
        self.charts_widget = DashboardCharts(data)
        self.content_layout.addWidget(self.charts_widget)
        
        self.status_label.setText("Dashboard Updated.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())