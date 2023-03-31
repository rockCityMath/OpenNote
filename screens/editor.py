from models.notebook import *
from modules.build_ui import *
from modules.load import new
from modules.save import Autosaver
from modules.object import *
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
        self.autosaver = Autosaver(self, self.notebook)  # Object with method for indicating changes and determining if we should autosave 
        self.undo_stack = [] #QUndoStack()
        self.shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut.setContext(Qt.ApplicationShortcut)
        self.shortcut.activated.connect(self.undo_event)
        
        build_ui(self)
        self.setFocus()
        self.temp_buffer=[]
        # models.notebook.Notebook is where all Notebook and Object data is stored
        # models.object.* are models for Widgets used in the editor
        #   Notebook Objects and Widgets from these models share params (geometry, text, image path, etc.)
        #   Pickle will save the Notebook object
        #   The editor will create and destroy Widgets per Page/Section (see modules.page.change_section, modules.load.build)
        #       A Section's Widgets also exist in self.object, ordered by time of creation
    
    # Drag object event
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        obj = self.focusWidget()
        self.temp_buffer.append({'type':'object','action':'move','name':obj.objectName(),'x':event.pos().x(),'y':event.pos().y()})


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
        
        # debugginh
        print(self.undo_stack[-1])
        print('--')
        for i in self.undo_stack:
            print(i)
      
      
  
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
                    self.object[index]=params
                    #TODO Hide old location
                    build_object(self,params)
                elif pop_item['action'] == 'create':
                    print('delete')
                else:
                    self.object.append(pop_item['data'])
                    self.notebook.page[self.page].section[self.section].object.append(pop_item['data'])
                    build_object(self,pop_item['data'])
                # print(pop_item.undo(self))
            elif pop_item['type']=='section':
                print('undoing section here')
            else:
                print('undoing page here')