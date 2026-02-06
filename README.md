# Chemical Equipment Visualizer (Hybrid Web + Desktop)

A hybrid data analytics platform for visualizing chemical equipment parameters.

This monorepo contains a Django backend, a React web frontend, and a PyQt5 desktop client.

## Features

- **Data Ingestion:** Upload CSV logs via Web or Desktop.
- **Analytics:** Real-time calculation of flowrate, pressure, and temperature stats.
- **Visualization:**
	- **Web:** Interactive Chart.js graphs and responsive tables.
	- **Desktop:** Embedded Matplotlib charts using PyQt5.
- **Reporting:** Auto-generate and download PDF summary reports.

## Tech Stack

- **Backend:** Python, Django, Django REST Framework, Pandas
- **Web Client:** React, Vite, Tailwind CSS, Chart.js
- **Desktop Client:** Python, PyQt5, Matplotlib, Qt-Material

## Installation & Setup

### 1. Backend (Django API)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API running at http://127.0.0.1:8000

### 2. Web Client (React)

```bash
cd web-client
npm install
npm run dev
```

App running at http://localhost:5173

### 3. Desktop Client (PyQt5)

```bash
cd desktop-client
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

