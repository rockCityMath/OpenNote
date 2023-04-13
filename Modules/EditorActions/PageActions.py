# HOW TO UPDATE AND DEAL WITH STATE AND UI
# editor.sections, pages, etc* is UI
# editor.notebook.* is state
# maybe special case for widgets, which handle thier own state and UI

# HOW TO SHOW AND HIDE WIDGETS ON SECTION NAV
# between show() and hide() or deleteLater() and then adding them back on nav
# do show() and hide(), might fuck with multiselect or something

# New Page
# create new page object
# update to that page (ui and indexes (on sections too))
# add a new section to that new page

# Display Page
# build the widget that gets added to the editor visually
# this will be used by new page, and loading a notebook

# Change Page
# hide old sections widgets
# update the page (ui and indexes ( on sections too))
# show the new page's first sections widgets

# Page menu
# menu that gets shown when right clicked (delete, rename)

# Rename page
# change the page name
# update visually

# Delete page
# remove page
# make sure it removes the sections and widgets in those sections
# handle deleting the current page
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from Models.Page import Page

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

# # A page needs to be displayed on the notebook, thru the user adding it or loading it on startup
# # Maybe call this addpage widget or something indicating its ui
# # dont need now?
# def displayPage(self, title):
#     editor = self
#     page = QPushButton(title)
#     page.mousePressEvent = lambda event: editor.handlePageClick(page, event)
#     page.setObjectName(title)
#     editor.pages.addWidget(page)

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

def handlePageClick(self, pageTab, event):
    editor = self
    pageTab.setFocus() #need?

    # Change Page
    if event.buttons() == Qt.LeftButton:
        pageIndex = editor.getPageTabIndex(pageTab)
        editor.goToPage(pageIndex)

    # Open Context Menu
    if event.buttons() == Qt.RightButton:
        pageMenu = QMenu(editor)

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
