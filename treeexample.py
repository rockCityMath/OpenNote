from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
import sys
from collections import deque
class PageView(QWidget):
    def __init__(self, data):
        super(PageView, self).__init__()

        # The actual tree view
        self.tree = QTreeView(self)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)

        # The layout the tree view is in
        layout = QVBoxLayout()
        layout.addWidget(self.tree)

        # The model the tree view is displaying
        self.model = QStandardItemModel()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(10)
        self.tree.setModel(self.model)

        data = [
            {'unique_id': 1, 'parent_id': 0, 'page_name': 'Notebook Pages'},
            {'unique_id': 2, 'parent_id': 1, 'page_name': 'Class 1'},
            {'unique_id': 3, 'parent_id': 2, 'page_name': 'Lucy'},
            {'unique_id': 4, 'parent_id': 2, 'page_name': 'Joe'},
            {'unique_id': 5, 'parent_id': 1, 'page_name': 'Class 2'},
            {'unique_id': 6, 'parent_id': 5, 'page_name': 'Lily'},
            {'unique_id': 7, 'parent_id': 5, 'page_name': 'Tom'},
            {'unique_id': 8, 'parent_id': 1, 'page_name': 'Class 3'},
            {'unique_id': 9, 'parent_id': 8, 'page_name': 'Jack'},
            {'unique_id': 10, 'parent_id': 8, 'page_name': 'Tim'},
        ]

        self.loadData(data)
        self.tree.expandAll()

    # Load a dict into treeview
    def loadData(self, data):
        self.model.setRowCount(0)
        root = self.model.invisibleRootItem()

        seen = {}
        values = deque(data)

        while values:
            value = values.popleft()
            if value['unique_id'] == 1:
                parent = root
            else:
                pid = value['parent_id']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            unique_id = value['unique_id']
            parent.appendRow([
                QStandardItem(value['page_name']),
            ])
            seen[unique_id] = parent.child(parent.rowCount() - 1)

    # When right clicking on a treeview item
    def openMenu(self, position):
        indexes = self.sender().selectedIndexes()
        clickedIndex = self.tree.indexAt(position)

        # Calculates information about the clicked index, for adding things above, below etc??
        if not clickedIndex.isValid():
            return
        item = self.model.itemFromIndex(clickedIndex)
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        else:
            level = 0

        menu = QMenu()
        addChildAction = menu.addAction(self.tr("Add Page")) # self.tr???
        addChildAction.triggered.connect(partial(self.addPage, level, clickedIndex))

        if item.parent != None:
            deletePageAction = menu.addAction(self.tr("Delete Page"))
            deletePageAction.triggered.connect(partial(self.deletePage, item))
        menu.exec_(self.sender().viewport().mapToGlobal(position))

    def addPage(self, level, clickedIndex):
        tempKey = QStandardItem('xx')
        tempVal = QStandardItem('yy')

        self.model.itemFromIndex(clickedIndex).appendRow([tempKey, tempVal])

    def deletePage(self, page):
        page.parent().removeRow(page.row())




if __name__ == '__main__':
    data = [
        {'unique_id': 1, 'parent_id': 0, 'page_name': 'Notebook Pages'},
        {'unique_id': 2, 'parent_id': 1, 'page_name': 'Class 1'},
        {'unique_id': 3, 'parent_id': 2, 'page_name': 'Lucy'},
        {'unique_id': 4, 'parent_id': 2, 'page_name': 'Joe'},
        {'unique_id': 5, 'parent_id': 1, 'page_name': 'Class 2'},
        {'unique_id': 6, 'parent_id': 5, 'page_name': 'Lily'},
        {'unique_id': 7, 'parent_id': 5, 'page_name': 'Tom'},
        {'unique_id': 8, 'parent_id': 1, 'page_name': 'Class 3'},
        {'unique_id': 9, 'parent_id': 8, 'page_name': 'Jack'},
        {'unique_id': 10, 'parent_id': 8, 'page_name': 'Tim'},
    ]

    app = QApplication(sys.argv)
    view = PageView(data)
    view.setGeometry(300, 300, 900, 300)
    view.setWindowTitle('QTreeview Example')
    view.show()
    sys.exit(app.exec_())



getline(cin, nameVarible)


