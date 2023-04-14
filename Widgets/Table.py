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
        
    def add_column(self):
        # Get the current number of columns in the table
        num_cols = self.columnCount()

        # Insert a new column at the end of the table
        self.insertColumn(num_cols)

        # Update the number of columns in the table
        self.cols += 1
        
    def delete_col(self):
        # Get the selected row index
        selected_col = self.currentRow()

        # Remove the selected row from the table
        self.removeColumn(selected_col)

        # Update the number of rows in the table
        self.cols -= 1
         
    def add_row(self):
        # Get the current number of rows in the table
        num_rows = self.rowCount()

        # Insert a new row at the end of the table
        self.insertRow(num_rows)

        # Update the number of rows in the table
        self.rows += 1
        
    def delete_row(self):
        # Get the selected row index
        selected_row = self.currentRow()

        # Remove the selected row from the table
        self.removeRow(selected_row)

        # Update the number of rows in the table
        self.rows -= 1

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
