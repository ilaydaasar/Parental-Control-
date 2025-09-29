from PyQt5.QtCore import QAbstractListModel, Qt, QVariant, pyqtSlot, QModelIndex, pyqtSignal
import os

class KeylogData(QAbstractListModel):
    fileSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.logs = []  # sadece dosya adları
        self.filtered_logs = []
        self.loadLogs()

    def rowCount(self, parent=QModelIndex()):
        return len(self.filtered_logs)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.filtered_logs):
            return QVariant()
        if role == Qt.DisplayRole:
            return self.filtered_logs[index.row()]
        return QVariant()

    def roleNames(self):
        return {Qt.DisplayRole: b'text'}

    def loadLogs(self):
        self.logs = []
        log_dir = "keylogs"
        if not os.path.exists(log_dir):
            return
        for filename in sorted(os.listdir(log_dir)):
            if filename.endswith(".txt"):
                self.logs.append(filename)
        self.filtered_logs = self.logs.copy()

    @pyqtSlot(str)
    def setFilter(self, keyword):
        self.loadLogs()
        if keyword.strip():
            self.filtered_logs = []
            for filename in self.logs:
                path = os.path.join("keylogs", filename)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if keyword.lower() in content.lower():
                            self.filtered_logs.append(filename)
                except Exception as e:
                    print(f"Filtreleme hatası ({filename}): {e}")
        else:
            self.filtered_logs = self.logs.copy()

        self.layoutChanged.emit()


    @pyqtSlot(str, result=str)
    def readFileContent(self, filename):
        path = os.path.join("keylogs", filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return "Dosya bulunamadı."
