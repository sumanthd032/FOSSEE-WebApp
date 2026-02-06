import sys
import os
# 
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QHBoxLayout, QFrame, QPushButton, QFileDialog, 
                             QMessageBox, QDialog, QStackedWidget, QTableWidget, 
                             QTableWidgetItem, QScrollArea, QLineEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Optional: Theme (Wrapped in try/catch to prevent crashes if missing)
try:
    from qt_material import apply_stylesheet
    HAS_THEME = True
except ImportError:
    HAS_THEME = False

# Import Custom Modules
from api_client import APIClient
from charts import DashboardCharts 

# --- WORKER THREADS (For Non-Blocking UI) ---
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
        
        layout.addWidget(QLabel("Chemical Visualizer Login").setStyleSheet("font-weight: bold; font-size: 16px;"))
        
        self.user_in = QLineEdit()
        self.user_in.setPlaceholderText("Username")
        self.pass_in = QLineEdit()
        self.pass_in.setPlaceholderText("Password")
        self.pass_in.setEchoMode(QLineEdit.Password)
        
        layout.addWidget(self.user_in)
        layout.addWidget(self.pass_in)
        
        btn = QPushButton("Sign In")
        btn.setStyleSheet("background-color: #1976D2; color: white; padding: 8px; font-weight: bold;")
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

        # 1. Sidebar
        self.setup_sidebar()

        # 2. Content Stack
        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack)

        # Init Tabs
        self.init_overview_tab()
        self.init_analytics_tab()
        self.init_data_tab()
        self.init_history_tab()

        # Status Bar
        self.statusBar = self.statusBar()
        self.status_label = QLabel("Ready")
        self.statusBar.addWidget(self.status_label)

        # Load Data
        self.refresh_data()

    def setup_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("background-color: #263238; color: white;")
        layout = QVBoxLayout(sidebar)
        
        layout.addWidget(QLabel("CEV Desktop").setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;"))
        
        self.nav_btns = []
        labels = ["Overview", "Analytics", "Data Logs", "History"]
        for i, lbl in enumerate(labels):
            btn = QPushButton(lbl)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton { text-align: left; padding: 15px; border: none; background: transparent; color: #b0bec5; font-weight: bold;}
                QPushButton:checked { color: white; background-color: #37474f; border-left: 4px solid #42a5f5; }
                QPushButton:hover { color: white; }
            """)
            btn.clicked.connect(lambda _, x=i: self.switch_tab(x))
            if i == 0: btn.setChecked(True)
            layout.addWidget(btn)
            self.nav_btns.append(btn)
            
        layout.addStretch()
        layout.addWidget(QPushButton("Log Out", clicked=self.close).setStyleSheet("color: #ef5350; padding: 20px; border: none; font-weight: bold;"))
        
        self.main_layout.addWidget(sidebar)

    def switch_tab(self, index):
        for i, btn in enumerate(self.nav_btns):
            btn.setChecked(i == index)
        self.content_stack.setCurrentIndex(index)

    # --- TAB UI SETUP ---
    def init_overview_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        layout.addWidget(QLabel("Overview").setStyleSheet("font-size: 24px; font-weight: bold; color: #333;"))
        
        # Stats Area
        self.stats_box = QFrame()
        self.stats_layout = QHBoxLayout(self.stats_box)
        layout.addWidget(self.stats_box)
        
        # Upload
        btn_upload = QPushButton("Upload New CSV")
        btn_upload.setFixedWidth(200)
        btn_upload.setStyleSheet("background-color: #1E88E5; color: white; padding: 12px; font-weight: bold; border-radius: 4px;")
        btn_upload.clicked.connect(self.upload_file)
        layout.addWidget(btn_upload)
        
        layout.addStretch()
        self.content_stack.addWidget(page)

    def init_analytics_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        header = QHBoxLayout()
        header.addWidget(QLabel("Analytics Dashboard").setStyleSheet("font-size: 24px; font-weight: bold; color: #333;"))
        btn_pdf = QPushButton("Download Report")
        btn_pdf.clicked.connect(self.download_report)
        btn_pdf.setStyleSheet("background-color: #333; color: white; padding: 8px 16px; font-weight: bold;")
        header.addWidget(btn_pdf)
        
        layout.addLayout(header)
        
        self.chart_container = QVBoxLayout()
        layout.addLayout(self.chart_container)
        
        self.content_stack.addWidget(page)

    def init_data_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Raw Data Logs").setStyleSheet("font-size: 24px; font-weight: bold; color: #333;"))
        
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.content_stack.addWidget(page)

    def init_history_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Upload History").setStyleSheet("font-size: 24px; font-weight: bold; color: #333;"))
        
        self.history_list_layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(self.history_list_layout)
        scroll.setWidget(container)
        
        layout.addWidget(scroll)
        self.content_stack.addWidget(page)

    # --- LOGIC ---
    def refresh_data(self):
        self.worker = DataFetchWorker()
        self.worker.data_ready.connect(self.update_ui)
        self.worker.history_ready.connect(self.update_history)
        self.worker.start()

    def update_ui(self, data):
        # 1. Update Stats
        # Clear old stats
        while self.stats_layout.count():
            w = self.stats_layout.takeAt(0).widget()
            if w: w.deleteLater()
            
        summary = data['summary']
        metrics = [
            ("Total Records", summary['total_records'], "#1E88E5"),
            ("Avg Flow", f"{summary['avg_flowrate']:.2f}", "#43A047"),
            ("Avg Pressure", f"{summary['avg_pressure']:.2f}", "#FB8C00")
        ]
        
        for label, val, color in metrics:
            card = QFrame()
            card.setStyleSheet(f"background-color: white; border-left: 5px solid {color}; border: 1px solid #ddd;")
            cl = QVBoxLayout(card)
            cl.addWidget(QLabel(label).setStyleSheet("color: #777; font-weight: bold;"))
            cl.addWidget(QLabel(str(val)).setStyleSheet("font-size: 24px; font-weight: bold;"))
            self.stats_layout.addWidget(card)
            
        # 2. Update Charts
        while self.chart_container.count():
            w = self.chart_container.takeAt(0).widget()
            if w: w.deleteLater()
        self.chart_container.addWidget(DashboardCharts(data))
        
        # 3. Update Table
        self.update_table(data['equipment_list'])

    def update_table(self, rows):
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Type", "Flow", "Pressure"])
        for r, item in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(str(item['equipment_id'])))
            self.table.setItem(r, 1, QTableWidgetItem(str(item['name'])))
            self.table.setItem(r, 2, QTableWidgetItem(str(item['type'])))
            self.table.setItem(r, 3, QTableWidgetItem(str(item['flowrate'])))
            self.table.setItem(r, 4, QTableWidgetItem(str(item['pressure'])))

    def update_history(self, history):
        while self.history_list_layout.count():
            w = self.history_list_layout.takeAt(0).widget()
            if w: w.deleteLater()
            
        for item in history:
            card = QFrame()
            card.setStyleSheet("background-color: white; border: 1px solid #ddd; margin-bottom: 5px; padding: 10px;")
            cl = QHBoxLayout(card)
            
            info = QLabel(f"<b>{item['file_name']}</b><br><span style='color:#777'>{item['uploaded_at']}</span>")
            stats = QLabel(f"Records: {item['total_records']}")
            
            cl.addWidget(info)
            cl.addStretch()
            cl.addWidget(stats)
            self.history_list_layout.addWidget(card)
        
        self.history_list_layout.addStretch()

    def upload_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "CSV", "", "*.csv")
        if path:
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
    
    # Try applying theme, ignore if fails (SVG errors)
    if HAS_THEME:
        try:
            apply_stylesheet(app, theme='light_blue.xml')
        except:
            pass
            
    # Fix logging noise
    os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.svg.warning=false"

    login = LoginWindow()
    if login.exec_() == QDialog.Accepted:
        w = MainWindow()
        w.show()
        sys.exit(app.exec_())