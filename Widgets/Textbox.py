from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from Modules.Enums import TextBoxStyles, WidgetType

class TextboxWidget(QTextEdit):
    # NEW: Can either specify w, h, content or let it default
    def __init__(self, x, y, w = 100, h = 100, t = 'new text!'):
        super().__init__()

        # self.type = 'text'
        self.setStyleSheet(TextBoxStyles.OUTFOCUS.value) # debt: this gets set all over the place
        self.setGeometry(x, y, w, h) # This sets geometry of DraggableObject, I think
        self.setText(t)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.show()

        self.persistGeometry = self.geometry()

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

    # all widgets implement? needed?
    def newGeometryEvent(self, newGeometry):
        self.persistGeometry = newGeometry

    # also all widgets implement? and move this
    @staticmethod
    def new(clickPos: QPoint):
        return TextboxWidget(clickPos.x(), clickPos.y())

    def __getstate__(self):
        data = {}
        data['geometry'] = self.persistGeometry # this is wierd
        data['content'] = self.toHtml()
        return data

    def __setstate__(self, data):
        self.__init__(data['geometry'].x(), data['geometry'].y(), data['geometry'].width(), data['geometry'].height(), data['content'])
