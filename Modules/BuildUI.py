from Modules.Save import save, saveAs
from Modules.Load import new, load

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from Models.DraggableContainer import DraggableContainer
from Widgets.Textbox import *

from Modules.EditorSignals import editorSignalsInstance, ChangedWidgetAttribute
from Modules.Undo import UndoHandler
from Widgets.Table import *

from Views.EditorFrameView import *

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

#builds the application's UI
def build_ui(editor):
    print("Building UI...")

    
    #editor.EditorFrameView = EditorFrameView(editor)
    #editor.statusBar = editor.statusBar()
    build_window(editor)
    build_menubar(editor)
    build_toolbar(editor)
    #build_test_toolbar(editor)

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

    addSectionButton = QPushButton("Add Section")
    #add functionality e.g. addSectionButton.clcicked.connect(editor.add_section_function)
    leftSideLayout.addWidget(addSectionButton)

def build_window(editor):
    editor.setWindowTitle("OpenNote")
    editor.setWindowIcon(QIcon('./Assets/OpenNoteLogo.png'))
    editor.setAcceptDrops(True)
    with open('./Styles/styles.qss',"r") as fh:
        editor.setStyleSheet(fh.read())

def build_menubar(editor):
    file = editor.menuBar().addMenu('&File')
    plugins = editor.menuBar().addMenu('&Plugins')

    new_file = build_action(editor, 'assets/icons/svg_file_open', 'New Notebook', 'New Notebook', False)
    new_file.setShortcut(QKeySequence.StandardKey.New)
    new_file.triggered.connect(lambda: new(editor))

    open_file = build_action(editor, 'assets/icons/svg_file_open', 'Open Notebook', 'Open Notebook', False)
    open_file.setShortcut(QKeySequence.StandardKey.Open)
    open_file.triggered.connect(lambda: load(editor))

    save_file = build_action(editor, 'assets/icons/svg_file_save', 'Save Notebook', 'Save Notebook', False)
    save_file.setShortcut(QKeySequence.StandardKey.Save)
    save_file.triggered.connect(lambda: save(editor))

    save_fileAs = build_action(editor, 'assets/icons/svg_file_save', 'Save Notebook As...', 'Save Notebook As', False)
    save_fileAs.setShortcut(QKeySequence.fromString('Ctrl+Shift+S'))
    save_fileAs.triggered.connect(lambda: saveAs(editor))

    add_widget = build_action(editor, 'assets/icons/svg_question', 'Add Custom Widget', 'Add Custom Widget', False)

    file.addActions([new_file, open_file, save_file, save_fileAs])
    plugins.addActions([add_widget])

def build_toolbar(editor):
    toolbar = QToolBar()
    toolbar.setIconSize(QSize(16, 16))
    toolbar.setMovable(False)
    editor.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    #separates toolbar with a line break
    spacer = QWidget()
    spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    toolbar_undo = build_action(toolbar, 'assets/icons/svg_undo', "undo", "undo", False)
    toolbar_undo.triggered.connect(editor.frameView.triggerUndo)


    redo = build_action(toolbar, 'assets/icons/svg_redo', "redo", "redo", False)
    


    font_family = QFontComboBox()
    font_family.currentFontChanged.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.Font, font_family.currentFont().family()))

    font_size = QComboBox()
    font_size.addItems([str(fs) for fs in FONT_SIZES])
    font_size.currentIndexChanged.connect(lambda x: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontSize, int(font_size.currentText())))

    #current issues: 
    # - Alternates between working and not working
    # - Textboxes do not remember settings like if font is toggled or current font size

    bgColor = build_action(toolbar, 'assets/icons/svg_font_bucket', "Background Color", "Background Color", False)
    #bgColor.triggered.connect(lambda: openGetColorDialog(purpose = "background"))
    #current bug, alternates between activating and not working when using
    bgColor.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.BackgroundColor, QColorDialog.getColor()))

    textboxColor = build_action(toolbar, 'assets/icons/svg_textboxColor', "Text Box Color", "Text Box Color", True)
    textboxColor.toggled.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.TextboxColor, QColorDialog.getColor()))

    #defines font color icon appearance and settings
    fontColor = build_action(toolbar, 'assets/icons/svg_font_color', "Font Color", "Font Color", False)
    fontColor.triggered.connect(lambda: openGetColorDialog(purpose = "font"))

    bold = build_action(toolbar, 'assets/icons/bold', "Bold", "Bold", True)
    bold.toggled.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontBold, None))

    italic = build_action(toolbar, 'assets/icons/italic.svg', "Italic", "Italic", True)
    italic.toggled.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontItalic, None))

    underline = build_action(toolbar, 'assets/icons/underline.svg', "Underline", "Underline", True)
    underline.toggled.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontUnderline, None))

    table = build_action(toolbar, 'assets/icons/svg_table', "Create Table", "Create Table", False)
    table.triggered.connect(editor.frameView.toolbar_table)

    hyperlink = build_action(toolbar, 'assets/icons/svg_hyperlink', "Hyperlink", "Hyperlink", False)
    hyperlink.triggered.connect(editor.frameView.toolbar_hyperlink)

    bullet = build_action(toolbar, 'assets/icons/svg_bullets', "Bullet List", "Bullet List", False)
    bullet.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.Bullet, None))

    '''
    editor.action1 = QAction('Action 1', editor)
    #editor.action1.triggered.connect(EditorFrameView.slot_action1)
    toolbar.addAction(editor.action1)
    editor.action2 = QAction('Action 2', editor)
    #editor.action2.triggered.connect(TextboxWidget.slot_action2)
    #editor.action2.triggered.connect(show_popup)
    toolbar.addAction(editor.action2)
    #editor.button = QPushButton("Click Me", editor)
    #editor.button.clicked.connect(editor.slot_button_click)'''
    

    toolbar.addActions([toolbar_undo, redo])
    toolbar.addSeparator()
    toolbar.addWidget(font_family)
    toolbar.addWidget(font_size)
    toolbar.addSeparator()
    toolbar.addActions([bgColor, textboxColor, fontColor, bold, italic, underline])
    toolbar.addSeparator()
    toolbar.addActions([table, hyperlink, bullet])

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
    action.setCheckable(set_checkable)
    return action