from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from Models.PageModel import PageModel

from typing import List
from collections import deque
from functools import partial

from Modules.EditorSignals import editorSignalsInstance

# Should connect to a SectionView, or emit event or something so we can show section tabs

# Page view and controller
class PageView(QWidget):
    def __init__(self, pageModels: List[PageModel]):
        super(PageView, self).__init__()

        self.pageModels: List[PageModel] # Reference to the array of page models

        # The actual tree widget
        self.tree = QTreeView(self)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)

        self.tree.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # The layout that holds the view
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)
        layout.setContentsMargins(0, 10, 0, 0)

        # The model used to build a tree (not a domain related persistant one like PageModel, etc)
        self.model = QStandardItemModel()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(10)
        self.tree.setModel(self.model)

        self.tree.viewport().installEventFilter(self)
        self.tree.currentChanged = self.changePage

        self.loadPages(pageModels)
        print("BUILT PAGEVIEW")

    def loadPages(self, pageModels: List[PageModel]):
        self.model.setRowCount(0)
        root = self.model.invisibleRootItem()

        # If no data was passed in (new notebook), create the root page
        if not pageModels:
            rootPageModel = PageModel.newRootPage()
            rootPage = QStandardItem(rootPageModel.title)
            rootPage.setData(rootPageModel)
            rootPage.setEditable(False)
            rootPage.setSelectable(False)
            root.appendRow([rootPage])

            self.pageModels = pageModels
            self.pageModels.append(rootPageModel)
            return

        seen: List[QStandardItemModel] = {}
        values = deque(pageModels) # double ended queue[PageModel]

        # Computer Science | Turn our pages with parent refs into a tree
        while values:
            value = values.popleft()
            if value.isRoot():                                     # Add the root page, and make it unselectable
                parent = root

                unique_id = value.getUUID()
                newPage = QStandardItem(value.title)
                newPage.setEditable(False)
                newPage.setSelectable(False)
                newPage.setData(value)
                parent.appendRow([newPage])
                seen[unique_id] = parent.child(parent.rowCount() - 1)
                continue
            else:
                pid = value.getParentUUID()
                if pid not in seen:                               # Add to the end of the list so we can add it when we know what its parent is
                    values.append(value)
                    continue
                parent = seen[pid]                                # When we've seen a page's parent, add it to the correct location in the tree
            unique_id = value.getUUID()
            newPage = QStandardItem(value.title)
            newPage.setData(value)
            newPage.setEditable(False)
            parent.appendRow([newPage])
            seen[unique_id] = parent.child(parent.rowCount() - 1)

        self.tree.expandAll()
        self.pageModels = pageModels    # Update the view's stored reference to the pageModels (in case we are loading new pages)

    def openMenu(self, position: QModelIndex):
        indexes = self.sender().selectedIndexes()
        clickedIndex = self.tree.indexAt(position)

        if not clickedIndex.isValid():
            return
        page = self.model.itemFromIndex(clickedIndex)
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

        if not page.data().isRoot():   # Dont delete the root page
            deletePageAction = menu.addAction(self.tr("Delete Page"))
            deletePageAction.triggered.connect(partial(self.deletePage, page))

            renamePageAction = menu.addAction(self.tr("Rename Page"))
            renamePageAction.triggered.connect(partial(self.renamePage, page))
        menu.exec_(self.sender().viewport().mapToGlobal(position))

    # Event filter for the tree view's viewport
    # So that we can stop it from selecting items on right click, but still allow click events to pass to the collapse button
    def eventFilter(self, source, event):
        if event.type() == QMouseEvent.MouseButtonPress:
            if(event.button() == Qt.RightButton):
                return True
        return False

    def addPage(self, level: int, clickedIndex: QModelIndex):

        # New page added under parent (what the user right clicked on)
        parentPage = self.model.itemFromIndex(clickedIndex)
        parentPageUUID = parentPage.data().getUUID()

        # Create a new page model, set that as the data for the new page
        newPageModel = PageModel('New Page', parentPageUUID)
        newPage = QStandardItem(newPageModel.title)
        newPage.setData(newPageModel)
        newPage.setEditable(False)
        parentPage.appendRow([newPage])       # Add to UI
        self.pageModels.append(newPageModel)  # Add to array of PageModel

        self.tree.expand(clickedIndex)

    def deletePage(self, page: QStandardItem):
        deletePages = [page]
        deletePages += self.getPageChildren(page)
        for p in deletePages:
            pageModel = p.data()
            self.pageModels.remove(pageModel)     # Remove parent and all child PageModels
        page.parent().removeRow(page.row())       # Remove from UI

    # Recursively build a list of all the given pages children
    def getPageChildren(self, page: QStandardItem):
        childPages = []
        for row in range(0, page.rowCount()): # mb doesnt need 0 (range(page.rowCount()))
            childPage = page.child(row)
            childPages.append(childPage)
            childPages += self.getPageChildren(childPage)
        return childPages

    def renamePage(self, page: QStandardItem):
        newName, accept = QInputDialog.getText(self, 'Change Page Title', 'Enter new title of page: ')
        if accept:
            page.setText(newName)                              # Rename in UI
            pageModel = page.data()
            pageModelIndex = self.pageModels.index(pageModel)
            self.pageModels[pageModelIndex].title = newName    # Rename in array of PageModel
            self.update()

    def changePage(self, current: QModelIndex, previous: QModelIndex):

        # Dont select invalid pages
        if not current.isValid() or not previous.isValid():
            return

        # Dont select root page
        if self.model.itemFromIndex(current).data().isRoot():
            selection = self.tree.selectionModel()
            selection.setCurrentIndex(previous, QItemSelectionModel.SelectCurrent)
            return

        # Make sure the selected item actually looks selected - improve this
        # I think it just needs to make sure the real selected item is highlighted and all others are not
        prev = self.model.itemFromIndex(previous)
        cur = self.model.itemFromIndex(current)
        cur.setBackground(QColor(193,220,243))
        prev.setBackground(QColor('white'))
        self.update()

        newPage = self.model.itemFromIndex(current) # could save selected page
        print("NEW PAGE: " + newPage.data().title)

        editorSignalsInstance.pageChanged.emit(newPage.data())
