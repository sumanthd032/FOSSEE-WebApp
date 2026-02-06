from PyQt5.QtCore import QThread, pyqtSignal
from api_client import APIClient

class UploadWorker(QThread):
    finished = pyqtSignal(bool, str) # Signal sends back (Success?, Message)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        # This runs in a background thread
        success, message = APIClient.upload_file(self.file_path)
        self.finished.emit(success, message)

class DataFetchWorker(QThread):
    data_ready = pyqtSignal(dict) 
    error_occurred = pyqtSignal(str)

    def run(self):
        data = APIClient.get_dashboard_data()
        if data:
            self.data_ready.emit(data)
        else:
            self.error_occurred.emit("No data available or connection failed.")