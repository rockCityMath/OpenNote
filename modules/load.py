import pickle

from models.object import TextBox
from modules.page import build_page
from modules.section import build_section
from modules.object import build_object

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# Loads models.notebook.Notebook class from file
def load(editor):
    path, accept = QFileDialog.getOpenFileName(
        editor, 
        'Open Notebook',
        '',
        'OpenNote (*.on)'
    )
    if accept:
        file = open(path, 'rb')
        destroy(editor)
        editor.notebook = pickle.load(file)
        editor.page = 0
        editor.section = 0
        #print("l", editor.notebook.page)
    build(editor)

# Builds widgets for Page[0], Section[0] from params in loaded models.notebook.Notebook object
# Sets initial editor.page & editor.section to 0 (first page & section)
def build(editor):

    # Display Notebook title
    editor.setWindowTitle(editor.notebook.title + " - OpenNote")
    editor.notebook_title.setText(editor.notebook.title)

    if len(editor.notebook.page) > 0:
        # Show all Pages in Notebook
        for p in range(len(editor.notebook.page)):
            params = editor.notebook.page[p]
            build_page(editor, params.title)    # Build functions add widgets to editor

        if len(editor.notebook.page[0].section) > 0:
            # Show all Sections in page 1
            for s in range(len(editor.notebook.page[0].section)):  
                params = editor.notebook.page[0].section[s]
                build_section(editor, params.title)
    
            if len(editor.notebook.page[0].section[0].object) > 0:
                # Show objects in page1, section1
                for o in range(len(editor.notebook.page[0].section[0].object)):
                    params = editor.notebook.page[0].section[0].object[o]
                    build_object(editor, params)

    # Select page1, section1
    editor.page = 0
    editor.section = 0

# Destroy all Widgets in the Current Notebook
def destroy(editor):

    if(len(editor.notebook.page)) > 0:
        # Destroy all Pages
        for p in range (len(editor.notebook.page)):
            editor.pages.itemAt(p).widget().deleteLater()

        if(len(editor.notebook.page[editor.page].section)) > 0:
            # Destroy all Sections
            for s in range(len(editor.notebook.page[editor.page].section)):
                editor.sections.itemAt(s).widget().deleteLater()

            if(len(editor.notebook.page[editor.page].section[editor.section].object)) > 0:
                # Destory all Objects
                for o in range(len(editor.notebook.page[editor.page].section[editor.section].object)):
                    editor.object[o].deleteLater()