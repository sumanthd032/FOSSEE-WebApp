import matplotlib
matplotlib.use('Qt5Agg') # Tell Matplotlib to use Qt5 backend

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget, QVBoxLayout

class MplCanvas(FigureCanvas):
    """A generic Canvas to draw plots on."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Create a Figure object (the paper)
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor('#f5f5f5')
        
        # Initialize parent Canvas
        super(MplCanvas, self).__init__(self.fig)

class DashboardCharts(QWidget):
    """Container for the two specific charts."""
    def __init__(self, data):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Create Canvas
        self.canvas = MplCanvas(self, width=10, height=8, dpi=100)
        layout.addWidget(self.canvas)
        
        self.plot_charts(data)

    def plot_charts(self, data):
        # Clear previous figures
        self.canvas.fig.clear()

        # Add subplot at position 121 (1 row, 2 cols, index 1)
        ax1 = self.canvas.fig.add_subplot(211) 
        
        types = [d['type'] for d in data['distribution']]
        counts = [d['count'] for d in data['distribution']]
        colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6']
        
        ax1.pie(counts, labels=types, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title("Equipment Type Distribution")

        # Add subplot at position 212 (2 rows, 1 col, index 2) - Stacked vertically
        ax2 = self.canvas.fig.add_subplot(212)
        
        # Sort and Slice top 5
        sorted_equip = sorted(data['equipment_list'], key=lambda x: x['pressure'], reverse=True)[:5]
        names = [d['name'] for d in sorted_equip]
        pressures = [d['pressure'] for d in sorted_equip]
        
        ax2.bar(names, pressures, color='#6366f1')
        ax2.set_ylabel("Pressure (bar)")
        ax2.set_title("Critical Pressure Levels (Top 5)")
        ax2.grid(True, axis='y', linestyle='--', alpha=0.7)

        # Refresh canvas
        self.canvas.draw()