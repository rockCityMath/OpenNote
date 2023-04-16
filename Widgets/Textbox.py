from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from Modules.Enums import TextBoxStyles, WidgetType

class TextboxWidget(QTextEdit):
    # NEW: Can either specify w, h, content or let it default
    def __init__(self, x, y, w = 10, h = 35, t = ''):
        super().__init__()

        self.type = 'text'
        self.setStyleSheet(TextBoxStyles.OUTFOCUS.value) # debt: this gets set all over the place
        self.setGeometry(x, y, w, h) # This sets geometry of DraggableObject, I think
        self.setText(t)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.show()

    # Set the textbox as selected so that the editor can change font attributes
    def mousePressEvent(self, event):
        # self.editor.selected = self
        QTextEdit.mousePressEvent(self, event)

    def focusOutEvent(self, event):
        QTextEdit.focusOutEvent(self, event)

    # When user starts typing in new box, expand its size
    def keyPressEvent(self, event):
        if len(self.toPlainText()) == 0:
            self.resize(100, 100)
            self.parentWidget().resize(100, 100)
            self.setStyleSheet(TextBoxStyles.INFOCUS.value)
        QTextEdit.keyPressEvent(self, event)

    # NEW: Save and load widget info from pickle methods
    def __getstate__(self):
        data = {}
        data['geometry'] = self.geometry()
        data['content'] = self.toHtml()

        return data

    def __setstate__(self, data):
        self.__data = data

    # Called when loading a notebook to reinstantiate widget
    def loadWidget(self, editor):
        print("LOAD WIDGET CALLED")
        # self.editor = editor
        # self.setGeometry(self.__data['geometry'])
        # self.setText(self.__data['content'])

class TextboxPickleable():
    def __init__(self,name, x, y, w, h, t):
        self.name=name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = t
        self.type = WidgetType.TEXT
