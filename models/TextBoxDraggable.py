from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class TextBoxDraggable(QTextEdit):
    def __init__(self, parent, x, y):
        super().__init__(parent)
        self.setGeometry(x, y, 180, 90)
        self.setStyleSheet("border: 5px solid #000; border-radius: 10px;")
        self.isMoving = False
        

    def __getstate__(self):
        self = self
        return self.__dict__
        
    def __setstate__(self, dict):
        self.__dict__ = dict
        self = self