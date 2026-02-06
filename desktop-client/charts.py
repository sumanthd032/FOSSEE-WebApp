import matplotlib
matplotlib.use('Qt5Agg')
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
        
        self.canvas = MplCanvas(self, width=10, height=8, dpi=100)
        layout.addWidget(self.canvas)
        
        self.plot_charts(data)

    def plot_charts(self, data):
        self.canvas.fig.clear()

        # 1. Doughnut Chart (Left/Top)
        ax1 = self.canvas.fig.add_subplot(211)
        
        if 'distribution' in data:
            types = [d['type'] for d in data['distribution']]
            counts = [d['count'] for d in data['distribution']]
            colors = ['#1976D2', '#D32F2F', '#388E3C', '#FBC02D', '#7B1FA2']
            
            wedges, texts, autotexts = ax1.pie(counts, labels=types, autopct='%1.1f%%', 
                                               colors=colors, startangle=90, 
                                               wedgeprops=dict(width=0.4)) # Doughnut style
            ax1.set_title("Equipment Type Distribution", fontsize=12, fontweight='bold')

        # 2. Bar Chart (Right/Bottom)
        ax2 = self.canvas.fig.add_subplot(212)
        
        if 'equipment_list' in data:
            sorted_equip = sorted(data['equipment_list'], key=lambda x: x['pressure'], reverse=True)[:5]
            names = [d['name'] for d in sorted_equip]
            pressures = [d['pressure'] for d in sorted_equip]
            
            ax2.bar(names, pressures, color='#5C6BC0')
            ax2.set_ylabel("Pressure (bar)")
            ax2.set_title("Top 5 Critical Pressure Levels", fontsize=12, fontweight='bold')
            ax2.grid(True, axis='y', linestyle='--', alpha=0.5)

        self.canvas.fig.tight_layout(pad=3.0)
        self.canvas.draw()