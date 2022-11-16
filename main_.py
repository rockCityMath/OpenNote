import sys, os

from modules import *
from widgets import *
from models.Notebook import Notebook
from models.Page import Page

os.environ["QT_FONT_DPI"] = "96"
FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

###GLOBAL FUNCTIONS###

#add notebook to recents.txt
def addToRecent(recent):
    f = open("recent.txt", "r")
    content = f.read()
    f.close()
    if recent not in content:
        print('file is new and added to recents')
        f = open("recent.txt", "a")
        f.write(recent)
        f.close()
    else:
        print("file is in recents already")

###DASHBOARD WINDOW### 

class NotebookSelection(QMainWindow):
    def __init__(self):
        super().__init__()

    # window title and resizing
        self.setWindowTitle("OpenNote - Select Notebook")
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width * 1.5, self.screen_height * 1.5)

    # stylesheet
        with open('dashboard_styles.qss',"r") as fh:
          self.setStyleSheet(fh.read())

        toolbar = QToolBar()
        toolbar.setObjectName("dashboard_toolbar")
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    # display recent files
        recentTitle = QLabel("Recent Notebooks")
        container = QWidget()
        container.setObjectName("container")
        grid = QGridLayout()
        layout = QVBoxLayout()
        layout.addWidget(recentTitle)
        layout.addLayout(grid)
        recentTitle.setFixedHeight(30)
        grid.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(container)
        container.setLayout(layout)

        f = open('recent.txt','r')
        notebooks = f.readlines()
        row = 1
        col = 1
        for i in range(len(notebooks)):
            recentCard = QWidget()
            recentCard.setObjectName("recentCard")
            recentCard.setFixedSize(250, 250)
            recentTitle = QLabel(recentCard)
            recentTitle.setObjectName("recentTitle")
            title = notebooks[i].split('- ')
            recentTitle.setText(title[1])
            grid.addWidget(recentCard,row,col)
            if col == 4:
                col=0
                row+=1
            col+=1

    ###TOOLBAR ACTIONS###

    # title
        title = QLabel("OpenNote")
        title.setObjectName("dashboard_title")

    # create
        self.create_notebook_action = self.create_action(self, './images/svg/arrow-down.svg', "Create Notebook", "Create Notebook", False)
        self.create_notebook_action.triggered.connect(self.create_notebook)

    # load
        self.open_file_action = self.create_action(self, './images/svg/arrow-down.svg', "Load Notebook", "Load Notebook", False)
        self.open_file_action.triggered.connect(self.load_notebook)

    # add actions to toolbar
        toolbar.addWidget(title)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)
        toolbar.addActions([self.create_notebook_action, self.open_file_action])

    ###FUNCTIONS - DASHBOARD###
    # helper function to make creating actions easier (see toolbar actions)
    def create_action(self, parent, icon_path, action_name, set_status_tip, set_checkable):
        action = QAction(QIcon(icon_path), action_name, parent)
        action.setStatusTip(set_status_tip)
        action.setCheckable(set_checkable)
        return action

    # save currently open file as...
    def create_notebook(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save notebook as',
            '',
            filter = "OpenNote (*.on)"
        )
        title = os.path.basename(path)
        self.notebook = Notebook(None, title)
        self.notebook.location = path
        self.notebook.save()

        recent = self.notebook.location + '/ - ' + self.notebook.title+'\n'
        addToRecent(recent)

        self.w = MainWindow(self.notebook, False)
        self.w.show()  
        OpenNote.close()  

    # open file
    def load_notebook(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self, 
            caption = 'Open Notebook',
            filter = "OpenNote (*.on)"
        )
        self.notebook = Notebook.load(path)

        recent = self.notebook.location + '/ - ' + self.notebook.title+'\n'
        addToRecent(recent)

        self.w = MainWindow(self.notebook, True)
        self.w.show()  
        OpenNote.close()  



class RecentCard(QWidget):
    def __init__(self, title_loc):
        super().__init__()
        global rwidgets
        

###MAIN WINDOW###

class MainWindow(QMainWindow):
    def __init__(self, notebook, load):
        super().__init__()

    ###INITIALIZE APP###
        self.notebook = notebook
    
    # window title and resizing
        self.setWindowTitle(self.notebook.title + " - OpenNote")
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width * 2, self.screen_height * 2)

    # initialize file settings
        self.path = None
        self.filterTypes = "OpenNote (*.on)"

    # stylesheet
        with open('styles.qss',"r") as fh:
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
        # for i in range(0,4):
        #     item = QStandardItem("Page " + str(i))
        #     parentItem.appendRow(item)
        #     parentItem = item
        #self.pages.setModel(self.model)    

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
        font = QFont("Times", 24)
        self.editor.setFont("Segoe UI")
        self.editor.setFontPointSize(24)
        self.editor.setTextColor('black')

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

    # initialize editor with new notebook object
        if load:
            if self.notebook.text:
                self.editor.setText(self.notebook.text)
            self.update_title()
            self.update_notebook_title()
        else:
            self.update_title()
            self.update_notebook_title()

    ###TOOLBAR ACTIONS###

    # current icons are all temporary/placeholders until I find better ones

    # undo
    # redo
    # font family
        self.font_family = QFontComboBox()
        self.font_family.currentFontChanged.connect(self.editor.setCurrentFont)

    # font size
        self.font_size = QComboBox()
        self.font_size.addItems([str(fs) for fs in FONT_SIZES])
        self.font_size.currentIndexChanged.connect(lambda font_size: self.editor.setFontPointSize(float(font_size)))

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
        self.font_color = QPushButton("Color")
        self.font_color.setObjectName("font_color")
        self.color_dialog = QColorDialog()
        self.color = self.editor.textColor()
        self.font_color.clicked.connect(lambda: self.font_color_action())
        

    # add actions to toolbar
        toolbar.addWidget(self.font_family)
        toolbar.addWidget(self.font_size)
        toolbar.addWidget(self.font_color)
        toolbar.addSeparator()
        toolbar.addActions([self.bold_action, self.italic_action, self.underline_action])

        self.format_actions = [
            self.font_family,
            self.font_size,
            self.bold_action,
            self.italic_action,
            self.underline_action
        ]

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
        recent = self.notebook.location + '/ - ' + self.notebook.title+'\n'
        addToRecent(recent)
        self.editor.setText(self.notebook.text)
        self.update_title()
        self.update_notebook_title()

    # save currently open file
    def file_save(self):
        lambda: self.file_saveAs(self)

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
        recent = self.notebook.location + '/ - ' + self.notebook.title+'\n'
        addToRecent(recent)
        self.update_title()
        self.update_notebook_title()

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

    def block_signals(self, actions, b):
        for x in actions:
            x.blockSignals(b)

    def font_color_action(self):
        self.color = self.color_dialog.getColor()
        self.editor.setTextColor(self.color)
        self.pal = QPalette()
        self.pal.setColor(QPalette.Normal, QPalette.ButtonText, self.color)
        self.font_color.setPalette(self.pal)

    # helper function to update toolbar options when text editor selection is changed
    def update_format(self):
        self.block_signals(self.format_actions, True)

        self.font_family.setCurrentFont(self.editor.currentFont())
        self.font_size.setCurrentText(str(int(self.editor.fontPointSize())))

        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.bold)

        self.block_signals(self.format_actions, False)

    #helper function to show error messages
    def dialog_message(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.show() 

###APPLICATION###

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #OpenNote = MainWindow()
    OpenNote = NotebookSelection()
    OpenNote.show()
    sys.exit(app.exec())