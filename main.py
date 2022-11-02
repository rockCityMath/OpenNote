# This Python file uses the following encoding: utf-8
import sys
import os
import platform

from modules import *
from widgets import *

from classes.Notebook import Notebook
from classes.Page import Page
from classes.util import UniqueList

os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

widgets = None

# Open a notebook from a .ON file
def openNotebook(self):
    fileInfoTuple = QFileDialog.getOpenFileName(self, 'Open Notebook')
    print(fileInfoTuple[0]) # 0 index is file path

    notebook = Notebook()
    notebook.load(fileInfoTuple[0])

    # for page in notebook.pages:
    #         print("Page: " + page.title)

    print("Title: " + notebook.title)

    self.w = MainWindow(notebook)
    self.w.show()  
        
				

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        
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
            notebook.pages.append(Page('test page'))
            notebook.pages.append(Page('test page 2'))
            notebook.save()
            
            print(notebook.title+' created and saved at:' + notebook.location)
            self.close()
            self.w = MainWindow(notebook)
            self.w.show()     
        
        # Open an existing notebook from a .ON file
        if btnName == "openNotebook":
            openNotebook(self)
            self.close()

        
        
class MainWindow(QMainWindow):
    def __init__(self, notebook):
        #super().__init__(parent)
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.notebook = notebook

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = False

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "OpenNote"
        description = "OpenNote - Open-source notetaking in Python."
        # APPLY TEXTS
        self.setWindowTitle(title)
        #self.setWindowFlag(Qt.FramelessWindowHint)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////
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

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()
        if btnName=='addPageBtn':
            print(self.notebook)
            name=input('Name: ')
            self.notebook.pages.append(Page(name))
        
        print('number of pages is: '+ str(self.notebook.pages.__len__()))
        for page in self.notebook.pages:
            print("Page: " + page.title)

    # RESIZE EVENTS - needs fix
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Dashboard()
    widget.show()
    sys.exit(app.exec_())
