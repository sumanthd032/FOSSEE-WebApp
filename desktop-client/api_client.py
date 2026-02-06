import requests

BASE_URL = "http://127.0.0.1:8000/api"

class APIClient:
    @staticmethod
    def get_dashboard_data():
        """Fetches the latest stats and equipment list."""
        try:
            response = requests.get(f"{BASE_URL}/dashboard/")
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
                response = requests.post(f"{BASE_URL}/upload/", files=files)
                
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
            with requests.get(f"{BASE_URL}/report/pdf/", stream=True) as r:
                r.raise_for_status()
                with open(save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return True, "Download Complete"
        except Exception as e:
            return False, str(e)