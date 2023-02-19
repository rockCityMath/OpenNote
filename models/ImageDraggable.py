from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from pprint import pprint

class ImageDraggable(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setPixmap(QPixmap('product1.png'))
        self.setGeometry(100, 100, 100, 100)

    def mouseMoveEvent(self, event):
            if event.buttons() == Qt.LeftButton:
                self.isMoving = True
                mimeData = QMimeData()
                drag = QDrag(self)
                drag.setMimeData(mimeData)
                drag.exec_(Qt.MoveAction)
        
        