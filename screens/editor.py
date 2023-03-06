from models.notebook import *
from modules.build_ui import *
from modules.load import new

from PyQt6 import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class Editor(QMainWindow):
    def __init__(self):
        super().__init__()

        # When the application is started, open a new, empty notebook
        self.notebook = Notebook('Untitled Notebook')    # Current notebook object
        self.object = []                        # List of Widgets on current Page/Section
        self.page = -1                          # Index of current Page (New notebook has no pages: set to -1)
        self.section = -1                       # Index of current Section (New notebook has no sections: set to -1)
        self.selected = None                    # Selected object (for font attributes of TextBox)

        build_ui(self)

        # models.notebook.Notebook is where all Notebook and Object data is stored
        # models.object.* are models for Widgets used in the editor
        #   Notebook Objects and Widgets from these models share params (geometry, text, image path, etc.)
        #   Pickle will save the Notebook object
        #   The editor will create and destroy Widgets per Page/Section (see modules.page.change_section, modules.load.build)
        #       A Section's Widgets also exist in self.object, ordered by time of creation

    # Drag object event
    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    # Drop object event
    def dropEvent(self, event):
        #check if object is in workspace
        if (not self.frame.geometry().contains(event.pos())
            or event.pos().y() < 120):
            return
        self.focusWidget().move(event.pos().x(), event.pos().y())
        event.acceptProposedAction()