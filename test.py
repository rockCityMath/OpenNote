import sys
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QLabel

class DragLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mime_data = QMimeData()
        drag.setMimeData(mime_data)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.MoveAction)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setWindowTitle("Drag and Drop Example")
        self.setGeometry(100, 100, 400, 300)
        self.drag_line_edit = DragLineEdit(self)
        self.drag_line_edit.setText("Drag me around")
        self.drag_line_edit.move(50, 50)
        self.drop_label = QLabel(self)
        self.drop_label.setText("Drop here")
        self.drop_label.setGeometry(150, 150, 100, 50)
        self.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.drag_line_edit.move(event.pos() - self.drag_line_edit.rect().center())
        event.setDropAction(Qt.MoveAction)
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())