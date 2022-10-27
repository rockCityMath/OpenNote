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

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        #super().__init__(parent)
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

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
            
        #Testing
        self.notebook=Notebook('Test')

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()
        if btnName=='addPageBtn':
            name=input('Name: ')
            self.notebook.pages.append(Page(name))
        print(self.notebook.pages)

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
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
