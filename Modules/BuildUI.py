from Modules.Save import save, saveAs
from Modules.Load import new, load

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from Modules.EditorSignals import editorSignalsInstance, ChangedWidgetAttribute

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

#builds the application's UI
def build_ui(editor):
    print("Building UI...")

    #editor.statusBar = editor.statusBar()
    build_window(editor)
    build_menubar(editor)
    #build_toolbar(editor)

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
    rightSideLayout.setSpacing(0)
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
    save_fileAs.triggered.connect(lambda: saveAs(editor))

    file.addActions([new_file, open_file, save_file, save_fileAs])

def build_toolbar(editor):
    toolbar = QToolBar()
    toolbar.setIconSize(QSize(15, 15))
    toolbar.setMovable(False)
    editor.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    font = QFontComboBox()
    font.currentFontChanged.connect(lambda x: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.Font, font.currentFont()))

    size = QComboBox()
    size.addItems([str(fs) for fs in FONT_SIZES])
    size.currentIndexChanged.connect(lambda x: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontSize, int(size.currentText())))

    fontColor = build_action(toolbar, 'assets/icons/svg_font_color', "Font Color", "Font Color", False)
    fontColor.triggered.connect(lambda x: openGetColorDialog(purpose = "font"))

    bgColor = build_action(toolbar, 'assets/icons/svg_font_bucket', "Text Box Color", "Text Box Color", False)
    bgColor.triggered.connect(lambda x: openGetColorDialog(purpose = "background"))

    bold = build_action(toolbar, 'assets/icons/bold', "Bold", "Bold", True)
    bold.triggered.connect(lambda x: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontBold, None))

    italic = build_action(toolbar, 'assets/icons/italic.svg', "Italic", "Italic", True)
    italic.triggered.connect(lambda x: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontItalic, None))

    underline = build_action(toolbar, 'assets/icons/underline.svg', "Underline", "Underline", True)
    underline.triggered.connect(lambda x: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontUnderline, None))

    toolbar.addWidget(font)
    toolbar.addWidget(size)
    toolbar.addActions([bgColor, fontColor, bold, italic, underline])

def openGetColorDialog(purpose):
    color = QColorDialog.getColor()
    if color.isValid():
        if purpose == "font":
            editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontColor, color)
        elif purpose == "background":
            editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.BackgroundColor, color)

def build_action(parent, icon_path, action_name, set_status_tip, set_checkable):
    action = QAction(QIcon(icon_path), action_name, parent)
    action.setStatusTip(set_status_tip)
    return action
