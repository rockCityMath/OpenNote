from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class HelloWorldText(QLabel):
    def __init__(self, x, y, w = 150, h = 50):
        super().__init__()

        self.setGeometry(x, y, w, h)
        self.setText("Hello World!")

    @staticmethod
    def new(clickPos: QPoint):
        return HelloWorldText(clickPos.x(), clickPos.y())

    def __getstate__(self):
        data = {}

        data['geometry'] = self.parentWidget().geometry()
        return data

    def __setstate__(self, data):
        self.__init__(data['geometry'].x(), data['geometry'].y(), data['geometry'].width(), data['geometry'].height())


