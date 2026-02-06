import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QHBoxLayout, QFrame, QPushButton, QFileDialog, 
                             QMessageBox, QDialog, QStackedWidget, QTableWidget, 
                             QTableWidgetItem, QScrollArea, QLineEdit, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFontDatabase 

# Import Custom Modules
from api_client import APIClient
from charts import DashboardCharts 

# --- WORKER THREADS ---
class UploadWorker(QThread):
    finished = pyqtSignal(bool, str)
    def __init__(self, path):
        super().__init__()
        self.path = path
    def run(self):
        success, msg = APIClient.upload_file(self.path)
        self.finished.emit(success, msg)

class DataFetchWorker(QThread):
    data_ready = pyqtSignal(dict)
    history_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def run(self):
        # 1. Fetch Dashboard
        dash = APIClient.get_dashboard_data()
        if dash:
            self.data_ready.emit(dash)
        else:
            self.error_occurred.emit("No Data or Connection Failed")
        
        # 2. Fetch History
        hist = APIClient.get_history()
        if hist:
            self.history_ready.emit(hist)

# --- LOGIN WINDOW ---
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 250)
        self.setStyleSheet("background-color: white; color: #333;")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        layout.addWidget(QLabel("Chemical Visualizer Login").setStyleSheet("font-weight: bold; font-size: 16px; border: none;"))
        
        self.user_in = QLineEdit()
        self.user_in.setPlaceholderText("Username")
        self.user_in.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")
        
        self.pass_in = QLineEdit()
        self.pass_in.setPlaceholderText("Password")
        self.pass_in.setEchoMode(QLineEdit.Password)
        self.pass_in.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")
        
        layout.addWidget(self.user_in)
        layout.addWidget(self.pass_in)
        
        btn = QPushButton("Sign In")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("background-color: #1976D2; color: white; padding: 10px; font-weight: bold; border-radius: 4px;")
        btn.clicked.connect(self.do_login)
        layout.addWidget(btn)

    def do_login(self):
        u = self.user_in.text()
        p = self.pass_in.text()
        if not u or not p: return
        
        res = APIClient.login(u, p)
        if res and 'token' in res:
            APIClient.set_token(res['token'])
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Invalid Credentials")

# --- MAIN WINDOW ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(100, 100, 1366, 768)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setup_sidebar()
        
        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack)

        self.init_overview_tab()
        self.init_analytics_tab()
        self.init_data_tab()
        self.init_history_tab()

        self.statusBar = self.statusBar()
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("padding: 5px;")
        self.statusBar.addWidget(self.status_label)

        self.refresh_data()

    def safe_add_widget(self, layout, widget):
        """Helper to prevent adding None widgets which crashes PyQt"""
        if widget is not None:
            layout.addWidget(widget)

    def setup_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("background-color: #263238;")
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QLabel("CEV Desktop")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: white; padding: 20px; background-color: #1c262b;")
        layout.addWidget(header)
        
        self.nav_btns = []
        labels = ["Overview", "Analytics", "Data Logs", "History"]
        for i, lbl in enumerate(labels):
            btn = QPushButton(lbl)
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(50)
            btn.setStyleSheet("""
                QPushButton { text-align: left; padding-left: 20px; border: none; background: transparent; color: #b0bec5; font-weight: bold; font-size: 14px;}
                QPushButton:checked { color: white; background-color: #37474f; border-left: 4px solid #42a5f5; }
                QPushButton:hover { color: white; background-color: #37474f; }
            """)
            btn.clicked.connect(lambda _, x=i: self.switch_tab(x))
            if i == 0: btn.setChecked(True)
            layout.addWidget(btn)
            self.nav_btns.append(btn)
            
        layout.addStretch()
        
        btn_logout = QPushButton("Log Out")
        btn_logout.clicked.connect(self.close)
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.setStyleSheet("color: #ef5350; padding: 20px; border: none; font-weight: bold; text-align: left; padding-left: 20px;")
        layout.addWidget(btn_logout)
        
        self.main_layout.addWidget(sidebar)

    def switch_tab(self, index):
        for i, btn in enumerate(self.nav_btns):
            btn.setChecked(i == index)
        self.content_stack.setCurrentIndex(index)

    def init_overview_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        self.safe_add_widget(layout, QLabel("Overview").setStyleSheet("font-size: 24px; font-weight: bold; color: #333;"))
        
        # Stats Area
        self.stats_box = QFrame()
        self.stats_layout = QHBoxLayout(self.stats_box)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        self.safe_add_widget(layout, self.stats_box)
        
        # Upload
        upload_container = QFrame()
        upload_container.setStyleSheet("background-color: #f5f5f5; border: 2px dashed #ccc; border-radius: 8px;")
        upload_container.setFixedHeight(150)
        ul_layout = QVBoxLayout(upload_container)
        ul_layout.setAlignment(Qt.AlignCenter)
        
        btn_upload = QPushButton("Upload New CSV")
        btn_upload.setFixedWidth(200)
        btn_upload.setCursor(Qt.PointingHandCursor)
        btn_upload.setStyleSheet("background-color: #1976D2; color: white; padding: 12px; font-weight: bold; border-radius: 4px;")
        btn_upload.clicked.connect(self.upload_file)
        
        self.safe_add_widget(ul_layout, QLabel("Drag CSV here or click to upload").setStyleSheet("color: #666; font-weight: bold;"))
        self.safe_add_widget(ul_layout, btn_upload)
        self.safe_add_widget(layout, upload_container)
        
        layout.addStretch()
        self.content_stack.addWidget(page)

    def init_analytics_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        header = QHBoxLayout()
        self.safe_add_widget(header, QLabel("Analytics Dashboard").setStyleSheet("font-size: 24px; font-weight: bold; color: #333;"))
        
        btn_pdf = QPushButton("Download Report")
        btn_pdf.setCursor(Qt.PointingHandCursor)
        btn_pdf.clicked.connect(self.download_report)
        btn_pdf.setStyleSheet("background-color: #333; color: white; padding: 8px 16px; font-weight: bold; border-radius: 4px;")
        self.safe_add_widget(header, btn_pdf)
        
        layout.addLayout(header)
        
        self.chart_container = QVBoxLayout()
        layout.addLayout(self.chart_container)
        
        self.content_stack.addWidget(page)

    def init_data_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.safe_add_widget(layout, QLabel("Raw Data Logs").setStyleSheet("font-size: 24px; font-weight: bold; color: #333;"))
        
        self.table = QTableWidget()
        self.safe_add_widget(layout, self.table)
        self.content_stack.addWidget(page)

    def init_history_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.safe_add_widget(layout, QLabel("Upload History").setStyleSheet("font-size: 24px; font-weight: bold; color: #333;"))
        
        self.history_list_layout = QVBoxLayout()
        self.history_list_layout.setAlignment(Qt.AlignTop)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(self.history_list_layout)
        scroll.setWidget(container)
        
        self.safe_add_widget(layout, scroll)
        self.content_stack.addWidget(page)

    def refresh_data(self):
        self.worker = DataFetchWorker()
        self.worker.data_ready.connect(self.update_ui)
        self.worker.history_ready.connect(self.update_history)
        self.worker.start()

    def update_ui(self, data):
        # 1. Update Stats
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        summary = data['summary']
        metrics = [
            ("Total Records", summary['total_records'], "#1E88E5"),
            ("Avg Flow", f"{summary['avg_flowrate']:.2f}", "#43A047"),
            ("Avg Pressure", f"{summary['avg_pressure']:.2f}", "#FB8C00")
        ]
        
        for label, val, color in metrics:
            card = QFrame()
            card.setStyleSheet(f"background-color: white; border-left: 5px solid {color}; border: 1px solid #ddd; border-radius: 6px;")
            cl = QVBoxLayout(card)
            self.safe_add_widget(cl, QLabel(label).setStyleSheet("color: #777; font-weight: bold; font-size: 12px;"))
            self.safe_add_widget(cl, QLabel(str(val)).setStyleSheet("font-size: 24px; font-weight: bold; color: #333;"))
            self.safe_add_widget(self.stats_layout, card)
            
        # 2. Update Charts
        while self.chart_container.count():
            item = self.chart_container.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        chart_widget = DashboardCharts(data)
        self.safe_add_widget(self.chart_container, chart_widget)
        
        # 3. Update Table
        self.update_table(data['equipment_list'])

    def update_table(self, rows):
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Type", "Flow", "Pressure"])
        self.table.setStyleSheet("QHeaderView::section { background-color: #f0f0f0; padding: 5px; border: none; }")
        for r, item in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(str(item['equipment_id'])))
            self.table.setItem(r, 1, QTableWidgetItem(str(item['name'])))
            self.table.setItem(r, 2, QTableWidgetItem(str(item['type'])))
            self.table.setItem(r, 3, QTableWidgetItem(str(item['flowrate'])))
            self.table.setItem(r, 4, QTableWidgetItem(str(item['pressure'])))

    def update_history(self, history):
        while self.history_list_layout.count():
            item = self.history_list_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        for item in history:
            card = QFrame()
            card.setStyleSheet("background-color: white; border: 1px solid #eee; border-radius: 6px; padding: 10px;")
            card.setFixedHeight(70)
            
            cl = QHBoxLayout(card)
            
            # File Info
            info_layout = QVBoxLayout()
            fname = QLabel(item['file_name'])
            fname.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
            fdate = QLabel(str(item['uploaded_at']).split('T')[0])
            fdate.setStyleSheet("color: #888; font-size: 12px;")
            self.safe_add_widget(info_layout, fname)
            self.safe_add_widget(info_layout, fdate)
            
            cl.addLayout(info_layout)
            cl.addStretch()
            self.safe_add_widget(cl, QLabel(f"{item['total_records']} Records").setStyleSheet("background-color: #e3f2fd; color: #1976D2; padding: 5px 10px; border-radius: 12px; font-size: 12px; font-weight: bold;"))
            
            self.safe_add_widget(self.history_list_layout, card)

    def upload_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "CSV", "", "*.csv")
        if path:
            self.status_label.setText(f"Uploading {os.path.basename(path)}...")
            self.u_worker = UploadWorker(path)
            self.u_worker.finished.connect(lambda s, m: (QMessageBox.information(self, "Info", m), self.refresh_data()))
            self.u_worker.start()

    def download_report(self):
        path, _ = QFileDialog.getSaveFileName(self, "PDF", "report.pdf", "*.pdf")
        if path:
            APIClient.download_pdf(path)
            QMessageBox.information(self, "Info", "Saved!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    try:
        from qt_material import apply_stylesheet

        apply_stylesheet(app, theme='light_blue.xml')
    except Exception as e:
        print(f"Theme load warning: {e}. Running with default style.")
    
    # Suppress loud SVG warnings
    os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.svg.warning=false"

    login = LoginWindow()
    if login.exec_() == QDialog.Accepted:
        w = MainWindow()
        w.show()
        sys.exit(app.exec_())