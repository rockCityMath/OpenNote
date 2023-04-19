from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from Modules.Enums import TextBoxStyles

class TextboxWidget(QTextEdit):
    def __init__(self, x, y, w = 100, h = 100, t = 'new text!'):
        super().__init__()

        self.setGeometry(x, y, w, h)                       # This sets geometry of DraggableObject
        self.setText(t)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.persistGeometry = self.geometry()

    @staticmethod
    def new(clickPos: QPoint):
        return TextboxWidget(clickPos.x(), clickPos.y())

    def newGeometryEvent(self, newGeometry: QRect):
        self.persistGeometry = newGeometry

    def __getstate__(self):
        data = {}

        # this is wierd, but dragcontainer position is seperate from this one, but we want that position
        # this widgets pos can be set in newGeometryEvent I think but it flickers too much
        data['geometry'] = self.persistGeometry
        data['content'] = self.toHtml()
        return data

    def __setstate__(self, data):
        self.__init__(data['geometry'].x(), data['geometry'].y(), data['geometry'].width(), data['geometry'].height(), data['content'])
        # print(type(self.__init__(data['geometry'].x(), data['geometry'].y(), data['geometry'].width(), data['geometry'].height(), data['content'])))


