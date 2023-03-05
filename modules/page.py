from models.notebook import *
from modules.section import *

from PySide6.QtWidgets import *

# When a user creates a new page
# 1 Call page.build_page to build a Widget and add to the sidebar (Page list)
# 2 Add Page object to models.notebook.Notebook
def add_page(editor):
    title, accept = QInputDialog.getText(editor, 'New Page Title', 'Enter title of new page: ')
    if accept:
        build_page(editor, title)
        editor.notebook.page.append(Page(title))

# Create page widget in sidebar when
# Case 1: When Notebook is loaded
# Case 2: When new Page is created by user
def build_page(editor, title):
    page = QPushButton(title)
    page.clicked.connect(lambda: change_page(editor))
    page.setObjectName(title)
    editor.pages.addWidget(page)

# Destroys all Section and Object widgets for current page
# Creates widgets from new page, Section[0]
def change_page(editor):
    # Save current section in models.notebook.Notebook
    if len(editor.object) > 0:
        store_section(editor)

    # Destroy all Widgets (TextBox, ImageObj, etc.)
    for o in range(len(editor.object)):
        editor.object[o].deleteLater()

    # Empty list of Widgets in editor
    editor.object.clear()

    # edtor.page is set to new page
    for p in range(len(editor.notebook.page)):
        if(editor.focusWidget().objectName() == editor.notebook.page[editor.page].title):
            editor.page = p
    # Above can probably be improved

    # editor.section is set to Section[0]
    # build all objects on Page[x], Section[0]
    editor.section = 0
    for o in range(len(editor.notebook.page[editor.page].section[editor.section].object)):
        params = editor.notebook.page[editor.page].section[editor.section].object[o]
        build_object(editor, params)