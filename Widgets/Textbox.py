from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from Modules.Enums import TextBoxStyles, WidgetType

class TextboxWidget(QTextEdit):
    def __init__(self, editor, x, y, w, h, t):
        super().__init__(editor)

        self.editor = editor
        self.type = WidgetType.TEXT
        self.setStyleSheet(TextBoxStyles.OUTFOCUS.value) # debt: this gets set everywhere
        self.setGeometry(x, y, w, h) # This sets geometry of DraggableObject
        self.setText(t)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.show()

    # Set the textbox as selected so that the editor can change font attributes
    def mousePressEvent(self, event):
        self.editor.selected = self
        QTextEdit.mousePressEvent(self, event)

    def focusOutEvent(self, event):
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)
        QTextEdit.focusOutEvent(self, event)

    # When user starts typing in new box, expand its size
    def keyPressEvent(self, event):
        if len(self.toPlainText()) == 0:
            self.resize(100, 100)
            self.parentWidget().resize(100, 100)
            self.setStyleSheet(TextBoxStyles.INFOCUS.value)
        QTextEdit.keyPressEvent(self, event)

class TextboxPickleable():
    def __init__(self,name, x, y, w, h, t):
        self.name=name
        self.x = x         
        self.y = y
        self.w = w
        self.h = h
        self.text = t    
        self.type = WidgetType.TEXT