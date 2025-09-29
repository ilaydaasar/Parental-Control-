from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QComboBox, QPushButton, QFormLayout, QMessageBox
from utils.limits import load_limits, save_limits

class LimitsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.layout().addWidget(QLabel("⏱ Süre Limitleri (dakika cinsinden)"))
        self.form = QFormLayout()
        self.widgets = {}
        limits = load_limits()

        for category in ["game", "web", "chat", "video", "other"]:
            spin = QSpinBox()
            spin.setRange(1, 240)
            spin.setValue(limits.get(category, {}).get("limit", 60))

            combo = QComboBox()
            combo.addItems(["notify", "close"])
            combo.setCurrentText(limits.get(category, {}).get("action", "notify"))

            self.form.addRow(f"{category.title()} süresi:", spin)
            self.form.addRow(f"{category.title()} aksiyon:", combo)
            self.widgets[category] = (spin, combo)

        self.layout().addLayout(self.form)

        save_btn = QPushButton("💾 Kaydet")
        save_btn.clicked.connect(self.save)
        self.layout().addWidget(save_btn)

    def save(self):
        new_data = {}
        for category, (spin, combo) in self.widgets.items():
            new_data[category] = {
                "limit": spin.value(),
                "action": combo.currentText()
            }

        save_limits(new_data)
        QMessageBox.information(self, "Başarılı", "Limitler kaydedildi.")
