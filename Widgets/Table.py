from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from Modules.Enums import TextBoxStyles, WidgetType

class TableWidget(QTableWidget):
    def __init__(self, editor, x, y,w,h, rows, cols):
            super().__init__(rows, cols, editor)
            #self.setEditTriggers(QTableWidget.DoubleClicked) # debt: What is this
            self.rows=rows
            self.cols=cols
            self.editor = editor
            self.type = WidgetType.TABLE
            self.setStyleSheet(TextBoxStyles.OUTFOCUS.value)
            self.setGeometry(x, y, w, h) # This sets geometry of DraggableObject
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.show()

    # Clicking into the cells is offset for some reason, correcting it
    def mouseDoubleClickEvent(self, e):
        corrected_pos = QPoint(e.pos().x()-25, e.pos().y()-35)
        new_event = QMouseEvent(QEvent.MouseButtonDblClick, corrected_pos, e.button(), e.buttons(), e.modifiers())
        self.setFocus()
        self.setStyleSheet(TextBoxStyles.INFOCUS.value) # Not ideal
        QTableWidget.mouseDoubleClickEvent(self, new_event)

class TablePickleable():
    def __init__(self,name, x, y, w, h, rows, cols):
        self.name=name
        self.x = x          
        self.y = y
        self.w = w
        self.h = h
        self.type = WidgetType.TABLE
        self.rows = rows
        self.cols = cols
