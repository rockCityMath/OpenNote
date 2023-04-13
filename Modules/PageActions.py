from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from Models.Notebook import *
from Models.Page import Page
from Modules.SectionActions import *

# When a user creates a new page
# 1 Call page.build_page to build a Widget and add to the sidebar (Page list)
# 2 Add Page object to models.notebook.Notebook
def add_page(editor):
    title, accept = QInputDialog.getText(editor, 'New Page Title', 'Enter title of new page: ')
    if accept:
        for p in range(len(editor.notebook.pages)):
            if title == editor.notebook.pages[p].title:
                error = QMessageBox(editor)
                error.setText("A Page with that name already exists.")
                error.show()
                return
        build_page(editor, title) # Add page widget to sidebar
        editor.notebook.pages.append(Page(title))
        add_page_change(editor)
        editor.sectionIndex = -1
        add_section(editor)
        editor.autosaver.onChangeMade()

# Create page widget in sidebar when
# Case 1: When Notebook is loaded
# Case 2: When new Page is created by user
def build_page(editor, title):
    page = QPushButton(title)
    page.mousePressEvent = lambda x: page_menu(editor, page, x)
    page.setObjectName(title)
    editor.pages.addWidget(page)

# Destroys all Section and Object widgets for current page
# Creates widgets from new page, Section[0]
def change_page(editor):
    # Save current section in models.notebook.Notebook
    # if len(editor.object) > 0:
    #     store_section(editor)

    # new page goto first section
    editor.sectionIndex = 1

    print("CHANGE PAGE")
    print(editor.pageIndex)
    print(editor.sectionIndex)

    print("# Section in page: " + str(len(editor.notebook.pages[editor.pageIndex].sections)))

    # NEW: Hide objects on old page's section
    currentSectionObjects = editor.notebook.pages[editor.pageIndex].sections[editor.sectionIndex].objects
    if len(currentSectionObjects) > 0:
        for o in currentSectionObjects:
            print("HIDING OLD PAGE OBJECT")
            o.hide()

    # Destroy all Widgets (TextBox, ImageObj, etc.)
    # if len(editor.object) > 0:
    #     for o in range(len(editor.object)):
    #         editor.object[o].deleteLater()

    # Empty list of Widgets in editor
    # editor.object.clear()

    # Destroy all Section Widgets on current Page
    # if len(editor.notebook.page[editor.page].section) > 0:
    #     for s in range(len(editor.notebook.page[editor.page].section)):
    #         editor.sections.itemAt(s).widget().deleteLater()

    # Update UI, set new page index
    for p in range(len(editor.notebook.pages)):
        editor.pages.itemAt(p).widget().setStyleSheet("background-color: #f0f0f0")
        if(editor.focusWidget().objectName() == editor.notebook.pages[p].title):
            print("UPDATING PAGE")
            editor.pages.itemAt(p).widget().setStyleSheet("background-color: #c2c2c2")
            editor.pageIndex = p
    # Above can probably be improved

    # Build all Section Widgets on current Page
    # if len(editor.notebook.page[editor.page].section) > 0:
    #     for s in range(len(editor.notebook.page[editor.page].section)):
    #         build_section(editor, editor.notebook.page[editor.page].section[s].title)

    # Show all objects on new page's first section
    newSectionObjects = editor.notebook.pages[editor.pageIndex].sections[editor.sectionIndex].objects
    for o in newSectionObjects:
        print("SHOWING NEW PAGE OBJECT")
        o.show()

    # editor.section is set to Section[0]
    # build all objects on Page[x], Section[0]
    # if(len(editor.notebook.page[editor.page].section)) > 0:
    #     editor.section = 0
    #     for o in range(len(editor.notebook.page[editor.page].section[editor.section].object)):
    #         params = editor.notebook.page[editor.page].section[editor.section].object[o]
    #         build_object(editor, params)
    #     editor.sections.itemAt(editor.section).widget().setStyleSheet("background-color: #c2c2c2")
    # else:
    #     editor.section = -1

# Run after a new page is built
def add_page_change(editor):

    firstPage = False
    if editor.pageIndex == -1:
        firstPage = True

    # Hide objects on old page
    if not firstPage:
        print("NEW PAGE CHANGE ")
        currentSectionObjects = editor.notebook.pages[editor.pageIndex].sections[editor.sectionIndex].objects
        if len(currentSectionObjects) > 0:
            for o in currentSectionObjects:
                print("HIDING OLD PAGE OBJECT")
                o.hide()

    # Set other page tabs to white
    for p in range(len(editor.notebook.pages)):
        print(len(editor.notebook.pages))
        editor.pages.itemAt(p).widget().setStyleSheet("background-color: #f0f0f0")

    # Set current page tab to grey - if theres one page, its because it just got added and its the only one
    if not firstPage:
        editor.pages.itemAt(editor.pageIndex).widget().setStyleSheet("background-color: #c2c2c2")

    # Update UI, set new page index
    for p in range(len(editor.notebook.pages)):
        editor.pages.itemAt(p).widget().setStyleSheet("background-color: #f0f0f0")
        if(editor.focusWidget().objectName() == editor.notebook.pages[p].title):
            print("UPDATING PAGE")
            editor.pages.itemAt(p).widget().setStyleSheet("background-color: #c2c2c2")
            editor.pageIndex = p

    if firstPage:
        editor.pages.itemAt(0).widget().setStyleSheet("background-color: #c2c2c2")
        editor.pageIndex = 1

    # Show all objects on new page's first section
    if not firstPage:
        newSectionObjects = editor.notebook.pages[editor.pageIndex].sections[editor.sectionIndex].objects
        for o in newSectionObjects:
            print("SHOWING NEW PAGE OBJECT")
            o.show()

# Handles Page Clicks
def page_menu(editor, page, event):
    page.setFocus()
    # Change Page
    if event.buttons() == Qt.LeftButton:
        change_page(editor)

    # Open Context Menu
    if event.buttons() == Qt.RightButton:
        page_menu = QMenu(editor)

        rename = QAction("Rename", editor)
        rename.triggered.connect(lambda: rename_page(editor))
        page_menu.addAction(rename)

        delete = QAction("Delete", editor)
        delete.triggered.connect(lambda: delete_page(editor))
        page_menu.addAction(delete)

        page_menu.exec(event.globalPos())

def rename_page(editor):
    title, accept = QInputDialog.getText(editor, 'Change Page Title', 'Enter new title of page: ')
    if accept:
        for p in range(len(editor.notebook.page)):
            if title == editor.notebook.page[p].title:
                error = QMessageBox(editor)
                error.setText("A Page with that name already exists.")
                error.show()
                return
        for p in range(len(editor.notebook.page)):
            if editor.focusWidget().objectName() == editor.notebook.page[p].title:
                editor.notebook.page[p].title = title
        editor.focusWidget().setObjectName(title)
        editor.focusWidget().setText(title)
        editor.autosaver.onChangeMade()
        # cmd = Undo({'object_name': editor.focusWidget().objectName(),'type':'page','name':title, 'action':'rename_page'})
        # editor.undo_stack.append(cmd)

def delete_page(editor):
    accept = QMessageBox.question(editor, 'Delete Page', 'Deleting this page will delete all sections and objects inside it. Are you sure you want to delete it?')
    if accept == QMessageBox.Yes:

        for p in range(len(editor.notebook.page)):
            if editor.focusWidget().objectName() == editor.notebook.page[p].title:

                # Remove page from sidebar
                editor.pages.itemAt(p).widget().deleteLater()

                # If current page is deleted, remove widgets from editor
                if editor.page == p:

                    if(len(editor.notebook.page[p].section)) > 0:
                        # Destroy all Sections
                        for s in range(len(editor.notebook.page[p].section)):
                            editor.sections.itemAt(s).widget().deleteLater()

                        if(len(editor.notebook.page[p].section[editor.section].object)) > 0:
                            # Destory all Objects
                            for o in range(len(editor.notebook.page[p].section[editor.section].object)):
                                editor.object[o].deleteLater()
                            editor.object.clear()

                # Remove objects from model

                #Remove all objects from all sections in Page[del]
                for s in range(len(editor.notebook.page[p].section)):
                        if len(editor.notebook.page[p].section[s].object) > 0:
                            editor.notebook.page[p].section[s].object.clear()

                # Remove all sections from Page[del]
                editor.notebook.page[p].section.clear()

                # Remove Page[del] from Notebook
                editor.notebook.page.pop(p)

                # Set current page and section to 0 if exists, build widgets if exists
                # If DNE, set page/section to -1
                if editor.page == p:
                    if len(editor.notebook.page) > 0:
                        # Select Page[0] if exists
                        editor.page = 0

                        # Highlight Page[0]
                        for p in range(editor.pages.count()):
                            editor.pages.itemAt(p).widget().setStyleSheet("background-color: #f0f0f0")
                        editor.pages.itemAt(0).widget().setStyleSheet("background-color: #c2c2c2")

                        # Build Sections, Widgets select Section[0] if exists
                        if len(editor.notebook.page[0].section) > 0:
                            for s in range(len(editor.notebook.page[0].section)):
                                params = editor.notebook.page[0].section[s]
                                build_section(editor, params.title)
                                editor.sections.itemAt(s).widget().setStyleSheet("background-color: #f0f0f0")
                            editor.section = 0
                            editor.sections.itemAt(editor.section).widget().setStyleSheet("background-color: #c2c2c2")

                            #CASE: Page[0]/Section[0] Exists: Build Widgets in Section[0]
                            for o in range(len(editor.notebook.page[0].section[0].object)):
                                params = editor.notebook.page[0].section[0].object[o]
                                build_object(editor, params)
                        else:
                            editor.section = -1
                    else:
                        editor.page = -1
                        editor.section = -1

                # Stop search for page after found (can cause index OOB w/o)
                return
        editor.autosaver.onChangeMade()

