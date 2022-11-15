import sys, os

from modules import *
from widgets import *
from models.Notebook import Notebook
from models.Page import Page

os.environ["QT_FONT_DPI"] = "96"
FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

###DASHBOARD WINDOW### 

class NotebookSelection(QMainWindow):
    def __init__(self):
        super().__init__()

        # window title and resizing
        self.setWindowTitle("OpenNote - Select Notebook")
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width * 2, self.screen_height * 2)

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    ###TOOLBAR ACTIONS

    # create
        self.create_notebook_action = self.create_action(self, './images/svg/arrow-down.svg', "Create Notebook", "Create Notebook", False)
        #self.create_action.toggled.connect()

    # load
        self.load_notebook_action = self.create_action(self, './images/svg/arrow-down.svg', "Load Notebook", "Load Notebook", False)
        #self.load_action.toggled.connect()

    # add actions to toolbar
        toolbar.addActions([self.create_notebook_action, self.load_notebook_action])

    # helper function to make creating actions easier (see toolbar actions)
    def create_action(self, parent, icon_path, action_name, set_status_tip, set_checkable):
        action = QAction(QIcon(icon_path), action_name, parent)
        action.setStatusTip(set_status_tip)
        action.setCheckable(set_checkable)
        return action

    def create_notebook(self):
        return
    def load_notebook(self):
        return

###MAIN WINDOW###

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    ###INITIALIZE APP###

    # initialize notebook object
        self.notebook = Notebook("", "Unititled")
    # window title and resizing
        self.setWindowTitle(self.notebook.title + " - OpenNote")
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width * 2, self.screen_height * 2)

    # initialize file settings
        self.path = None
        self.filterTypes = "OpenNote (*.on)"

    # stylesheet
        with open('OpenNote/styles.qss',"r") as fh:
          self.setStyleSheet(fh.read())

    ###LAYOUT AND WIDGET INITIALIZATION###

    # menubar
        file_menu = self.menuBar().addMenu('&File')
        edit_menu = self.menuBar().addMenu('&Edit')

    # toolbar
        toolbar = QToolBar('Edit')
        toolbar.setIconSize(QSize(25, 25))
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    # statusbar - remove in final version
        self.statusBar = self.statusBar()

    # main container layout
        container = QWidget()
        grid = QGridLayout()
        self.setCentralWidget(container)
        container.setLayout(grid)
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

    # sidebar and workspace layout
        sidebar = QVBoxLayout()
        workspace = QVBoxLayout()
        grid.addLayout(sidebar, 0, 0, -1, 1)
        grid.addLayout(workspace, 0, 1, -1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 4)

    # sidebar widgets
        self.notebook_title = QLabel()
        self.pages_title = QLabel()
        self.pages = QTreeView()
        addPage = QPushButton("Create New Page")
        sidebar.addWidget(self.notebook_title)
        sidebar.addWidget(self.pages_title)
        sidebar.addWidget(self.pages)
        sidebar.addWidget(addPage)

    # workspace widgets
        sections = QHBoxLayout()
        self.editor = QTextEdit()
        workspace.addLayout(sections)
        workspace.addWidget(self.editor)

    # stylesheet reference for widgets
        container.setObjectName("container")
        self.notebook_title.setObjectName("notebook_title")
        self.pages_title.setObjectName("pages_title")
        self.pages.setObjectName("pages")
        addPage.setObjectName("addPage")

    ###SIDEBAR WIDGETS###

    # notebook
        self.notebook_title.setText(self.notebook.title)

    # pages
        self.pages_title.setText("Pages")

        self.model = QStandardItemModel()               # model should be saved - stores page titles
        parentItem = self.model.invisibleRootItem()
        for i in range(0,4):
            item = QStandardItem("Page " + str(i))
            parentItem.appendRow(item)
            parentItem = item
        self.pages.setModel(self.model)

    # addPage
        addPage.clicked.connect(lambda: self.add_page_action(parentItem))

    ###WORKSPACE WIDGETS###

    # sections
        addSection = QPushButton()
        addSection.setText("+")
        addSection.setFixedWidth(30)    

        button1 = QPushButton("Section 1")
        button2 = QPushButton("Section 2")
        button3 = QPushButton("Section 3")
        button4 = QPushButton("Section 4")
        sections.addWidget(button1)
        sections.addWidget(button2)
        sections.addWidget(button3)
        sections.addWidget(button4)

        sections.addWidget(addSection)

    # editor
        self.editor.selectionChanged.connect(self.update_format)

        self.editor.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        self.editor.setAcceptRichText(True)
        font = QFont("Times", 12)
        self.editor.setFont(font)
        self.editor.setFontPointSize(12)

    ###MENUBAR ACTIONS###

    # open file
        open_file_action = self.create_action(self, './OpenNote/images/svg/arrow-down.svg', 'Open Notebook...', 'Open Notebook', False)
        open_file_action.setShortcut(QKeySequence.StandardKey.Open)
        open_file_action.triggered.connect(self.file_open)

        save_file_action = self.create_action(self, './OpenNote/images/svg/arrow-down.svg', 'Save Notebook', 'Save Notebook', False)
        save_file_action.setShortcut(QKeySequence.StandardKey.Save)
        save_file_action.triggered.connect(self.file_saveAs)

        save_fileAs_action = self.create_action(self, './OpenNote/images/svg/arrow-down.svg', 'Save Notebook As...', 'Save Notebook As', False)
        save_fileAs_action.setShortcut(QKeySequence.fromString('Ctrl+Shift+S'))
        save_fileAs_action.triggered.connect(self.file_saveAs)

    # add actions to file menu
        file_menu.addActions([open_file_action, save_file_action, save_fileAs_action])

    ###TOOLBAR ACTIONS###

    # current icons are all temporary/placeholders until I find better ones

    # undo
    # redo
    # font style
    # font size
    # bold
        self.bold_action = self.create_action(self, './OpenNote/images/svg/bold.svg', "Bold", "Bold", True)
        self.bold_action.toggled.connect(lambda x: self.editor.setFontWeight(700 if x else 500))

    # italic
        self.italic_action = self.create_action(self, './OpenNote/images/svg/italic.svg', "Italic", "Italic", True)
        self.italic_action.toggled.connect(self.editor.setFontItalic)

    # underline
        self.underline_action = self.create_action(self, './OpenNote/images/svg/underline.svg', "Underline", "Underline", True)
        self.underline_action.toggled.connect(self.editor.setFontUnderline)

    # highlight
    # font color

    # add actions to toolbar
        toolbar.addActions([self.bold_action, self.italic_action, self.underline_action])


        self.update_format()

###FUNCTIONS###

    # open file
    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self, 
            caption = 'Open Notebook',
            filter = self.filterTypes
        )
        self.notebook = Notebook.load(path)
        self.editor.setText(self.notebook.text)
        self.update_title()
        self.update_notebook_title()

        #self.editor.setText(notebook.text)
        #self.editor.setText(self.notebook.text)
        #"""if path:
        #    try:
        #        with open(path, 'r') as f:
        #            text = f.read()
        #            self.editor.setText(text)
        #            #notebook = Notebook.load(path)
        #    except Exception as e:
        #        self.dialog_message(str(e))
        #    else:
        #        self.path = path
        #        self.editor.setHtml(text)
        #        self.update_title()"""

    # save currently open file
    def file_save(self):
        lambda: self.notebook.save()
        #"""if self.path is None:
        #    self.file_saveAs()
        #else:
        #    try:
        #        text = self.editor.toHtml()
        #        with open(self.path, 'w') as f:
        #            f.write(text)
        #            #self.notebook.save()
        #            f.close
        #    except Exception as e:
        #        self.dialog_message(str(e))"""

    # save currently open file as...
    def file_saveAs(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save notebook as',
            '',
            self.filterTypes
        )
        self.notebook.text = self.editor.toHtml()
        self.notebook.location = path
        self.notebook.title = os.path.basename(path)
        self.notebook.text = self.editor.toHtml()
        self.notebook.save()
        self.update_title()
        self.update_notebook_title()
        #"""text = self.editor.toHtml()

        #if not path:
        #    return
        #else:
        #    try:
        #        with open(path, 'w') as f:
        #            f.write(text)
        #            #self.notebook.save()
        #            f.close()
        #    except Exception as e:
        #        self.dialog_message(str(e))
        #    else:
        #        self.path = path
        #        self.update_title()"""

    # create a new page
    def add_page_action(self, parentItem):
        title, accept = QInputDialog.getText(self, 'New Page Title', 'Enter title of new page: ')
        if accept:
            item = QStandardItem(title)
            parentItem.appendRow(item)
            self.pages.setModel(self.model)

    # helper function to make creating actions easier (see toolbar actions)
    def create_action(self, parent, icon_path, action_name, set_status_tip, set_checkable):
        action = QAction(QIcon(icon_path), action_name, parent)
        action.setStatusTip(set_status_tip)
        action.setCheckable(set_checkable)
        return action

    # helper function to update window title based on open notebook
    def update_title(self):
        self.setWindowTitle(self.notebook.title + " - OpenNote")

    # helper function to update notebook_title label based on open notebook
    def update_notebook_title(self):
        self.notebook_title.setText(self.notebook.title)

    # helper function to update toolbar options when text editor selection is changed
    def update_format(self):
        self.blockSignals(True)

        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.bold)

        self.blockSignals(False)

    #helper function to show error messages
    def dialog_message(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.show() 

###APPLICATION###

if __name__ == "__main__":
    app = QApplication(sys.argv)
    OpenNote = MainWindow()
    #OpenNote = NotebookSelection()
    OpenNote.show()
    sys.exit(app.exec())