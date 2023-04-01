from models.notebook import *
from modules.object import build_object
from modules.undo import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# Refer to page.(add, build, change)_page in Page.py for notes
def add_section(editor):
    if editor.page > -1:
        title, accept = QInputDialog.getText(editor, 'New Section Title', 'Enter title of new section: ')
        if accept:
            for s in range(len(editor.notebook.page[editor.page].section)):
                if title == editor.notebook.page[editor.page].section[s].title:
                    error = QMessageBox(editor)
                    error.setText("A section with that name already exists.")
                    error.show()
                    return
            build_section(editor, title)
            editor.notebook.page[editor.page].section.append(Section(title))
            editor.section += 1
            for s in range(len(editor.notebook.page[editor.page].section)):
                editor.sections.itemAt(s).widget().setStyleSheet("background-color: #f0f0f0")
            editor.sections.itemAt(editor.section).widget().setStyleSheet("background-color: #c2c2c2")
            editor.autosaver.onChangeMade()
    else:
        error = QMessageBox(editor)
        error.setText("Cannot create a section without a page.")
        error.show()

def build_section(editor, title):
    section = QPushButton(title)
    section.mousePressEvent = lambda x: section_menu(editor, section, x)
    section.setObjectName(title)
    editor.sections_frame.setFixedWidth(0)
    editor.sections.addWidget(section)

def change_section(editor, section):
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

def section_menu(editor, section, event):
    section.setFocus()
    # Change Page
    if event.buttons() == Qt.LeftButton:
        change_section(editor, section)

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
        old_name = editor.notebook.page[editor.page].section[s].title
        for s in range(len(editor.notebook.page[editor.page].section)):
            if title == editor.notebook.page[editor.page].section[s].title:
                error = QMessageBox(editor)
                error.setText("A section with that name already exists.")
                error.show()
                return
        for s in range(len(editor.notebook.page[editor.page].section)):
            if editor.focusWidget().objectName() == editor.notebook.page[editor.page].section[s].title:
                editor.notebook.page[editor.page].section[s].title = title
        editor.focusWidget().setObjectName(title)
        editor.focusWidget().setText(title)
        editor.autosaver.onChangeMade()
        # cmd = Undo({'object_name':editor.focusWidget().objectName(),'type':'section', 'action':'rename', 'old_name':old_name})
        # editor.undo_stack.append(cmd)

def delete_section(editor):
    accept = QMessageBox.question(editor, 'Delete Section', 'Deleting this section will delete all objects inside it. Are you sure you want to delete it?')
    if accept == QMessageBox.Yes:

        p = editor.page

        for s in range(len(editor.notebook.page[p].section)):
            if editor.focusWidget().objectName() == editor.notebook.page[p].section[s].title:

                #Remove section Widget from editor
                editor.sections.itemAt(s).widget().deleteLater()

                # If current section is deleted, remove all objects from editor
                if editor.section == s:
                    if len(editor.notebook.page[p].section[s].object) > 0:
                        
                        for o in range(len(editor.notebook.page[p].section[s].object)):
                            editor.object[o].deleteLater()
                        editor.object.clear()

                # Remove objects from model
                if len(editor.notebook.page[p].section[s].object) > 0:
                    editor.notebook.page[p].section[s].object.clear()
                
                # Remove section from model
                editor.notebook.page[p].section.pop(s)

                if editor.section == s:
                    if len(editor.notebook.page[p].section) > 0:
                        editor.section = 0

                        for x in range(editor.sections.count()):
                            editor.sections.itemAt(s).widget().setStyleSheet("background-color: #f0f0f0")
                        editor.sections.itemAt(0).widget().setStyleSheet("background-color: #c2c2c2")

                        if len(editor.notebook.page[p].section[0].object) > 0:
                            for o in range(len(editor.notebook.page[p].section[0].object)):
                                params = editor.notebook.page[p].section[0].object[o]
                                build_object(editor, params)
                else:
                    editor.section = -1
                    
                editor.autosaver.onChangeMade()
                return
        editor.autosaver.onChangeMade()

