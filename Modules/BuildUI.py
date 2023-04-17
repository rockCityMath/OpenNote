from Modules.Enums import WidgetType
from Modules.Save import save, saveAs
from Modules.Load import new, load
from Modules.ObjectActions import add_object, paste_object
from Modules.Views.EditorFrameView import EditorFrameView

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

#builds the application's UI
def build_ui(editor):
    print("Building UI...")

    #editor.statusBar = editor.statusBar()
    build_window(editor)
    build_menubar(editor)
    build_toolbar(editor)

    # Application's main layout (grid)
    gridLayout = QGridLayout()
    gridContainerWidget = QWidget()
    editor.setCentralWidget(gridContainerWidget)
    gridContainerWidget.setLayout(gridLayout)

    gridLayout.setSpacing(3)
    gridLayout.setContentsMargins(6, 6, 0, 0)

    gridLayout.setColumnStretch(0, 1) # The left side (index 0) will take up 1/7? of the space of the right
    gridLayout.setColumnStretch(1, 7)

    # Left side of the app's layout
    leftSideLayout = QVBoxLayout()
    leftSideContainerWidget = QWidget()
    leftSideContainerWidget.setLayout(leftSideLayout)
    leftSideLayout.setContentsMargins(0, 0, 0, 0)
    leftSideLayout.setSpacing(0)

    # Right side of the app's layout
    rightSideLayout = QVBoxLayout()
    rightSideContainerWidget = QWidget()
    rightSideContainerWidget.setLayout(rightSideLayout)
    rightSideLayout.setContentsMargins(0, 0, 0, 0)
    rightSideLayout.setSpacing(3)
    rightSideLayout.setStretch(0, 0)
    rightSideLayout.setStretch(1, 1)

    # Add appropriate widgets (ideally just view controllers) to their layouts
    leftSideLayout.addWidget(editor.notebookTitleView, 0)
    leftSideLayout.addWidget(editor.pageView, 1) # Page view has max stretch factor
    rightSideLayout.addWidget(editor.sectionView, 0)
    rightSideLayout.addWidget(editor.frameView, 1) # Frame view has max stretch factor

    # Add L+R container's widgets to the main grid
    gridLayout.addWidget(leftSideContainerWidget, 0, 0)
    gridLayout.addWidget(rightSideContainerWidget, 0, 1)

def build_window(editor):
    editor.setWindowTitle("OpenNote")
    editor.setAcceptDrops(True)
    with open('styles/styles.qss',"r") as fh:
        editor.setStyleSheet(fh.read())

def build_menubar(editor):
    file = editor.menuBar().addMenu('&File')
    plugins = editor.menuBar().addMenu('&Plugins')

    new_file = build_action(editor, 'assets/icons/svg_file_open', 'New Notebook...', 'New Notebook', False)
    new_file.setShortcut(QKeySequence.StandardKey.New)
    new_file.triggered.connect(lambda: new(editor))

    open_file = build_action(editor, 'assets/icons/svg_file_open', 'Open Notebook...', 'Open Notebook', False)
    open_file.setShortcut(QKeySequence.StandardKey.Open)
    open_file.triggered.connect(lambda: load(editor))

    save_file = build_action(editor, 'assets/icons/svg_file_save', 'Save Notebook', 'Save Notebook', False)
    save_file.setShortcut(QKeySequence.StandardKey.Save)
    save_file.triggered.connect(lambda: save(editor))

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

    # debt: The second lambda function is unclear and not good ux, it unselects the highlighted text after setting the font
    # size.currentIndexChanged.connect(lambda x: editor.selected.setFontPointSize(int(size.currentText()) if x else editor.selected.fontPointSize()))
    size.currentIndexChanged.connect(lambda x: changeFontSize(x))

    def changeFontSize(x):
        editor.selected.setFontPointSize(int(size.currentText()) if x else editor.selected.fontPointSize())

        cursor = editor.selected.textCursor()
        cursor.clearSelection()
        editor.selected.setTextCursor(cursor)


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
