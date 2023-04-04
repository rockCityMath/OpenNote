from modules.save import save, saveAs
from modules.load import new, load
from modules.page import add_page
from modules.section import add_section
from modules.object import add_object, add_plugin_object, paste_object
from modules.plugins import get_plugins

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
    sidebar_widget = QWidget()
    sidebar_widget.setFixedWidth(250)
    sidebar_widget.setLayout(sidebar)
    workspace = QVBoxLayout()
    grid.addWidget(sidebar_widget)
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
    sidebar.setContentsMargins(0, 0, 0, 0)
    editor.pages.setContentsMargins(0, 0, 0, 0)
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
    sections = QHBoxLayout()
    sections_widget = QWidget()
    sections_widget.setFixedHeight(40)
    sections_widget.setLayout(sections)

    editor.sections = QHBoxLayout()
    editor.sections_frame = QFrame()

    editor.add_section = QPushButton("+")
    editor.add_section.setFixedWidth(50)
    editor.add_section.setStyleSheet("background-color: #c2c2c2;")
    editor.add_section.clicked.connect(lambda: add_section(editor))
    sections.addWidget(editor.add_section)
    sections.addLayout(editor.sections)
    sections.addWidget(editor.sections_frame)
    sections.setContentsMargins(0, 0, 0, 0)
    editor.sections.setContentsMargins(0, 0, 0, 0)
    workspace.addWidget(sections_widget)

    editor.frame = QFrame(editor)
    editor.frame.setStyleSheet("background-color: white;")
    editor.frame.mousePressEvent = lambda event: frame_menu(editor, event)
    workspace.addWidget(editor.frame)

    # stylesheet reference
    container.setObjectName("container")
    editor.notebook_title.setObjectName("notebook_title")
    editor.pages_title.setObjectName("pages_title")
    editor.pages.setObjectName("pages")
    addPage.setObjectName("addPage")
    editor.pages_title.setText("Pages")

def build_window(editor):
    editor.setWindowTitle("OpenNote")
    editor.screen_width, editor.screen_height = editor.geometry().width(), editor.geometry().height()
    editor.resize(editor.screen_width * 2, editor.screen_height * 2)
    editor.setAcceptDrops(True)
    editor.setAcceptDrops(True)
    with open('styles/styles.qss',"r") as fh:
        editor.setStyleSheet(fh.read())

def build_menubar(editor):
    file = editor.menuBar().addMenu('&File')
    #edit = editor.menuBar().addMenu('&edit')
    plugins = editor.menuBar().addMenu('&Plugins')

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
    size.currentIndexChanged.connect(lambda x: editor.selected.setFontPointSize(int(size.currentText()) if x else editor.selected.fontPointSize()))

    bold = build_action(toolbar, 'assets/icons/svg_font_bold', "Bold", "Bold", True)
    bold.toggled.connect(lambda x: editor.selected.setFontWeight(700 if x else 500))

    italic = build_action(toolbar, 'assets/icons/svg_font_italic', "Italic", "Italic", True)
    italic.toggled.connect(lambda x: editor.selected.setFontItalic(True if x else False))

    underline = build_action(toolbar, 'assets/icons/svg_font_underline', "Underline", "Underline", True)
    underline.toggled.connect(lambda x: editor.selected.setFontUnderline(True if x else False))

    toolbar.addWidget(font)
    toolbar.addWidget(size)
    toolbar.addActions([bold, italic, underline])

def build_action(parent, icon_path, action_name, set_status_tip, set_checkable):
    action = QAction(QIcon(icon_path), action_name, parent)
    action.setStatusTip(set_status_tip)
    action.setCheckable(set_checkable)
    return action

def frame_menu(editor, event):
    # if editor.selected != None:
    #     if editor.selected.type == 'text':
    #         textCursor = editor.selected.textCursor()
    #         textCursor.clearSelection()
    #         editor.selected.setTextCursor(textCursor)
    if event.buttons() == Qt.LeftButton:
        o = len(editor.object) - 1
        if len(editor.object) > 0:
            if editor.notebook.page[editor.page].section[editor.section].object[o].type == 'text':
                if editor.object[o].childWidget.toPlainText() == '':
                    editor.object[o].deleteLater()
                    editor.object.pop(o)
                    editor.notebook.page[editor.page].section[editor.section].object.pop(o)
                    editor.autosaver.onChangeMade()
        add_object(editor, event, 'text')
        editor.object[len(editor.object) - 1].childWidget.setFocus()

    # Open Context Menu
    if event.buttons() == Qt.RightButton:
        editor.setFocus()
        if editor.section > -1:
            frame_menu = QMenu(editor)

            # add_text = QAction("Add Text", editor)
            # add_text.triggered.connect(lambda: add_object(editor, event, 'text'))
            # frame_menu.addAction(add_text)

            add_image = QAction("Add Image", editor)
            add_image.triggered.connect(lambda: add_object(editor, event, 'image_object'))
            frame_menu.addAction(add_image)

            add_table = QAction("Add Table", editor)
            add_table.triggered.connect(lambda: add_object(editor, event, 'table'))
            frame_menu.addAction(add_table)

            paste = QAction("Paste", editor)
            paste.triggered.connect(lambda: paste_object(editor, event))
            frame_menu.addAction(paste)

            take_screensnip = QAction("Snip Screen", editor)
            take_screensnip.triggered.connect(lambda: editor.snipArea({'x': event.pos().x(), 'y': event.pos().y()}))
            frame_menu.addAction(take_screensnip)

#            lambduhs=[]
#            for name, c in get_plugins():
#                displayName = getattr(c,"DisplayName",name)
#                shortcut = getattr(c,"ShortcutKey","")
#                item_action = QAction(displayName, editor)
#                if shortcut!="":
#                        item_action.setShortcut(QKeySequence.fromString(shortcut))
#                def tmp(name,c):
#                    return lambda: add_plugin_object(editor,event,name,c)
#                item_action.triggered.connect(tmp(name,c))
#                frame_menu.addAction(item_action)

            frame_menu.exec(event.globalPos())
