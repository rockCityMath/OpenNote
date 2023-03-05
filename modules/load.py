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
    path, _ = QFileDialog.getOpenFileName(
        editor, 
        'Open Notebook',
        '',
        'OpenNote (*.on)'
    )

    file = open(path, 'rb')
    editor.notebook = pickle.load(file)

    build(editor)

# Builds widgets for Page[0], Section[0] from params in loaded models.notebook.Notebook object
# Sets initial editor.page & editor.section to 0 (first page & section)
def build(editor):

    # Display Notebook title
    editor.setWindowTitle(editor.notebook.title + " - OpenNote")
    editor.notebook_title.setText(editor.notebook.title)

    # Show all Pages in Notebook
    for p in range(len(editor.notebook.page)):
        params = editor.notebook.page[p]
        build_page(editor, params.title)    # Build functions add widgets to editor

    # Show all Sections in page 1
    for s in range(len(editor.notebook.page[0].section)):  
        params = editor.notebook.page[0].section[s]
        build_section(editor, params.title)

    # Show objects in page1, section1
    for o in range(len(editor.notebook.page[0].section[0].object)):
        params = editor.notebook.page[0].section[0].object[o]
        build_object(editor, params)

    # Select page1, section1
    editor.page = 0
    editor.section = 0