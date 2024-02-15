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
    home = editor.menuBar().addMenu('&Home')
    insert = editor.menuBar().addMenu('&Insert')
    plugins = editor.menuBar().addMenu('&Plugins')

    new_file = build_action(editor, './Assets/icons/svg_file_open', 'New Notebook', 'New Notebook', False)
    new_file.setShortcut(QKeySequence.StandardKey.New)
    new_file.triggered.connect(lambda: new(editor))

    open_file = build_action(editor, './Assets/icons/svg_file_open', 'Open Notebook', 'Open Notebook', False)
    open_file.setShortcut(QKeySequence.StandardKey.Open)
    open_file.triggered.connect(lambda: load(editor))

    save_file = build_action(editor, './Assets/icons/svg_file_save', 'Save Notebook', 'Save Notebook', False)
    save_file.setShortcut(QKeySequence.StandardKey.Save)
    save_file.triggered.connect(lambda: save(editor))

    save_fileAs = build_action(editor, './Assets/icons/svg_file_save', 'Save Notebook As...', 'Save Notebook As', False)
    save_fileAs.setShortcut(QKeySequence.fromString('Ctrl+Shift+S'))
    save_fileAs.triggered.connect(lambda: saveAs(editor))

    toggle_home_toolbar = build_action(editor, '', 'Toggle Home Toolbar', 'Toggle Home Toolbar', False)
    toggle_home_toolbar.triggered.connect(lambda: set_toolbar_visibility(editor))

    toggle_insert_toolbar = build_action(editor, '', 'Toggle Insert Toolbar', 'Toggle Insert Toolbar', False)
    #toggle_insert_toolbar.triggered.connect(lambda: set_toolbar_visibility(insert))

    add_widget = build_action(editor, './Assets/icons/svg_question', 'Add Custom Widget', 'Add Custom Widget', False)

    file.addActions([new_file, open_file, save_file, save_fileAs])
    home.addActions([toggle_home_toolbar])
    insert.addActions([toggle_insert_toolbar])
    plugins.addActions([add_widget])

def set_toolbar_visibility(editor):
    toolbar = editor.findChild(QToolBar)
    if toolbar:
    	print("toolbar visibility change")
    	toolbar.setVisible(not toolbar.isVisible())

def build_toolbar(editor):
    toolbar = QToolBar()
    toolbar.setIconSize(QSize(16, 16))
    toolbar.setMovable(False)
    editor.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    #separates toolbar with a line break
    spacer = QWidget()
    spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    undo = build_action(toolbar, './Assets/icons/svg_undo', "undo", "undo", False)
    undo.triggered.connect(editor.frameView.triggerUndo)

    redo = build_action(toolbar, './Assets/icons/svg_redo', "redo", "redo", False)
    # redo.triggered.connect(editor.frameView.triggerRedo)


    font_family = QFontComboBox()
    default_font = font_family.currentFont().family()
    print(f"default font is {default_font}")
    font_family.currentFontChanged.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.Font, font_family.currentFont().family()))

    font_size = QComboBox()
    font_size.addItems([str(fs) for fs in FONT_SIZES])
    default_font_size_index = 8 #default text size is 18
    font_size.setCurrentIndex(default_font_size_index)
    font_size.currentIndexChanged.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontSize, int(font_size.currentText())))

    #current issues: 
    # - Alternates between working and not working
    # - Textboxes do not remember settings like if font is toggled or current font size

    bgColor = build_action(toolbar, './Assets/icons/svg_font_bucket', "Background Color", "Background Color", False)
    #bgColor.triggered.connect(lambda: openGetColorDialog(purpose = "background"))
    #current bug, alternates between activating and not working when using
    bgColor.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.BackgroundColor, QColorDialog.getColor()))

    textHighlightColor = build_action(toolbar, './Assets/icons/svg_textHighlightColor', "Text Highlight Color", "Text Highlight Color", True)

    textHighlightColor.toggled.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.TextHighlightColor, QColorDialog.getColor()))

    #defines font color icon appearance and settings
    fontColor = build_action(toolbar, './Assets/icons/svg_font_color', "Font Color", "Font Color", False)
    fontColor.triggered.connect(lambda: openGetColorDialog(purpose = "font"))

    bold = build_action(toolbar, './Assets/icons/bold', "Bold", "Bold", True)
    bold.toggled.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontBold, None))

    italic = build_action(toolbar, './Assets/icons/italic.svg', "Italic", "Italic", True)
    italic.toggled.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontItalic, None))

    underline = build_action(toolbar, './Assets/icons/underline.svg', "Underline", "Underline", True)
    underline.toggled.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontUnderline, None))

    table = build_action(toolbar, './Assets/icons/svg_table', "Create Table", "Create Table", False)
    table.triggered.connect(editor.frameView.toolbar_table)

    hyperlink = build_action(toolbar, './Assets/icons/svg_hyperlink', "Hyperlink", "Hyperlink", False)
    hyperlink.triggered.connect(editor.frameView.toolbar_hyperlink)
    
    # Bullets with placeholder for more bullet options
    bullet = build_action(toolbar, './Assets/icons/svg_bullets', "Bullets", "Bullets", False)
    bullet.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.Bullet, None))
    

    toolbar.addActions([undo, redo])
    
    toolbar.addSeparator()
    
    toolbar.addWidget(font_family)
    toolbar.addWidget(font_size)
    
    toolbar.addSeparator()
    
    toolbar.addActions([bold, italic, underline, fontColor, textHighlightColor, bgColor, bullet])

    # numbering menu start
    numbering_menu = QMenu(editor)
    
    bullet_num = build_action(numbering_menu, './Assets/icons/svg_bullet_number', "", "", False)
    bullet_num.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.Bullet_Num, None))

    bulletUpperA = build_action(numbering_menu, './Assets/icons/svg_bulletUA', "", "", False)
    bulletUpperA.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.BulletUA, None))

    bulletUpperR = build_action(numbering_menu, './Assets/icons/svg_bulletUR', "", "", False)
    bulletUpperR.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.BulletUR, None))

    numbering_menu.addAction(bullet_num)
    numbering_menu.addAction(bulletUpperA)
    numbering_menu.addAction(bulletUpperR)

    # cant directly add numbering menu to toolbar so this is required 
    numbering = QToolButton(editor)
    numbering.setIcon(QIcon('./Assets/icons/svg_bullet_number'))
    numbering.setPopupMode(QToolButton.MenuButtonPopup)
    numbering.setMenu(numbering_menu)

    toolbar.addWidget(numbering)
	
    align_left = build_action(toolbar,"./Assets/icons/svg_align_left","Align Left","Align Left",False)
    align_left.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.AlignLeft, None))

    align_center = build_action(toolbar,"./Assets/icons/svg_align_center","Align Center","Align Center",False)
    align_center.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.AlignCenter, None))
    align_right = build_action(toolbar, "./Assets/icons/svg_align_right", "Align Right", "Align Right", False)
    align_right.triggered.connect(lambda x: self.setAlignment(Qt.AlignRight))
    
    toolbar.addActions([align_left, align_center, align_right])
    
    toolbar.addSeparator()
    
    toolbar.addActions([table, hyperlink])

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
