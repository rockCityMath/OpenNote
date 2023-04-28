from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class RedTextbox(QTextEdit):
    def __init__(self, x, y, w = 15, h = 30, t = ''):
        super().__init__()

        self.setGeometry(x, y, w, h)
        self.setText(t)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textChanged.connect(self.textChangedEvent)
        self.setStyleSheet('background-color: red;')

    def textChangedEvent(self):
        if len(self.toPlainText()) < 2:
            print("RESIZE TEXT")
            self.resize(100, 100)

    def changeBackgroundColorEvent(self, color: QColor):
        print("NEW COLOR: ", color)
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
        return RedTextbox(clickPos.x(), clickPos.y())

    def __getstate__(self):
        data = {}

        data['geometry'] = self.parentWidget().geometry()
        data['content'] = self.toHtml()
        return data

    def __setstate__(self, data):
        self.__init__(data['geometry'].x(), data['geometry'].y(), data['geometry'].width(), data['geometry'].height(), data['content'])

    def checkEmpty(self):
        if len(self.toPlainText()) < 1:
            return True
        return False


