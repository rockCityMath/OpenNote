from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtTest import *

from collections import deque
from functools import partial
# Should connect to a SectionView, or emit event or something so we can show section tabs
from typing import List
import pprint

from Models.PageModel import PageModel

class PageView(QWidget):
    def __init__(self, pageModels: List[PageModel]):
        super(PageView, self).__init__()

        self.pageModels = pageModels

        # The actual tree view
        self.tree = QTreeView(self)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)

        self.tree.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # The model the tree view is displaying
        self.model = QStandardItemModel()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(10)
        self.tree.setModel(self.model)



        self.tree.viewport().installEventFilter(self)
        # self.tree.dataChanged = self.renamePage
        self.tree.currentChanged = self.changePage

        self.tree.setFixedHeight(1000) # Im sorry

        self.loadPages(pageModels)

    # Event filter for the tree views viewport????, so that we can stop it from selecting items on right click
    # But still allow click events to pass to the collapse buttons (insane...)
    def eventFilter(self, source, event):
        if event.type() == QMouseEvent.MouseButtonPress:
            if(event.button() == Qt.RightButton):
                print("kill mouse press")
                return True
        return False

    def loadPages(self, pageModels: List[PageModel]):
        self.model.setRowCount(0)
        root = self.model.invisibleRootItem()

        # If no data was passed in (new notebook), create the root page
        if not pageModels: # dupplicate stuff here
            rootPageModel = PageModel.newRootPage()
            newPage = QStandardItem(rootPageModel.title)
            newPage.setData(rootPageModel)
            newPage.setEditable(False)
            newPage.setSelectable(False)
            root.appendRow([newPage])

            self.pageModels = pageModels
            self.pageModels.append(rootPageModel)
            return

        seen = {} # QStandardItem list
        values = deque(pageModels)

        # Computer Science | Turn our pages with parent refs into a tree
        while values:
            value = values.popleft()
            if value.uuid == 0:                                     # Add the root page, and make it uneditable
                parent = root

                unique_id = value.uuid
                newPage = QStandardItem(value.title)
                newPage.setEditable(False)
                newPage.setSelectable(False)
                newPage.setData(value)
                parent.appendRow([newPage])
                seen[unique_id] = parent.child(parent.rowCount() - 1)
                continue
            else:
                pid = value.parentUuid
                if pid not in seen:                               # Add to the end of the list so we can add it when we know what its parent is
                    values.append(value)
                    continue
                parent = seen[pid]                                # When we've seen a pages parent, add it to the correct location in the tree
            unique_id = value.uuid
            newPage = QStandardItem(value.title)
            newPage.setData(value)
            parent.appendRow([newPage])
            seen[unique_id] = parent.child(parent.rowCount() - 1)

        self.tree.expandAll()
        self.pageModels = pageModels                             # Update the reference to the pageModels (in case we are loading new pages)

    def openMenu(self, position):
        indexes = self.sender().selectedIndexes()
        clickedIndex = self.tree.indexAt(position)

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
        addChildAction = menu.addAction(self.tr("Add Page"))
        addChildAction.triggered.connect(partial(self.addPage, level, clickedIndex))

        if item.data().uuid != 0:   # Dont delete the root page
            deletePageAction = menu.addAction(self.tr("Delete Page"))
            deletePageAction.triggered.connect(partial(self.deletePage, item))

            renamePageAction = menu.addAction(self.tr("Rename Page"))
            renamePageAction.triggered.connect(partial(self.renamePage, item))
        menu.exec_(self.sender().viewport().mapToGlobal(position))

    def addPage(self, level, clickedIndex):

        # New page added under parent (what the user right clicked on)
        parentPage = self.model.itemFromIndex(clickedIndex)
        parentPageModel = parentPage.data()

        # Create a new page model, set that as the data for the new page
        newPageModel = PageModel('New Page', parentPageModel.uuid)
        newPage = QStandardItem(newPageModel.title)
        newPage.setData(newPageModel)
        parentPage.appendRow([newPage])      # Add to UI
        self.pageModels.append(newPageModel)  # Add to array of PageModel

        self.tree.expand(clickedIndex)

    def deletePage(self, page):
        pageModel = page.data()
        self.pageModels.remove(pageModel)     # Remove from array of PageModel
        page.parent().removeRow(page.row())  # Remove from UI

    def renamePage(self, page):
        print("RENAME")
        print(page)



        page.setText("Renamed")
        print(page.text())
        pageModel = page.data()
        pageIndex = self.pageModels.index(pageModel)
        self.pageModels[pageIndex].title = "Renamed"
        self.update()


    def changePage(self, current, previous):
        print("CHANGEPAGE")

        # Dont select invalid pages
        if not current.isValid() or not previous.isValid():
            return

        # Dont select root page
        if self.model.itemFromIndex(current).data().uuid == 0:
            selection = self.tree.selectionModel()
            selection.setCurrentIndex(previous, QItemSelectionModel.SelectCurrent)
            return

        # Make sure the selected item actually looks selected - improve this
        prev = self.model.itemFromIndex(previous)
        cur = self.model.itemFromIndex(current)
        cur.setBackground(QColor(193,220,243))
        prev.setBackground(QColor('#f0f0f0'))
        self.update()

        newPage = self.model.itemFromIndex(current)
        print(newPage.data().title)



