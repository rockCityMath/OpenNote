from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from Models.PageModel import PageModel

from typing import List
from collections import deque
from functools import partial

from Modules.EditorSignals import editorSignalsInstance


# Page view and controller
class PageView(QWidget):
    def __init__(self, pageModels: List[PageModel]):
        super(PageView, self).__init__()

        self.pageModels: List[PageModel]  # Reference to the array of page models

        # The actual tree widget
        self.tree = QTreeView(self)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)

        self.tree.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tree.setStyleSheet("padding-left: 10px;")

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

        # If no data was passed in (new notebook), create the root page, and a first page
        if not pageModels:
            print("CREATING ROOT AND FIRST PAGE")
            rootPageModel = PageModel.newRootPage()
            rootPage = QStandardItem(rootPageModel.title)
            rootPage.setData(rootPageModel)
            rootPage.setEditable(False)
            rootPage.setSelectable(False)
            root.appendRow([rootPage])

            # Create a first page
            newPageModel = PageModel("New Page", 0)
            newPage = QStandardItem(newPageModel.title)
            newPage.setData(newPageModel)
            newPage.setEditable(False)
            rootPage.appendRow([newPage])  # Add to UI

            pageModels.append(newPageModel)  # Add to array of PageModel
            self.pageModels = pageModels  # Update reference to array of PageModel
            self.pageModels.append(rootPageModel)
            self.tree.expandAll()

            # root.child(0).child(0).setBackground(QColor(193,220,243)) # Highlight first page (it's already selected)
            return

        seen: List[QStandardItemModel] = {}
        values = deque(pageModels)  # double ended queue[PageModel]

        # Computer Science | Turn our pages with parent refs into a tree
        while values:
            value = values.popleft()
            if value.isRoot():  # Add the root page, and make it unselectable
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
                if (
                    pid not in seen
                ):  # Add to the end of the list so we can add it when we know what its parent is
                    values.append(value)
                    continue
                parent = seen[
                    pid
                ]  # When we've seen a page's parent, add it to the correct location in the tree
            unique_id = value.getUUID()
            newPage = QStandardItem(value.title)
            newPage.setData(value)
            newPage.setEditable(False)
            parent.appendRow([newPage])
            seen[unique_id] = parent.child(parent.rowCount() - 1)

        # root.child(0).child(0).setBackground(QColor(193,220,243)) # Highlight first page (its selected)
        self.tree.expandAll()  # Mb dont
        self.pageModels = pageModels  # Update the view's stored reference to the pageModels (in case we are loading new pages)

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

        if not page.data().isRoot():  # Dont delete the root page
            deletePageAction = menu.addAction(self.tr("Delete Page"))
            deletePageAction.triggered.connect(partial(self.deletePage, page))

            renamePageAction = menu.addAction(self.tr("Rename Page"))
            renamePageAction.triggered.connect(partial(self.renamePage, page))

            #Current Issue: settings do not save because autosave only saves editor state
            '''
            mergePageAction = menu.addAction(self.tr("Merge Pages"))
            mergePageAction.triggered.connect(partial(self.mergePages, page))
            '''

            changeTextColorAction = menu.addAction(self.tr("Change Text Color"))
            changeTextColorAction.triggered.connect(partial(self.changeTextColor, page))
            
            changeBackgroundColorAction = menu.addAction(self.tr("Change Background Color"))
            changeBackgroundColorAction.triggered.connect(partial(self.changeBackgroundColor, page))
        menu.exec_(self.sender().viewport().mapToGlobal(position))

    # Dont let the right click reach the viewport, context menu will still open but this will stop the page from being selected
    def eventFilter(self, source, event):
        if event.type() == QMouseEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                return True
        return False
    
    def addPage(self, level: int, clickedIndex: QModelIndex):
<<<<<<< HEAD
        # New page added under parent (what the user right clicked on)
=======


        # New page added to root 
        # will add functionallity for page groups which can be nested 
    
>>>>>>> 5b2a7e0a68ed735cf55aee09f0f246d28a28586a
        parentPage = self.model.itemFromIndex(clickedIndex)
        while not parentPage.data().isRoot():
            parentPage = parentPage.parent()
        parentPageUUID = parentPage.data().getUUID()

        # Create a new page model, set that as the data for the new page
        newPageModel = PageModel("New Page", parentPageUUID)
        newPage = QStandardItem(newPageModel.title)
        newPage.setData(newPageModel)
        newPage.setEditable(False)
        parentPage.appendRow([newPage])  # Add to UI
        self.pageModels.append(newPageModel)  # Add to array of PageModel

        self.tree.expand(clickedIndex) 

    def deletePage(self, page: QStandardItem):
        deletePages = [page]
        deletePages += self.getPageChildren(page)
        for p in deletePages:
            pageModel = p.data()
            self.pageModels.remove(pageModel)  # Remove parent and all child PageModels
        page.parent().removeRow(page.row())  # Remove from UI

    # Recursively build a list of all the given pages children
    def getPageChildren(self, page: QStandardItem):
        childPages = []
        for row in range(
            0, page.rowCount()
        ):  # mb doesnt need 0 (range(page.rowCount()))
            childPage = page.child(row)
            childPages.append(childPage)
            childPages += self.getPageChildren(childPage)
        return childPages

    def renamePage(self, page: QStandardItem):
        newName, accept = QInputDialog.getText(
            self, "Change Page Title", "Enter new title of page: "
        )
        if accept:
            page.setText(newName)  # Rename in UI
            pageModel = page.data()
            pageModelIndex = self.pageModels.index(pageModel)
            self.pageModels[
                pageModelIndex
            ].title = newName  # Rename in array of PageModel
            self.update()

    def changePage(self, current: QModelIndex, previous: QModelIndex):
        print("ATTEMPT CHANGE PAGE")

        # Means this is probably the first page change, so prev was first page
        if not previous.isValid():
            previous = self.model.invisibleRootItem().child(0).child(0).index()

        # Dont select root page
        if self.model.itemFromIndex(current).data().isRoot():
            print("ROOT PAGE SELECTED")
            selection = self.tree.selectionModel()
            selection.setCurrentIndex(previous, QItemSelectionModel.SelectCurrent)
            return

        # Make sure the selected item actually looks selected - should improve this
        prev = self.model.itemFromIndex(previous)
        cur = self.model.itemFromIndex(current)
        # cur.setBackground(QColor(193,220,243))
        # prev.setBackground(QColor('white'))
        self.update()

        newPage = self.model.itemFromIndex(current)  # could save selected page
        newPageModel = newPage.data()
        print("CHANGED PAGE TO: " + newPage.data().title)

<<<<<<< HEAD
        editorSignalsInstance.pageChanged.emit(
            newPageModel
        )  # Tell the sectionView that the page has changed
=======
        editorSignalsInstance.pageChanged.emit(newPageModel) # Tell the sectionView that the page has changed

    '''
    #   Not sure if working as intended 
    def mergePages(self):
        # Prompt the user to select two pages
        selectedIndexes = self.tree.selectedIndexes()

        # Check if exactly two pages are selected
        if len(selectedIndexes) == 2:
            # Retrieve the QStandardItem objects corresponding to the selected pages
            page1Item = self.model.itemFromIndex(selectedIndexes[0])
            page2Item = self.model.itemFromIndex(selectedIndexes[1])

            # Extract the PageModel objects from the selected QStandardItem objects
            page1Model = page1Item.data()
            page2Model = page2Item.data()

            # Merge the sections of the two pages into one page
            mergedSections = page1Model.sections + page2Model.sections
            newPageModel = PageModel('Merged Page', 0, mergedSections)  # Assuming 0 as the parent UUID for the root

            # Create a new QStandardItem for the merged page
            newPageItem = QStandardItem(newPageModel.title)
            newPageItem.setData(newPageModel)
            newPageItem.setEditable(False)

            # Insert the new merged page at the bottom of the children of the root
            root = self.model.invisibleRootItem()
            index = root.rowCount()  # Get the last index
            root.insertRow(index, [newPageItem])

            # Remove the original two pages from the model
            root.removeRow(page1Item.row())
            root.removeRow(page2Item.row())

            # Update the pageModels list
            self.pageModels.remove(page1Model)
            self.pageModels.remove(page2Model)
            self.pageModels.append(newPageModel)

            # Expand the tree to show the changes
            self.tree.expandAll()
        else:
            # If not exactly two pages are selected, show a warning or message
            QMessageBox.warning(self, 'Invalid Selection', 'Please select exactly two pages to merge.', QMessageBox.Ok)
    '''
    
    def changeTextColor(self, page: QStandardItem):
        color = QColorDialog.getColor()
        if color.isValid():
            page.setForeground(color)

    def changeBackgroundColor(self, page: QStandardItem):
        color = QColorDialog.getColor()
        if color.isValid():
            page.setBackground(color)
>>>>>>> 5b2a7e0a68ed735cf55aee09f0f246d28a28586a
