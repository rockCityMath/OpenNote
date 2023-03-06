from modules.save import save, saveAs
from modules.load import new, load
from modules.page import add_page
from modules.section import add_section
from modules.object import add_object

from PyQt6 import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

#builds the application's UI
def build_ui(editor):

    #TODO: Finish UI refactor - Natalio

    #editor.statusBar = editor.statusBar()
    build_window(editor)
    build_menubar(editor)
    build_toolbar(editor)
    container = QWidget()
    grid = QGridLayout()
    editor.setCentralWidget(container)
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
    editor.notebook_title = QTextEdit()
    editor.notebook_title.setText(editor.notebook.title)
    editor.notebook_title.setFixedHeight(40)
    editor.pages_title = QLabel()
    editor.pages_title.setFixedHeight(40)
    editor.pages = QVBoxLayout()
    editor.pages_frame = QFrame()
    
    #sidebar.setStretchFactor(editor.pages, 1)
    addPage = QPushButton("Create New Page")
    addPage.clicked.connect(lambda: add_page(editor))
    sidebar.addWidget(editor.notebook_title)
    sidebar.addWidget(editor.pages_title)
    sidebar.addLayout(editor.pages)
    sidebar.addWidget(editor.pages_frame)
    sidebar.addWidget(addPage)

    # workspace widgets
    editor.sections = QHBoxLayout()
    workspace.addLayout(editor.sections)
    editor.frame = QFrame(editor)
    editor.frame.setStyleSheet("background-color: white;")
    workspace.addWidget(editor.frame)


    # stylesheet reference
    container.setObjectName("container")
    editor.notebook_title.setObjectName("notebook_title")
    editor.pages_title.setObjectName("pages_title")
    editor.pages.setObjectName("pages")
    addPage.setObjectName("addPage")
    editor.pages_title.setText("Pages")



def build_window(editor):
    editor.setWindowTitle("ON - DEV")
    editor.screen_width, editor.screen_height = editor.geometry().width(), editor.geometry().height()
    editor.resize(editor.screen_width * 2, editor.screen_height * 2)
    editor.setAcceptDrops(True)
    editor.setAcceptDrops(True)
    with open('styles/styles.qss',"r") as fh:
        editor.setStyleSheet(fh.read())


def build_menubar(editor):
    file = editor.menuBar().addMenu('&File')
    #edit = editor.menuBar().addMenu('&edit')
    items = editor.menuBar().addMenu('&Items')

    new_file = build_action(editor, 'assets/icons/svg_file_open', 'New Notebook...', 'New Notebook', False)
    new_file.setShortcut(QKeySequence.StandardKey.New)
    new_file.triggered.connect(lambda: new(editor))

    open_file = build_action(editor, 'assets/icons/svg_file_open', 'Open Notebook...', 'Open Notebook', False)
    open_file.setShortcut(QKeySequence.StandardKey.Open)
    open_file.triggered.connect(lambda: load(editor))

    save_file = build_action(editor, 'assets/icons/svg_file_save', 'Save Notebook', 'Save Notebook', False)
    save_file.setShortcut(QKeySequence.StandardKey.Save)
    save_file.triggered.connect(lambda: save(editor, editor.notebook))

    save_fileAs = build_action(editor, 'assets/icons/svg_file_save', 'Save Notebook As...', 'Save Notebook As', False)
    save_fileAs.setShortcut(QKeySequence.fromString('Ctrl+Shift+S'))
    save_fileAs.triggered.connect(lambda: saveAs(editor, editor.notebook))

    file.addActions([new_file, open_file, save_file, save_fileAs])


def build_toolbar(editor):
    toolbar = QToolBar()
    toolbar.setIconSize(QSize(25, 25))
    toolbar.setMovable(False)
    editor.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    font = QFontComboBox()
    font.currentFontChanged.connect(lambda x: editor.selected.setCurrentFont(font.currentFont() if x else editor.selected.currentFont()))

    size = QComboBox()
    size.addItems([str(fs) for fs in FONT_SIZES])
    size.currentIndexChanged.connect(lambda x: editor.selected.setFontPointSize(float(x + 10) if x else editor.selected.fontPointSize()))

    bold = build_action(toolbar, 'assets/icons/svg_font_bold', "Bold", "Bold", True)
    bold.toggled.connect(lambda x: editor.selected.setFontWeight(700 if x else 500))

    italic = build_action(toolbar, 'assets/icons/svg_font_italic', "Italic", "Italic", True)
    italic.toggled.connect(lambda x: editor.selected.setFontItalic(True if x else False))

    underline = build_action(toolbar, 'assets/icons/svg_font_underline', "Underline", "Underline", True)
    underline.toggled.connect(lambda x: editor.selected.setFontUnderline(True if x else False))

    editor.add_section = QPushButton("Add Section")
    editor.add_section.clicked.connect(lambda: add_section(editor))

    editor.add_textbox = QPushButton("Add Text")
    editor.add_textbox.clicked.connect(lambda: add_object(editor, 'text'))

    editor.add_image = QPushButton("Add Image")
    editor.add_image.clicked.connect(lambda: add_object(editor, 'image'))

    toolbar.addWidget(font)
    toolbar.addWidget(size)
    toolbar.addActions([bold, italic, underline])
    toolbar.addSeparator()
    toolbar.addWidget(editor.add_section)
    toolbar.addWidget(editor.add_textbox)
    toolbar.addWidget(editor.add_image)


def build_action(parent, icon_path, action_name, set_status_tip, set_checkable):
    action = QAction(QIcon(icon_path), action_name, parent)
    action.setStatusTip(set_status_tip)
    action.setCheckable(set_checkable)
    return action


