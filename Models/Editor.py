from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from Modules.BuildUI import *
from Modules.Save import Autosaver
from Modules.Screensnip import SnippingWidget
from Models.NotebookModel import NotebookModel
from Models.SectionModel import SectionModel
from Modules.Undo import UndoHandler

from Views.PageView import PageView
from Views.EditorFrameView import EditorFrameView
from Views.NotebookTitleView import NotebookTitleView
from Views.SectionView import SectionView


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.notebook = NotebookModel('Untitled Notebook')    # Current notebook object
        # self.selected = None                                  # Selected object (for font attributes of TextBox)

        # View-Controllers that let the user interact with the underlying models
        self.notebookTitleView = NotebookTitleView(self.notebook.title)
        self.frameView = EditorFrameView(self)
        self.pageView = PageView(self.notebook.pages)
        self.sectionView = SectionView(self.notebook.pages[0].sections)

        self.autosaver = Autosaver(self) # Waits for change signals and saves the notebook
        self.setFocus()

        self.settings = QSettings("UNT - Team Olive", "OpenNote")

        build_ui(self)

    def closeEvent(self, event):
        # Save window size and position before exiting

        print("Window closing event triggered")
        
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        super().closeEvent(event)

    def showEvent(self, event):
        # Restores window size and position

        print("Window showing event triggered")

        self.restoreGeometry(self.settings.value("geometry", self.saveGeometry())) 
        self.restoreState(self.settings.value("windowState", self.saveState()))
        super().showEvent(event)
    # def focusInEvent(self, event):
    #     self.repaint()
