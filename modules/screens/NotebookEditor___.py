import os, sys

from modules.Helpers import *
from modules.MenuFunctions import *
from modules import *
from models import *

os.environ["QT_FONT_DPI"] = "96"
FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

class NotebookEditor(QMainWindow):
    def __init__(self, notebook):
        super().__init__()

        self.notebook = notebook
        currentPageIndex = 0
        #self.setAcceptDrops(True)

        self.setWindowTitle(self.notebook.title + " - OpenNote")
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width * 2, self.screen_height * 2)
        self.path = None

        with open('styles/styles.qss',"r") as ss:
            self.setStyleSheet(ss.read())
            ss.close()
        
#layout
        container = QWidget()
        container.setObjectName("container")
        grid = QGridLayout()
        sidebar = QVBoxLayout()
        self.notebookTitle = QLabel()
        self.notebookTitle.setObjectName("notebook_title")
        self.notebookTitle.setText(self.notebook.title)
        self.pagesTitle = QLabel()
        self.pagesTitle.setObjectName("pages_title")
        self.pagesTitle.setText("Pages")
        self.pages = QTreeView()
        self.pages.setObjectName("pages")
        addPage = QPushButton("Create New Page")
        addPage.setObjectName("addPage")
        sidebar.addWidget(self.notebookTitle)
        sidebar.addWidget(self.pagesTitle)
        sidebar.addWidget(self.pages)
        sidebar.addWidget(addPage)
        workspace = QVBoxLayout()
        sections = QHBoxLayout()
        workspace.addLayout(sections)
        self.frame = QFrame(self)
        self.frame.setStyleSheet("background-color: white;")
        workspace.addWidget(self.frame)
        grid.setSpacing(0)
        grid.setContentsMargins(0,0,0,0)
        grid.addLayout(sidebar, 0, 0, -1, 1)
        grid.addLayout(workspace, 0, 1, -1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 4)
        container.setLayout(grid)
        self.setCentralWidget(container)

#file menu
        openFile = createAction(self, 'styles/icons/svg_file_open', 'Open Notebook...', 'Open Notebook', False)
        openFile.setShortcut(QKeySequence.StandardKey.Open)
        openFile.triggered.connect(openNotebook)
        saveFile = createAction(self, 'styles/icons/svg_file_save', 'Save Notebook', 'Save Notebook', False)
        saveFile.setShortcut(QKeySequence.StandardKey.Save)
        saveFile.triggered.connect(saveNotebook)
        saveFileAs = createAction(self, 'styles/icons/svg_file_save', 'Save Notebook As...', 'Save Notebook As', False)
        saveFileAs.setShortcut(QKeySequence.fromString('Ctrl+Shift+S'))
        saveFileAs.triggered.connect(saveNotebookAs)
        fileMenu = self.menuBar().addMenu('&File')
        fileMenu.addActions([openFile, saveFile, saveFileAs])
