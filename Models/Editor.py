from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from Modules.BuildUI import *
from Modules.Save import Autosaver
from Modules.Screensnip import SnippingWidget
from Models.NotebookModel import NotebookModel
from Models.SectionModel import SectionModel

from Views.PageView import PageView
from Views.EditorFrameView import EditorFrameView
from Views.NotebookTitleView import NotebookTitleView
from Views.SectionView import SectionView


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.notebook = NotebookModel('Untitled Notebook')    # Current notebook object
        self.selected = None                                  # Selected object (for font attributes of TextBox)

        # View-Controllers that let the user interact with the underlying models
        self.notebookTitleView = NotebookTitleView(self.notebook.title)
        self.frameView = EditorFrameView(self)
        self.pageView = PageView(self.notebook.pages)
        self.sectionView = SectionView(self.notebook.pages[0].sections)

        # OLD STUFF
        self.autosaver = Autosaver(self)  # Object with method for indicating changes and determining if we should autosave
        self.undo_stack = [] #QUndoStack()
        self.temp_buffer = []

        self.shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut.setContext(Qt.ApplicationShortcut)
        self.shortcut.activated.connect(self.undo_event)

        self.setFocus()

        build_ui(self)

    def focusInEvent(self, event):
        self.repaint()

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

                    self.object[index].deleteLater()

                    self.object.pop(index)
                    #deleting in old position
                    build_object(self,params)
                    self.autosaver.onChangeMade()
                elif pop_item['action'] == 'create':
                    self.object[index].deleteLater()
                    self.object.pop(index)
                    self.notebook.page[self.page].section[self.section].object.pop(index)
                    self.autosaver.onChangeMade()
                else:
                    # self.object.append(pop_item['data'])
                    self.notebook.page[self.page].section[self.section].object.append(pop_item['data'])
                    build_object(self,pop_item['data'])
                    self.autosaver.onChangeMade()
