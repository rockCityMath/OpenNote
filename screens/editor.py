from models.notebook import *
from modules.build_ui import *
from modules.load import new
from modules.save import Autosaver
from modules.screensnip import SnippingWidget
from modules.object import add_snip

from modules.object import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

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
        self.temp_buffer = []
        self.shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut.setContext(Qt.ApplicationShortcut)
        self.shortcut.activated.connect(self.undo_event)
        self.setFocus()
        self.snippingWidget = SnippingWidget(app=QApplication.instance())
        self.snippingWidget.onSnippingCompleted = self.onSnippingCompleted

        build_ui(self)

    # If user takes a screensnip, save it to a file and put it on the page
    def onSnippingCompleted(self, image_blob):
        self.setWindowState(Qt.WindowActive)
        if image_blob is None:
            return

        pos = self.snippingWidget.event_pos
        add_snip(self, pos, image_blob)

    def snipArea(self, event_pos):
        self.setWindowState(Qt.WindowMinimized)
        self.snippingWidget.start(event_pos)

    # Drag object event
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        obj = self.focusWidget()
        self.temp_buffer.append({'type':'object','action':'move','name':obj.objectName(),'x':event.pos().x(),'y':event.pos().y()})

    def focusInEvent(self, event):
        self.repaint()

    # Drop object event
    def dropEvent(self, event):
        #check if object is in workspace
        if (not self.frame.geometry().contains(event.pos())
            or event.pos().y() < 120):
            return
        self.focusWidget().move(event.pos().x(), event.pos().y())
        event.acceptProposedAction()
        self.autosaver.onChangeMade()
        self.undo_stack += self.temp_buffer[:1]
        self.temp_buffer = []

    def undo_event(self):
        if len(self.undo_stack)>0:
            pop_item = self.undo_stack.pop(-1)
            if pop_item['type']=='object':
                index = 0
                for i in range(len(self.notebook.page[self.page].section[self.section].object)):
                    if pop_item['name']==self.notebook.page[self.page].section[self.section].object[i].name:
                        index=i
                #TODO instead of object[0] i need to find object by name
                if pop_item['action'] == 'move':
                    params = self.notebook.page[self.page].section[self.section].object[index]
                    params.x = pop_item['x']
                    params.y = pop_item['y']         
                    self.notebook.page[self.page].section[self.section].object[index] = params
                    #deleting in old position
                    self.object[index].deleteLater()
                    self.object.pop(index)
                    #TODO Hide old location
                    build_object(self,params)
                elif pop_item['action'] == 'create':
                    self.object[index].deleteLater()
                    self.object.pop(index)
                    self.notebook.page[self.page].section[self.section].object.pop(index)
                else:
                    self.object.append(pop_item['data'])
                    self.notebook.page[self.page].section[self.section].object.append(pop_item['data'])
                    build_object(self,pop_item['data'])
