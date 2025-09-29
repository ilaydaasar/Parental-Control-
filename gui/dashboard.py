from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QFrame
from PyQt5.QtGui import QPixmap
import os
import random
import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class RiskChartCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(4, 3), dpi=100)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        self.plot()

    def plot(self):
        labels = ['Web', 'Game', 'Chat', 'Video']
        values = [5, 2, 3, 1]  # Dummy data
        self.axes.clear()
        self.axes.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        self.draw()


class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # KPI Boxes
        kpi_layout = QHBoxLayout()
        for title in ["Toplam Riskli İçerik", "Ortalama Ekran Süresi", "Aktif Kategori", "Son Uyarı"]:
            group = QVBoxLayout()
            label = QLabel(title)
            label.setStyleSheet("font-weight: bold; font-size: 14px;")
            value = QLabel("0")  # Dummy placeholder
            value.setStyleSheet("font-size: 16px; color: #2a2a2a;")
            group.addWidget(label)
            group.addWidget(value)
            box = QFrame()
            box.setFrameShape(QFrame.Box)
            box.setLayout(group)
            box.setFixedWidth(200)
            kpi_layout.addWidget(box)
        main_layout.addLayout(kpi_layout)

        # Risk Images Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)
        self.load_risk_images(scroll_layout)
        scroll.setWidget(scroll_content)

        main_layout.addWidget(QLabel("📸 Yakalanan Riskli Görseller"))
        main_layout.addWidget(scroll)

        # Chart
        main_layout.addWidget(QLabel("📊 Risk Dağılımı Grafiği"))
        main_layout.addWidget(RiskChartCanvas())

        self.setLayout(main_layout)

    def load_risk_images(self, layout):
        folder = "flagged"
        today = datetime.datetime.now().strftime("%Y%m%d")
        if not os.path.exists(folder):
            return

        files = [f for f in os.listdir(folder) if today in f and f.endswith(".png")]
        selected = random.sample(files, min(3, len(files)))

        for file in selected:
            pixmap = QPixmap(os.path.join(folder, file))
            if not pixmap.isNull():
                label = QLabel()
                label.setPixmap(pixmap.scaled(180, 120))
                label.setFixedSize(180, 120)
                label.setStyleSheet("border: 1px solid gray; margin: 5px;")
                layout.addWidget(label)
