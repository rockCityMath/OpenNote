from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDialogButtonBox
from PyQt5.QtCore import Qt

class CreateTableDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.rowsLineEdit = QLineEdit()
        self.colsLineEdit = QLineEdit()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Rows:"))
        layout.addWidget(self.rowsLineEdit)
        layout.addWidget(QLabel("Columns:"))
        layout.addWidget(self.colsLineEdit)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def getTableSize(self):
        rows = int(self.rowsLineEdit.text())
        cols = int(self.colsLineEdit.text())
        return rows, cols

class MainWindow(QTableWidget):
    def __init__(self, rows, cols, parent=None):
        super().__init__(rows, cols, parent)

        self.setEditTriggers(QTableWidget.DoubleClicked)

app = QApplication([])

dialog = CreateTableDialog()
if dialog.exec_() == QDialog.Accepted:
    rows, cols = dialog.getTableSize()

    mainWindow = MainWindow(rows, cols)
    mainWindow.show()

    app.exec_()
