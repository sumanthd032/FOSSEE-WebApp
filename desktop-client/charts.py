import matplotlib
matplotlib.use('Qt5Agg') # Force Qt5 Backend
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget, QVBoxLayout

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor('#f5f5f5')
        super(MplCanvas, self).__init__(self.fig)

class DashboardCharts(QWidget):
    def __init__(self, data):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create Canvas
        self.canvas = MplCanvas(self, width=10, height=8, dpi=100)
        layout.addWidget(self.canvas)
        
        self.plot_charts(data)

    def plot_charts(self, data):
        self.canvas.fig.clear()

        # 1. Doughnut Chart (Distribution)
        if 'distribution' in data and data['distribution']:
            ax1 = self.canvas.fig.add_subplot(211)
            types = [d['type'] for d in data['distribution']]
            counts = [d['count'] for d in data['distribution']]
            # Modern colors
            colors = ['#1E88E5', '#E53935', '#43A047', '#FB8C00', '#8E24AA']
            
            ax1.pie(counts, labels=types, autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops=dict(width=0.4))
            ax1.set_title("Equipment Type Distribution", fontsize=10, fontweight='bold', pad=10)

        # 2. Bar Chart (Top Pressures)
        if 'equipment_list' in data and data['equipment_list']:
            ax2 = self.canvas.fig.add_subplot(212)
            # Sort top 5 by pressure
            sorted_equip = sorted(data['equipment_list'], key=lambda x: x['pressure'], reverse=True)[:5]
            
            names = [d['name'] for d in sorted_equip]
            pressures = [d['pressure'] for d in sorted_equip]
            
            ax2.bar(names, pressures, color='#3949AB', alpha=0.8)
            ax2.set_ylabel("Pressure (bar)")
            ax2.set_title("Critical Pressure Levels (Top 5)", fontsize=10, fontweight='bold', pad=10)
            ax2.grid(True, axis='y', linestyle='--', alpha=0.3)

        self.canvas.fig.tight_layout(pad=2.0)
        self.canvas.draw()