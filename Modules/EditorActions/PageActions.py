from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# User requests to add a new page to the notebook
def addPage(self):
    editor = self
    title, accept = QInputDialog.getText(editor, 'New Page Title', 'Enter title of new page: ')
    if accept:
        for p in range(len(editor.notebook.pages)):
            if title == editor.notebook.pages[p].title:
                error = QMessageBox(editor)
                error.setText("A Page with that name already exists.")
                error.show()
                return

        # should append and show the page
        editor.notebook.pages.append(Page(editor, title))
        # editor.displayPage(title)

        # NEED TO ADD SECTION HERE
        print("WILL ADD SECTION")
        # add_section(editor)

        # Switch to new page
        newPageIndex = len(editor.notebook.pages) - 1 #i think theyre 0 index?
        editor.goToPage(newPageIndex)

        editor.autosaver.onChangeMade()

        print("ADD PAGE COMPLETE")
        print("NEW PAGE INDEX: " + str(editor.pageIndex))
        print("NEW PAGE COUNT: " + str(len(editor.notebook.pages)))
        print("NEW SECTION COUNT: " + str(len(editor.notebook.pages[editor.pageIndex].sections)))

def goToPage(self, pageIndex):
    editor = self

    # mb check if its actually a diff page
    # if pageindex == editor.pageindex

    # BRING BACK WHEN SECTIONS CAN BE ADDED
    # Hide widgets on the current page's section
    # currentWidgets = editor.notebook.pages[editor.pageIndex].sections[editor.sectionIndex].widgets # kind of mixing state and ui
    # for w in currentWidgets:
    #     w.hide()

    # Set new page tab to active color, others to inactive
    for p in range(len(editor.notebook.pages)):
        if p == pageIndex:
            editor.notebook.pages[p].tabWidget.setStyleSheet("background-color: #C2C2C2")
        else:
            editor.notebook.pages[p].tabWidget.setStyleSheet("background-color: #F0F0F0")

    # BRING BACK
    # Show page's first section's widgets
    # newWidgets = editor.notebook.pages[pageIndex].sections[0].widgets
    # for w in newWidgets:
    #     w.show()

    # Set new page and section indexes
    editor.pageIndex = pageIndex
    editor.sectionIndex = 0

    # Set new page's first section to active color, others to inactive (could move to a section function)
    # for s in range(len(editor.notebook.pages[pageIndex].sections)):
    #     if s == 0:
    #         editor.sections[s].widget().setStyleSheet("background-color: #F0F0F0")
    #     else:
    #         editor.sections[s].widget().setStyleSheet("background-color: #C2C2C2")

    print("GOTO PAGE COMPLETE")
    print("NEW PAGE INDEX: " + str(editor.pageIndex))
    print("NEW PAGE COUNT: " + str(len(editor.notebook.pages)))
    print("NEW SECTION COUNT: " + str(len(editor.notebook.pages[editor.pageIndex].sections)))

def handlePageClick(self, pageTab, page, event):
    editor = self
    pageTab.setFocus() #need?

    # Change Page
    if event.buttons() == Qt.LeftButton:
        pageIndex = editor.getPageTabIndex(pageTab)
        editor.goToPage(pageIndex)

    # Open Context Menu
    if event.buttons() == Qt.RightButton:
        pageMenu = QMenu(editor)

        addPage = QAction("Add Page", editor)
        addPage.triggered.connect(lambda: page.addChildPage(editor))
        pageMenu.addAction(addPage)

        rename = QAction("Rename", editor)
        rename.triggered.connect(lambda: editor.renamePage(pageTab))
        pageMenu.addAction(rename)

        delete = QAction("Delete", editor)
        delete.triggered.connect(lambda: editor.deletePage(pageTab))
        pageMenu.addAction(delete)

        pageMenu.exec(event.globalPos())

# need to rename visually and in notebook
def renamePage(self, pageTab):
    editor = self
    title, accept = QInputDialog.getText(editor, 'Change Page Title', 'Enter new title of page: ')
    if accept:
        for p in range(len(editor.notebook.pages)):
            if title == editor.notebook.pages[p].title:
                error = QMessageBox(editor)
                error.setText("A Page with that name already exists.")
                error.show()
                return

        # Update name on widget and in notebook
        pageIndex = editor.getPageTabIndex(pageTab)

        editor.notebook.pages[pageIndex].title = title
        editor.notebook.pages[pageIndex].tabWidget.setObjectName(title)
        editor.notebook.pages[pageIndex].tabWidget.setText(title)

        editor.autosaver.onChangeMade()

def deletePage(self, pageTab):
    editor = self
    pageIndex = editor.getPageTabIndex(pageTab)
    newPageIndex = 0

    # If removing the current page
    if editor.pageIndex == pageIndex:
        if len(editor.notebook.pages) > 1:   # goto another page or if there isnt any set -1 indexes
            if pageIndex == 0:               # if deleting the first page, go to the second, else go to the previous
                newPageIndex = 1
            else:
                newPageIndex = pageIndex - 1
        else:
            newPageIndex = -1 # -1 section index too or is that handled in deleting all section

    # Remove page and it's sections from UI
    # for s in editor.notebook.pages[pageIndex].sections:
    #     s.deleteLater()
    editor.notebook.pages[pageIndex].tabWidget.deleteLater()

    # Have to delete widgets using the notebook attribute
    # for s in editor.notebook.pages[pageIndex].sections:
    #     for w in s.widgets:
    #         w.deleteLater()



    # Remove the page from the notebook, it wont persist anymore
    del[editor.notebook.pages[pageIndex]] # maybe = None?

    # If not deleting the last page, go to new page
    if newPageIndex != -1:
        print("WENT TO NEW PAGE: " + str(newPageIndex))
        editor.goToPage(newPageIndex)

        print("PAGE DELETE COMPLETE")
        print("NEW PAGE INDEX: " + str(editor.pageIndex))
        print("NEW PAGE COUNT: " + str(len(editor.notebook.pages)))
        print("NEW SECTION COUNT: " + str(len(editor.notebook.pages[editor.pageIndex].sections)))

    else:
        print("LAST PAGE DELETED")


# Util function to get index of given tab widget
def getPageTabIndex(self, pageTab):
    print("FINDING PAGE INDEX...")
    editor = self
    for p in range(len(editor.notebook.pages)):
        if pageTab == editor.notebook.pages[p].tabWidget:
            print("FOUND PAGE INDEX: " + str(p) + " FOR TITLE: " + editor.notebook.pages[p].title)
            return p
    else:
        print("GIVEN PAGE NOT FOUND IN NOTEBOOK")
        exit()


from functools import partial
from collections import deque

# Should connect to a SectionView

from Models.PageModel import PageModel

# Needs to recieve data in constructor
class PageView(QWidget):
    def __init__(self):
        super(PageView, self).__init__()

        # The actual tree view
        self.tree = QTreeView(self)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)

        self.tree.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # The layout the tree view is in
        # layout = QVBoxLayout()
        # layout.setContentsMargins(100, 0, 0, 0)
        # layout.addWidget(self.tree)

        # The model the tree view is displaying
        self.model = QStandardItemModel()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(10)
        self.tree.setModel(self.model)
        self.tree.dataChanged = self.itemChanged
        # self.tree.setFixedHeight(1000) # Im sorry

        childPage1 = PageModel("Child1")
        childPage2 = PageModel("Child2")
        childPage3 = PageModel("Child3")
        pages = PageModel()

        # Test data
        data = [
            {'unique_id': 1, 'parent_id': 0, 'page_name': 'Notebook Pages'},
            {'unique_id': 2, 'parent_id': 1, 'page_name': 'Bio'},
            {'unique_id': 3, 'parent_id': 2, 'page_name': 'Unit 2'},
            {'unique_id': 4, 'parent_id': 2, 'page_name': 'Quiz'},
            {'unique_id': 5, 'parent_id': 1, 'page_name': 'Math'},
            {'unique_id': 6, 'parent_id': 5, 'page_name': 'Unit Circle'},
            {'unique_id': 7, 'parent_id': 5, 'page_name': 'Formulas'},
            {'unique_id': 8, 'parent_id': 1, 'page_name': 'PE'},
            {'unique_id': 9, 'parent_id': 8, 'page_name': 'Running'},
            {'unique_id': 10, 'parent_id': 8, 'page_name': 'Walking'},
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
            newPage = QStandardItem(value['page_name'])
            parent.appendRow([newPage])
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
        tempKey = QStandardItem('New Page')
        tempVal = QStandardItem('yy')

        parentPage = self.model.itemFromIndex(clickedIndex)
        parentPage.appendRow([tempKey, tempVal])
        self.tree.expand(clickedIndex)

    def deletePage(self, page):
        page.parent().removeRow(page.row())


    def itemChanged(self, topLeftIndex, bottomRightIndex, roles):
        print("TL : " + str(topLeftIndex.column()) + " " + str(topLeftIndex.row()))
        print("ROLES: " + str(roles))
        print("VAL: " + str(self.model.itemFromIndex(topLeftIndex).text()))



