from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class TableWidget(QWidget):
    def __init__(self, x, y, w, h, rows, cols):
        super(TableWidget, self).__init__()

        # The actual table widget
        self.table = QTableWidget(rows, cols, self)
        # Hide the horizontal and vertical headers
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)

        # Get the default table border color from the palette
        table_border_color = self.palette().color(QPalette.Window)

        # Add a custom border on the top of the widget
        self.table.setStyleSheet(f"QTableView {{border: 1px solid {table_border_color.name()};}}")
           
        # Make the cells resizable
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setGeometry(x, y, w, h)
        self.table.setGeometry(0, 0, w, h)
        self.resize(w, h)
        self.persistantGeometry = self.geometry()
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True) # If extending a qwidget to insert something else, dont receive mouse events

    # Child widget not concerned with pos but is with w, h
    def newGeometryEvent(self, newGeometry: QRect):
        self.table.resize(newGeometry.width(), newGeometry.height())
        self.persistantGeometry = newGeometry
        return

    def addRow(self):
        self.table.insertRow(self.table.rowCount())

    def addCol(self):
        self.table.insertColumn(self.table.columnCount())

    @staticmethod
    def new(clickPos: QPoint):
        return TableWidget(clickPos.x(), clickPos.y(), 200, 200, 2, 2)

    def customMenuItems(self):
        addRow = QAction("Add Row", self)
        addRow.triggered.connect(self.addRow)

        addCol = QAction("Add Column", self)
        addCol.triggered.connect(self.addCol)

        return [addRow, addCol]

    def __getstate__(self):
        state = {}

        t = self.table
        rowCnt = t.rowCount()
        colCnt = t.columnCount()
        tableData = [["" if t.item(i, j) == None else t.item(i, j).text() for i in range(rowCnt)] for j in range(colCnt)] # :)

        state['tableData'] = tableData
        state['geometry'] = self.parentWidget().geometry() # Can get whole geometry from parent, or just the pos
        return state

    def __setstate__(self, state):
        self.__init__(state['geometry'].x(),
                      state['geometry'].y(),
                      state['geometry'].width(),
                      state['geometry'].height(),
                      len(state['tableData'][0]),
                      len(state['tableData']))

        rowCnt = len(state['tableData'][0])
        colCnt = len(state['tableData'])

        for i in range(colCnt):
            for j in range(rowCnt):
                self.table.setItem(j, i, QTableWidgetItem(state['tableData'][i][j]))
