import requests

BASE_URL = "http://127.0.0.1:8000/api"

class APIClient:
    TOKEN = None  # Class variable to store token

    @classmethod
    def set_token(cls, token):
        cls.TOKEN = token

    @classmethod
    def get_headers(cls):
        """Helper to attach Auth header."""
        if cls.TOKEN:
            return {'Authorization': f'Token {cls.TOKEN}'}
        return {}

    @staticmethod
    def login(username, password):
        """Authenticate user and return token response if successful."""
        try:
            payload = {'username': username, 'password': password}
            response = requests.post(f"{BASE_URL}/login/", json=payload)
            if response.status_code == 200:
                return response.json()  # Returns {'token': '...'}
            return None
        except requests.exceptions.RequestException:
            return None

    @staticmethod
    def get_dashboard_data():
        """Fetches the latest stats and equipment list."""
        try:
            response = requests.get(
                f"{BASE_URL}/dashboard/",
                headers=APIClient.get_headers()
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 204:
                return None 
            else:
                print(f"Error fetching data: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Network Error: {e}")
            return None

    @staticmethod
    def upload_file(file_path):
        """Uploads a CSV file to the backend."""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f"{BASE_URL}/upload/",
                    files=files,
                    headers=APIClient.get_headers()
                )
                
            if response.status_code == 201:
                return True, "Upload Successful"
            else:
                return False, f"Upload Failed: {response.text}"
        except Exception as e:
            return False, str(e)
        
    @staticmethod
    def download_pdf(save_path):
        """Downloads the PDF and saves it to the specified path."""
        try:
            with requests.get(
                f"{BASE_URL}/report/pdf/",
                stream=True,
                headers=APIClient.get_headers()
            ) as r:
                r.raise_for_status()
                with open(save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return True, "Download Complete"
        except Exception as e:
            return False, str(e)