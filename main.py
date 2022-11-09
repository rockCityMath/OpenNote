# This Python file uses the following encoding: utf-8
import sys
import os

from modules import *
from widgets import *

from models.Notebook import Notebook
from models.Page import Page

os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

widgets = None
				
# Initial window that allows user to open or create notebook
class NotebookSelection(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notebook Selection")
        
        # Define add notebook button and input fields
        self.addNotebookButton = QPushButton("Add Notebook")
        self.addNotebookButton.setCheckable(True)
        self.addNotebookButton.setObjectName('addNotebook')
        self.addNotebookButton.clicked.connect(self.buttonClick)

        self.input = QLineEdit()
        self.input.setPlaceholderText('page name')
        
        self.location = QLineEdit()
        self.location.setPlaceholderText('location: ( . or ./Desktop etc)')

        # Define open notebook button
        self.openNotebookButton = QPushButton("Open Notebook")
        self.openNotebookButton.setCheckable(True)
        self.openNotebookButton.setObjectName('openNotebook')
        self.openNotebookButton.clicked.connect(self.buttonClick)

        # Place buttons and fields on layout
        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.location)
        layout.addWidget(self.addNotebookButton)
        layout.addWidget(self.openNotebookButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    # Handle dashboard button clicks
    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

        # Create a new .ON file to hold the notebook
        if btnName=='addNotebook':
            notebook = Notebook(self.input.text())
            notebook.location = self.location.text() + '/' + self.input.text() + '.on'
            notebook.save()
            
            self.close()
            self.w = MainWindow(notebook)
            self.w.show()     
        
        # Open an existing notebook from a .ON file
        if btnName == "openNotebook":
            fileInfoTuple = QFileDialog.getOpenFileName(self, 'Open Notebook')
            print(fileInfoTuple[0])

            notebook = Notebook.load(fileInfoTuple[0])

            self.w = MainWindow(notebook)
            self.w.show()  
            self.close()    
        
# Editor Window
class MainWindow(QMainWindow):
    def __init__(self, notebook):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # Editor Context
        self.notebook = notebook
        self.pagesList = self.findChild(QListView, "pagesList")
        self.model = QStandardItemModel()
        self.pagesList.setModel(self.model)

        # Editor Initialization
        self.selectedPageIndex = 0
        self.selectedPageLabel = self.findChild(QLabel, "activePage")

        if self.notebook.pages:
            self.selectedPageLabel.setText(self.notebook.pages[0].title)
        else:
            self.selectedPageLabel.setText("No pages!")

        self.notebookTitle = self.findChild(QLabel, "notebookTitle")
        self.notebookTitle.setText(self.notebook.title)

        self.updateNotebookPages()
        
        
        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        Settings.ENABLE_CUSTOM_TITLE_BAR = False

        # APP NAME
        title = "OpenNote"
        description = "OpenNote - Open-source notetaking in Python."
        self.setWindowTitle(title)
        #self.setWindowFlag(Qt.FramelessWindowHint)

        # BUTTON SIGNALS
        widgets.minimizeAppBtn.clicked.connect(self.buttonClick)
        widgets.maximizeRestoreAppBtn.clicked.connect(self.buttonClick)
        widgets.closeAppBtn.clicked.connect(self.buttonClick)
        widgets.fileBtn.clicked.connect(self.buttonClick)
        widgets.homeBtn.clicked.connect(self.buttonClick)
        widgets.viewBtn.clicked.connect(self.buttonClick)
        widgets.helpBtn.clicked.connect(self.buttonClick)
        widgets.undoBtn.clicked.connect(self.buttonClick)
        widgets.boldBtn.clicked.connect(self.buttonClick)
        widgets.italicBtn.clicked.connect(self.buttonClick)
        widgets.underlineBtn.clicked.connect(self.buttonClick)
        widgets.highlightBtn.clicked.connect(self.buttonClick)
        widgets.addPageBtn.clicked.connect(self.buttonClick)
        widgets.saveBtn.clicked.connect(self.buttonClick)

        # OTHER SIGNALS
        self.model.dataChanged.connect(self.renamePage)
        self.pagesList.selectionModel().selectionChanged.connect(self.selectPage)

        # SET CUSTOM THEME
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            UIFunctions.theme(self, themeFile, True) # LOAD AND APPLY STYLE
            AppFunctions.setThemeHack(self) # SET HACKS


    # BUTTON HANDLER
    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == 'addPageBtn':
            title, ok = QInputDialog.getText(self, 'Page Title', 'Enter title of new page: ')
            if ok:
                self.notebook.pages.append(Page(title)) # set the added page as active?
                self.updateNotebookPages()
            
        elif btnName == 'saveBtn':
            self.notebook.save()

        else:
            print(btnName + " pressed")


    # Editor Functions
    def renamePage(self):
        updatedName = self.pagesList.currentIndex().data()
        renamedPageIndex = self.pagesList.currentIndex().row()
        self.notebook.pages[renamedPageIndex].title = updatedName

    def selectPage(self):
        self.selectedPageIndex = self.pagesList.currentIndex().row()
        self.selectedPageLabel.setText(self.notebook.pages[self.selectedPageIndex].title)

    def updateNotebookPages(self):
        self.model.removeRows(0, self.model.rowCount())
        for page in self.notebook.pages:
            item = QStandardItem(page.title)
            self.model.appendRow(item)

    # RESIZE EVENTS - needs fix
    def resizeEvent(self, event):
        UIFunctions.resize_grips(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    selectionUI = NotebookSelection()
    selectionUI.show()
    sys.exit(app.exec_())
