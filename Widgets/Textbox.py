from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class TextboxWidget(QTextEdit):
    def __init__(self, x, y, w = 100, h = 100, t = 'new text!'):
        super().__init__()

        self.setGeometry(x, y, w, h)                       # This sets geometry of DraggableObject
        self.setText(t)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.persistGeometry = self.geometry()

    def changeBackgroundColorEvent(self, color: QColor):
        print("NEW COLOR: ", color)
        # self.setStyleSheet()
        print(color.getRgb())
        rgb = color.getRgb()
        self.setStyleSheet(f'background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]});')

    def changeFontColorEvent(self, color: QColor):
        self.setTextColor(color)
        self.removeSelection()

    def changeFontEvent(self, font: QFont):
        self.setCurrentFont(font)
        self.removeSelection()

    def changeFontSizeEvent(self, size: int):
        self.setFontPointSize(size)
        self.removeSelction()

    def changeFontBoldEvent(self):
        self.setFontWeight(QFont.Bold)
        self.removeSelection()

    def changeFontItalicEvent(self):
        self.setFontItalic(True)
        self.removeSelection()

    def changeFontUnderlineEvent(self):
        self.setFontUnderline(True)
        self.removeSelection()

    def removeSelection(self):
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)

    @staticmethod
    def new(clickPos: QPoint):
        return TextboxWidget(clickPos.x(), clickPos.y())

    def newGeometryEvent(self, newGeometry: QRect):
        self.persistGeometry = newGeometry

    def __getstate__(self):
        data = {}

        data['geometry'] = self.parentWidget().geometry()
        data['content'] = self.toHtml()
        return data

    def __setstate__(self, data):
        self.__init__(data['geometry'].x(), data['geometry'].y(), data['geometry'].width(), data['geometry'].height(), data['content'])


