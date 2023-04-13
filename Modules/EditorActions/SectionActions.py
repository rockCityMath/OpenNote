# New Section
# get user input for name
# add to the page
# add visually in editor
# change to new section visually (widgets, tabs, etc?)
# update section index

# Display Section
# add section widget to notebook visually
# will be used by new section and loading from notebook

# Change Section
# hide old section widgets
# update to new section (ui and indexes)
# show new section widgets

# Section Menu
# menu that lets user rename and delete

# Rename Section
# get user input for new name
# update section name visually and in state

# Delete Section
# delete section from notebook and visually
# make sure it deletes the current sections widgets
# handle case where section is current one

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from Models.Editor import Editor

def addSection(self):
    editor = self
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

