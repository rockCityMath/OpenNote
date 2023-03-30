from models.notebook import *
from modules.build_ui import *
from modules.load import new
from modules.save import Autosaver
from modules.screensnip import SnippingWidget
from modules.object import add_snip

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import cv2
import os
from datetime import datetime

# models.notebook.Notebook is where all Notebook and Object data is stored
# models.object.* are models for Widgets used in the editor
#   Notebook Objects and Widgets from these models share params (geometry, text, image path, etc.)
#   Pickle will save the Notebook object
#   The editor will create and destroy Widgets per Page/Section (see modules.page.change_section, modules.load.build)
#       A Section's Widgets also exist in self.object, ordered by time of creation

class Editor(QMainWindow):
    def __init__(self):
        super().__init__()

        # When the application is started, open a new, empty notebook
        self.notebook = Notebook('Untitled Notebook')    # Current notebook object
        self.object = []                        # List of Widgets on current Page/Section
        self.page = -1                          # Index of current Page (New notebook has no pages: set to -1)
        self.section = -1                       # Index of current Section (New notebook has no sections: set to -1)
        self.selected = None                    # Selected object (for font attributes of TextBox)
        self.autosaver = Autosaver(self, self.notebook)  # Object with method for indicating changes and determining if we should autosave
        self.undo_stack = [] #QUndoStack()
        self.clipboard_object = None
        self.shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut.activated.connect(self.undo_event)
        self.setFocus()
        self.snippingWidget = SnippingWidget(app=QApplication.instance())
        self.snippingWidget.onSnippingCompleted = self.onSnippingCompleted

        build_ui(self)

    # If user takes a screensnip, save it to a file and put it on the page
    def onSnippingCompleted(self, image_blob):
        print(self.snippingWidget.event_pos)
        self.setWindowState(Qt.WindowActive)
        if image_blob is None:
            return

        pos = self.snippingWidget.event_pos

        currentDatetime = datetime.now()
        fileName = currentDatetime.strftime("%d-%m-%Y_%H-%M-%S") + ".png"

        path = os.getcwd() + "/screenshots/" + fileName
        cv2.imwrite(path, image_blob)
        add_snip(self, pos, path)

    def snipArea(self, event_pos):
        self.setWindowState(Qt.WindowMinimized)
        self.snippingWidget.start(event_pos)



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
        self.autosaver.onChangeMade()

    def undo_event(self):
        if len(self.undo_stack)>0:
            pop_item = self.undo_stack.pop(-1)
            print(pop_item.parameter)
