# Chemical Equipment Visualizer (CEV)

A hybrid data analytics platform designed for monitoring and visualizing chemical equipment parameters.

This monorepo architecture integrates a robust Django backend with two distinct client frontends: a modern React web application and a native PyQt5 desktop application.

## 🚀 Features

### Core Functionality

- **Multi-Client Access:** Seamlessly switch between Web and Desktop interfaces; both connect to the same centralized API.
- **Secure Authentication:** Token-based user authentication system ensuring data privacy and user isolation.
- **Data Ingestion:** Drag-and-drop CSV upload for equipment logs (supports Flowrate, Pressure, Temperature, etc.).

### Analytics & Visualization

- **Real-time Dashboard:** Instant calculation of Key Performance Indicators (Total Records, Average Metrics).
- **Interactive Charts:**
	- **Web:** Doughnut distribution charts, Scatter plots for correlation analysis, and Radar charts using Chart.js.
	- **Desktop:** Embedded, interactive Matplotlib visualizations within a native PyQt5 interface.
- **Rolling History:** Automatically archives the last 5 uploads per user for quick reference.

### Reporting

- **PDF Generation:** One-click generation of professional PDF summary reports containing statistical overviews and data snapshots.

## 🛠 Tech Stack

| Component | Technologies |
| --- | --- |
| Backend | Python 3.10+, Django 5, Django REST Framework, Pandas, ReportLab, SQLite |
| Web Client | React 18, Vite, Tailwind CSS, Lucide Icons, Chart.js, Axios |
| Desktop Client | Python, PyQt5, Matplotlib, Requests, Qt-Material |

## 📦 Installation & Setup

### Prerequisites

- Python 3.10 or higher
- Node.js & npm (for Web Client)

**Linux users only:** Install SVG support for Qt:

```bash
sudo apt-get install libqt5svg5-dev
```

### 1) Backend (Django API)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Initialize the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create a superuser (optional):

```bash
python manage.py createsuperuser
```

Start the server:

```bash
python manage.py runserver
```

API running at http://127.0.0.1:8000

### 2) Web Client (React)

```bash
cd web-client
npm install
npm run dev
```

Open http://localhost:5173

### 3) Desktop Client (PyQt5)

```bash
cd desktop-client
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

