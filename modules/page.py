from models.notebook import *
from modules.section import *

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# When a user creates a new page
# 1 Call page.build_page to build a Widget and add to the sidebar (Page list)
# 2 Add Page object to models.notebook.Notebook
def add_page(editor):
    title, accept = QInputDialog.getText(editor, 'New Page Title', 'Enter title of new page: ')
    if accept:
        build_page(editor, title)
        editor.notebook.page.append(Page(title))
        add_page_change(editor)
        editor.section = -1
        add_section(editor)
        editor.sections.itemAt(0).widget().setStyleSheet("background-color: #c2c2c2")

# Create page widget in sidebar when
# Case 1: When Notebook is loaded
# Case 2: When new Page is created by user
def build_page(editor, title):
    page = QTextEdit(title)
    page = QPushButton(title)
    #page.clicked.connect(lambda: change_page(editor))
    #page.mousePressEvent = lambda editor: change_page(editor)
    page.mousePressEvent = lambda x: page_menu(editor, x)
    #page.setContextMenuPolicy(Qt.CustomContextMenu)
    #page.customContextMenuRequested.connect(lambda: page_menu(editor))
    page.setObjectName(title)
    editor.pages.addWidget(page)

# Destroys all Section and Object widgets for current page
# Creates widgets from new page, Section[0]
def change_page(editor):
    # Save current section in models.notebook.Notebook
    if len(editor.object) > 0:
        store_section(editor)

    # Destroy all Widgets (TextBox, ImageObj, etc.)
    if len(editor.object) > 0:
        for o in range(len(editor.object)):
            editor.object[o].deleteLater()

    # Empty list of Widgets in editor
    editor.object.clear()

    # Destroy all Section Widgets on current Page
    if len(editor.notebook.page[editor.page].section) > 0:
        for s in range(len(editor.notebook.page[editor.page].section)):
            editor.sections.itemAt(s).widget().deleteLater()

    # edtor.page is set to new page
    for p in range(len(editor.notebook.page)):
        editor.pages.itemAt(p).widget().setStyleSheet("background-color: #f0f0f0")
        if(editor.focusWidget().objectName() == editor.notebook.page[p].title):
            editor.pages.itemAt(p).widget().setStyleSheet("background-color: #c2c2c2")
            editor.page = p
    # Above can probably be improved

    # Build all Section Widgets on current Page
    if len(editor.notebook.page[editor.page].section) > 0:
        for s in range(len(editor.notebook.page[editor.page].section)):
            build_section(editor, editor.notebook.page[editor.page].section[s].title)

    # editor.section is set to Section[0]
    # build all objects on Page[x], Section[0]
    if(len(editor.notebook.page[editor.page].section)) > 0:
        editor.section = 0
        for o in range(len(editor.notebook.page[editor.page].section[editor.section].object)):
            params = editor.notebook.page[editor.page].section[editor.section].object[o]
            build_object(editor, params)
        #print("objectname", editor.sections.itemAt(editor.section).widget().objectName())
        editor.sections.itemAt(editor.section).widget().setStyleSheet("background-color: #c2c2c2")
    else:
        editor.section = -1

# Variant on above function for CASE: Add New Page
def add_page_change(editor):

    # Save current section in models.notebook.Notebook
    if len(editor.object) > 0:
        store_section(editor)

    # Destroy all Widgets (TextBox, ImageObj, etc.)
    if len(editor.object) > 0:
        for o in range(len(editor.object)):
            editor.object[o].deleteLater()

    # Empty list of Widgets in editor
    editor.object.clear()
    #editor.page = 0
    # Destroy all Section Widgets on current Page
    if len(editor.notebook.page[editor.page].section) > 0:
        print("Page", editor.page)
        for s in range(len(editor.notebook.page[editor.page].section)):
            print("sec index", s)
            editor.sections.itemAt(s).widget().deleteLater()
    print("sec count", editor.sections.count())
    # editor.page is set to new page
    editor.page += 1

    for p in range(len(editor.notebook.page)):
        editor.pages.itemAt(p).widget().setStyleSheet("background-color: #f0f0f0")

    editor.pages.itemAt(editor.page).widget().setStyleSheet("background-color: #c2c2c2")

# Handles Page Clicks
def page_menu(editor, event):

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
    title, accept = QInputDialog.getText(editor, 'Change Page Title', 'Enter new title of new page: ')
    if accept:
        for p in range(len(editor.notebook.page)):
            if editor.focusWidget().objectName() == editor.notebook.page[p].title:
                editor.notebook.page[p].title = title
        editor.focusWidget().setObjectName(title)
        editor.focusWidget().setText(title)

def delete_page(editor):
    print("delete")
    # delete all widgets
    # delete all sections
    # from notebook object and editor
    # go to page 0 section 0 if exists, -1 if DNE