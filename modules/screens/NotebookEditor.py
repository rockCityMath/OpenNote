import os, sys
from modules import *
from models import *
from pprint import pprint

# move to settings?
os.environ["QT_FONT_DPI"] = "96"
FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

### MAIN WINDOW###
class NotebookEditor(QMainWindow):
    def __init__(self, notebook):
        super().__init__()

        ## ---------------------- Initialize App ----------------------- ##
        self.notebook = notebook
        self.currentPageIndex = 0
        self.setAcceptDrops(True)
    
        # window title and resizing  
        self.setWindowTitle(self.notebook.title + " - OpenNote")
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width * 2, self.screen_height * 2)

        # initialize file settings
        self.path = None
        self.filterTypes = "OpenNote (*.on)"

        # stylesheet
        with open('styles/styles.qss',"r") as fh:
          self.setStyleSheet(fh.read())

        ## ---------------------- Layout & Widget Initialization ----------------------- ##

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
        
        self.frame = QFrame(self)
        self.frame.setStyleSheet("background-color: white;")
        workspace.addWidget(self.frame)
        
        self.frame.mousePressEvent = self.create_textedit #event that creates a text editor on click

        # stylesheet reference for widgets
        container.setObjectName("container")
        self.notebook_title.setObjectName("notebook_title")
        self.pages_title.setObjectName("pages_title")
        self.pages.setObjectName("pages")
        addPage.setObjectName("addPage")
        

        # notebook
        self.notebook_title.setText(self.notebook.title)

        # pages
        self.pages_title.setText("Pages")

        self.model = QStandardItemModel()              
        parentItem = self.model.invisibleRootItem()

        # init pages, this should probably move to an onUpdatedPages() function that adding, deleting, (renaming?) pages emits
        for page in self.notebook.pages:
            item = QStandardItem(page.title)
            item.setEditable(False)                   # Take this out when implementing renaming
            parentItem.appendRow(item)
            self.pages.setModel(self.model)

        self.pages.clicked.connect(self.onChangePage) 
        
        # addPage
        addPage.clicked.connect(lambda: self.onPageAdded(parentItem))

        

        # sections
        addSection = QPushButton()
        addSection.setText("+")
        addSection.setFixedWidth(30)    
        button1 = QPushButton("Section 1")
        button2 = QPushButton("Section 2")
        button3 = QPushButton("Section 3")
        button4 = QPushButton("Section 4")
        button5 = QPushButton("Add Image")
        sections.addWidget(button1)
        sections.addWidget(button2)
        sections.addWidget(button3)
        sections.addWidget(button4)
        sections.addWidget(button5)

        button5.setObjectName("addImage")
        #addimage
        button5.clicked.connect(lambda: self.addImage())

        sections.addWidget(addSection)

        # editor
        self.editor.selectionChanged.connect(self.onSelectionChanged)
        self.editor.textChanged.connect(self.onUpdateText)
        self.editor.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        font = QFont("Times", 24)
        self.editor.setFont("Segoe UI")
        self.editor.setFontPointSize(24)
        self.editor.setTextColor('black')

        ## ---------------------- Define Menu Items ----------------------- ##

        # open file
        open_file_action = self.create_action(self, 'styles/icons/svg_file_open', 'Open Notebook...', 'Open Notebook', False)
        open_file_action.setShortcut(QKeySequence.StandardKey.Open)
        open_file_action.triggered.connect(self.openNotebook)

        save_file_action = self.create_action(self, 'styles/icons/svg_file_save', 'Save Notebook', 'Save Notebook', False)
        save_file_action.setShortcut(QKeySequence.StandardKey.Save)
        save_file_action.triggered.connect(self.saveNotebook)

        save_fileAs_action = self.create_action(self, 'styles/icons/svg_file_save', 'Save Notebook As...', 'Save Notebook As', False)
        save_fileAs_action.setShortcut(QKeySequence.fromString('Ctrl+Shift+S'))
        save_fileAs_action.triggered.connect(self.saveNotebookAs)

        # add actions to file menu
        file_menu.addActions([open_file_action, save_file_action, save_fileAs_action])

        # initialize editor with first page of notebook
        if self.notebook.pages:
            self.editor.setText(self.notebook.pages[0].text)

        ## ---------------------- Define Toolbar Actions ----------------------- ##

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
        self.bold_action = self.create_action(self, 'styles/icons/svg_font_bold', "Bold", "Bold", True)
        self.bold_action.toggled.connect(lambda x: self.editor.setFontWeight(700 if x else 500))

        # italic
        self.italic_action = self.create_action(self, 'styles/icons/svg_font_italic', "Italic", "Italic", True)
        self.italic_action.toggled.connect(self.editor.setFontItalic)

        # underline
        self.underline_action = self.create_action(self, 'styles/icons/svg_font_underline', "Underline", "Underline", True)
        self.underline_action.toggled.connect(self.editor.setFontUnderline)

        # highlight
        # font color

        self.color = self.editor.textColor()
        self.pixmap = QPixmap('styles/icons/svg_font_color.svg')
        self.painter = QPainter(self.pixmap)
        self.painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        self.painter.setBrush(self.color)
        self.painter.setPen(self.color)
        self.painter.drawRect(self.pixmap.rect())
        self.font_color_icon = QIcon(self.pixmap)

        self.font_color = QPushButton()
        self.font_color.setIcon(QIcon(self.font_color_icon))
        self.font_color.setIconSize(QSize(30,30))
        self.font_color.setObjectName("font_color")
        self.color_dialog = QColorDialog()
        self.color = self.editor.textColor()
        self.font_color.clicked.connect(self.onFontColor)

        # add actions to toolbar
        toolbar.addWidget(self.font_family)
        toolbar.addWidget(self.font_size)
        toolbar.addWidget(self.font_color)
        toolbar.addSeparator()
        toolbar.setIconSize(QSize(30, 30))
        toolbar.addActions([self.bold_action, self.italic_action, self.underline_action])

        self.format_actions = [
            self.font_family,
            self.font_size,
            self.bold_action,
            self.italic_action,
            self.underline_action
        ]

        self.update_format()

    ## ---------------------- Notebook Functions ----------------------- ##
    def dragEnterEvent(self, event):
        event.accept() # accept the movement event

    def dropEvent(self, event):
        position = event.pos()

        # this is so bad...
        for textedit in self.notebook.pages[self.currentPageIndex].textedits: # look thru all textedits in array
            if textedit.isMoving: # this is set by the mouse event on the TextBoxDraggable object when it starts moving
                textedit.move(position.x(), position.y()) 
                textedit.isMoving = False
                event.accept()

        for image in self.notebook.pages[self.currentPageIndex].images:
            if image.isMoving:
                image.move(position.x(), position.y()) 
                image.isMoving = False
                event.accept()

    # Creates textedit when frame is clicked 
    def create_textedit(self, event):
        x = event.pos().x() + 150
        y = event.pos().y() + 100

        self.textedit = TextBoxDraggable(self, x, y, None)
        self.notebook.pages[self.currentPageIndex].textedits.append(self.textedit)
        self.textedit.show()
   
    def openNotebook(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self, 
            caption = 'Open Notebook',
            filter = self.filterTypes
        )
        self.notebook = Notebook.load(path)
        recent = self.notebook.location + '/ - ' + self.notebook.title+'\n'
        # addToRecent(recent)

        self.editor.setText(self.notebook.pages[0].text)
        self.update_title()
        self.update_notebook_title()

        e.notebookSelected.emit(self.notebook)

    def saveNotebook(self):
        self.notebook.save()

    def saveNotebookAs(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save notebook as',
            '',
            self.filterTypes
        )
        self.notebook.save()
        # recent = self.notebook.location + '/ - ' + self.notebook.title+'\n'
        # addToRecent(recent)

    ## ---------------------- EVENT HANDLERS ----------------------- ##

    def onPageAdded(self, parentItem):
        title, accept = QInputDialog.getText(self, 'New Page Title', 'Enter title of new page: ')
        if accept:
            item = QStandardItem(title)
            parentItem.appendRow(item)
            self.pages.setModel(self.model)

            newPage = Page(title)
            self.notebook.pages.append(newPage)
            # could add a call to onChangePage here to switch to new page on creation

    def addImage(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self, 
            caption = 'Add Image',
        )

        img = TextBoxDraggable(self, 50, 50, path)
        img.show()
        self.notebook.pages[self.currentPageIndex].images.append(img)

    def onUpdateText(self):
        self.notebook.pages[self.currentPageIndex].text = self.editor.toHtml()

    def onPageRename(self):
        print("rename!")
        print(self)

    def onChangePage(self, QModelIndex):

        for textedit in self.notebook.pages[self.currentPageIndex].textedits:
            textedit.hide()

        for image in self.notebook.pages[self.currentPageIndex].images:
            image.hide()

        # Update the current page index
        self.currentPageIndex = QModelIndex.row()

        # Switch to the new pages content
        # self.textedits = self.notebook.pages[self.currentPageIndex].textedits

        # Show current page's textedits
        for textedit in self.notebook.pages[self.currentPageIndex].textedits:
            textedit.show()

        for image in self.notebook.pages[self.currentPageIndex].images:
            image.show()

        # self.editor.setText(newPageText)

    # Update toolbar options when text editor selection is changed
    def onSelectionChanged(self):
        self.block_signals(self.format_actions, True)

        self.font_family.setCurrentFont(self.editor.currentFont())
        self.font_size.setCurrentText(str(int(self.editor.fontPointSize())))

        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.bold)

        self.block_signals(self.format_actions, False)

    def onFontColor(self):
        self.color = self.color_dialog.getColor()
        self.editor.setTextColor(self.color)
        self.pal = QPalette()
        self.pal.setColor(QPalette.Normal, QPalette.Button, self.color)
        self.font_color.setPalette(self.pal)
        self.color = self.editor.textColor()
        #self.pixmap = QPixmap('styles/icons/svg_font_color.svg')
        #self.painter = QPainter(self.pixmap)
        #self.painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        #self.painter.setBrush(self.color)
        #self.painter.setPen(self.color)
        #self.painter.drawRect(self.pixmap.rect())
        #self.font_color_icon = QIcon(self.pixmap)
        #self.font_color.setIcon(QIcon(self.font_color_icon))

    ## ---------------------- Helper Functions ----------------------- ##

    # Helper function to make creating actions easier (see toolbar actions)
    def create_action(self, parent, icon_path, action_name, set_status_tip, set_checkable):
        action = QAction(QIcon(icon_path), action_name, parent)
        action.setStatusTip(set_status_tip)
        action.setCheckable(set_checkable)
        return action

    # Helper function to update window title based on open notebook
    def update_title(self):
        self.setWindowTitle(self.notebook.title + " - OpenNote")

    # Helper function to update notebook_title label based on open notebook
    def update_notebook_title(self):
        self.notebook_title.setText(self.notebook.title)

    def block_signals(self, actions, b):
        for x in actions:
            x.blockSignals(b)

    # Helper function to show error messages
    def dialog_message(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.show() 

    # Helper function to update toolbar options when text editor selection is changed
    def update_format(self):
        self.block_signals(self.format_actions, True)

        self.font_family.setCurrentFont(self.editor.currentFont())
        self.font_size.setCurrentText(str(int(self.editor.fontPointSize())))

        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.bold)

        self.block_signals(self.format_actions, False)


