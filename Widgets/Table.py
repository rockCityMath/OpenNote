from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from Modules.Enums import TextBoxStyles, WidgetType

class TableWidget(QTableWidget):
    def __init__(self, editor, x, y,w,h, rows, cols,t=[]):
            super().__init__(rows, cols, editor)
            #self.setEditTriggers(QTableWidget.DoubleClicked) # debt: What is this
            self.rows=rows
            self.cols=cols
            self.editor = editor
            self.t = [[0 for j in range(cols)] for i in range(rows)]
            self.type = WidgetType.TABLE
            self.setStyleSheet(TextBoxStyles.OUTFOCUS.value)
            self.setGeometry(x, y, w, h) # This sets geometry of DraggableObject
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.show()
            self.cellChanged.connect(self.on_cell_changed)
            
    # Clicking into the cells is offset for some reason, correcting it
    def mouseDoubleClickEvent(self, e):
        corrected_pos = QPoint(e.pos().x()-25, e.pos().y()-35)
        new_event = QMouseEvent(QEvent.MouseButtonDblClick, corrected_pos, e.button(), e.buttons(), e.modifiers())
        self.setFocus()
        self.setStyleSheet(TextBoxStyles.INFOCUS.value) # Not ideal
        QTableWidget.mouseDoubleClickEvent(self, new_event)
    
    def on_cell_changed(self, row, col):
        value = self.item(row, col).text()
        self.t[row][col] = value

class TablePickleable():
    def __init__(self,name, x, y, w, h, rows, cols, t=[]):
        self.name=name
        self.x = x          
        self.y = y
        self.w = w
        self.h = h
        
        self.t = [[0 for j in range(cols)] for i in range(rows)]
        self.type = WidgetType.TABLE
        self.rows = rows
        self.cols = cols
