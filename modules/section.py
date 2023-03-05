from models.notebook import *
from modules.object import build_object

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# Refer to page.(add, build, change)_page in Page.py for notes
def add_section(editor):
    title, accept = QInputDialog.getText(editor, 'New Section Title', 'Enter title of new section: ')
    if accept:
        build_section(editor, title)
        editor.notebook.page[editor.page].section.append(Section(title))
        editor.section += 1

def build_section(editor, title):
    section = QPushButton(title)
    #section.clicked.connect(lambda: change_section(editor))
    section.mousePressEvent = lambda x: section_menu(editor, x)
    section.setObjectName(title)
    editor.sections.addWidget(section)

def change_section(editor):
    store_section(editor)

    for o in range(len(editor.object)):
        editor.object[o].deleteLater()
    editor.object.clear()

    for s in range(len(editor.notebook.page[editor.page].section)):
        editor.sections.itemAt(s).widget().setStyleSheet("background-color: #f0f0f0")
        if(editor.focusWidget().objectName() == editor.notebook.page[editor.page].section[s].title):
            editor.sections.itemAt(s).widget().setStyleSheet("background-color: #c2c2c2")
            editor.section = s

    for o in range(len(editor.notebook.page[editor.page].section[editor.section].object)):
        params = editor.notebook.page[editor.page].section[editor.section].object[o]
        build_object(editor, params)

# When a user changes sections (or changes pages, which will cause the section to change)
# Store params from all Widgets into their respective Objects in models.notebook.Notebook
def store_section(editor):
    if(len(editor.notebook.page) > 0 and len(editor.notebook.page[editor.page].section) > 0):
        if(len(editor.notebook.page[editor.page].section[editor.section].object)) > 0:
            for o in range(len(editor.notebook.page[editor.page].section[editor.section].object)):
                if editor.notebook.page[editor.page].section[editor.section].object[o].type == 'text':
                    editor.notebook.page[editor.page].section[editor.section].object[o].text = editor.object[o].toHtml()
                    editor.notebook.page[editor.page].section[editor.section].object[o].x = editor.object[o].geometry().x()
                    editor.notebook.page[editor.page].section[editor.section].object[o].y = editor.object[o].geometry().y()
                    editor.notebook.page[editor.page].section[editor.section].object[o].w = editor.object[o].geometry().width()
                    editor.notebook.page[editor.page].section[editor.section].object[o].h = editor.object[o].geometry().height()
                if editor.notebook.page[editor.page].section[editor.section].object[o].type == 'image':
                    editor.notebook.page[editor.page].section[editor.section].object[o].x = editor.object[o].geometry().x()
                    editor.notebook.page[editor.page].section[editor.section].object[o].y = editor.object[o].geometry().y()
                    editor.notebook.page[editor.page].section[editor.section].object[o].w = editor.object[o].geometry().width()
                    editor.notebook.page[editor.page].section[editor.section].object[o].h = editor.object[o].geometry().height()

def section_menu(editor, event):
    # Change Page
    if event.buttons() == Qt.LeftButton:
        change_section(editor)

    # Open Context Menu
    if event.buttons() == Qt.RightButton:
        section_menu = QMenu(editor)

        rename = QAction("Rename", editor)
        rename.triggered.connect(lambda: rename_section(editor))
        section_menu.addAction(rename)

        delete = QAction("Delete", editor)
        delete.triggered.connect(lambda: delete_section(editor))
        section_menu.addAction(delete)

        section_menu.exec(event.globalPos())

def rename_section(editor):
    title, accept = QInputDialog.getText(editor, 'Change Section Title', 'Enter new title of section: ')
    if accept:
        for s in range(len(editor.notebook.page[editor.page].section)):
            if editor.focusWidget().objectName() == editor.notebook.page[editor.page].section[s].title:
                editor.notebook.page[editor.page].section[s].title = title
        editor.focusWidget().setObjectName(title)
        editor.focusWidget().setText(title)

def delete_section(editor):
    print("delete")
    return