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

import subprocess

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

def check_appearance():
    """Checks DARK/LIGHT mode of macos."""
    cmd = 'defaults read -g AppleInterfaceStyle'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True)
    return bool(p.communicate()[0])  

    
def build_window(editor):
    editor.setWindowTitle("OpenNote")
    editor.setWindowIcon(QIcon('./Assets/OpenNoteLogo.png'))
    editor.setAcceptDrops(True)

    if check_appearance() == False:
        with open('./Styles/styles.qss',"r") as fh:
            editor.setStyleSheet(fh.read())
    else:
        with open('./Styles/stylesDark.qss',"r") as fh:
            editor.setStyleSheet(fh.read())

def build_menubar(editor):
    file = editor.menuBar().addMenu('&File')
    home = editor.menuBar().addMenu('&Home')
    insert = editor.menuBar().addMenu('&Insert')
    draw = editor.menuBar().addMenu('&Draw')
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
    toggle_home_toolbar.triggered.connect(lambda: set_toolbar_visibility(editor, 'homeToolbar'))

    toggle_insert_toolbar = build_action(editor, '', 'Toggle Insert Toolbar', 'Toggle Insert Toolbar', False)
    toggle_insert_toolbar.triggered.connect(lambda: set_toolbar_visibility(editor, 'insertToolbar'))
    
    toggle_draw_toolbar = build_action(editor, '', 'Toggle Draw Toolbar', 'Toggle Draw Toolbar', False)
    toggle_draw_toolbar.triggered.connect(lambda: set_toolbar_visibility(editor, 'drawToolbar'))

    add_widget = build_action(editor, './Assets/icons/svg_question', 'Add Custom Widget', 'Add Custom Widget', False)

    file.addActions([new_file, open_file, save_file, save_fileAs])
    
    home.addActions([toggle_home_toolbar])
    
    insert.addActions([toggle_insert_toolbar])
    
    draw.addActions([toggle_draw_toolbar])
    
    plugins.addActions([add_widget])

def set_toolbar_visibility(editor, triggered_toolbar):
    # Find all toolbars in the editor
    toolbars = editor.findChildren(QToolBar)

    # Iterate over each toolbar
    for toolbar in toolbars:
        if toolbar.objectName() == triggered_toolbar:
            # Toggle the visibility of the triggered toolbar
            print(toolbar.objectName(),"visibility change")
            toolbar.setVisible(not toolbar.isVisible())
        else:
            # Hide all other toolbars
            toolbar.setVisible(False)

def build_toolbar(editor):
    # homeToolbar code
    homeToolbar = QToolBar()
    homeToolbar.setObjectName('homeToolbar')
    homeToolbar.setIconSize(QSize(16, 16))
    homeToolbar.setMovable(False)
    homeToolbar.setStyleSheet('font-size: 10pt;')
    editor.addToolBar(Qt.ToolBarArea.TopToolBarArea, homeToolbar)

    #separates toolbar with a line break
    spacer = QWidget()
    spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    cut = build_action(homeToolbar, './Assets/icons/svg_cut', "cut", "cut", False)
    cut.triggered.connect(editor.frameView.cutWidgetEvent)
    
    copy = build_action(homeToolbar, './Assets/icons/svg_copy', "copy", "copy", False)
    copy.triggered.connect(editor.frameView.copyWidgetEvent)


    font_family = QFontComboBox()
    font_family.setFixedWidth(150)
    default_font = font_family.currentFont().family()
    print(f"default font is {default_font}")
    font_family.currentFontChanged.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.Font, font_family.currentFont().family()))

    font_size = QComboBox()
    font_size.setFixedWidth(50)
    font_size.addItems([str(fs) for fs in FONT_SIZES])
    # default text size is 11
    default_font_size_index = 4
    font_size.setCurrentIndex(default_font_size_index)
    font_size.currentIndexChanged.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontSize, int(font_size.currentText())))

    #current issues: 
    # - Alternates between working and not working
    # - Textboxes do not remember settings like if font is toggled or current font size

    bgColor = build_action(homeToolbar, './Assets/icons/svg_font_bucket', "Background Color", "Background Color", False)
    #bgColor.triggered.connect(lambda: openGetColorDialog(purpose = "background"))
    #current bug, alternates between activating and not working when using
    bgColor.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.BackgroundColor, QColorDialog.getColor()))

    textHighlightColor = build_action(homeToolbar, './Assets/icons/svg_textHighlightColor', "Text Highlight Color", "Text Highlight Color", True)

    textHighlightColor.toggled.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.TextHighlightColor, QColorDialog.getColor()))

    #defines font color icon appearance and settings
    fontColor = build_action(homeToolbar, './Assets/icons/svg_font_color', "Font Color", "Font Color", False)
    fontColor.triggered.connect(lambda: openGetColorDialog(purpose = "font"))

    bold = build_action(homeToolbar, './Assets/icons/bold', "Bold", "Bold", True)
    bold.toggled.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontBold, None))

    italic = build_action(homeToolbar, './Assets/icons/italic.svg', "Italic", "Italic", True)
    italic.toggled.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontItalic, None))

    underline = build_action(homeToolbar, './Assets/icons/underline.svg', "Underline", "Underline", True)
    underline.toggled.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontUnderline, None))
    
    # Bullets with placeholder for more bullet options
    bullet = build_action(homeToolbar, './Assets/icons/svg_bullets', "Bullets", "Bullets", False)
    bullet.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.Bullet, None))

    paperColor= build_action(homeToolbar, './Assets/icons/svg_paper', "Paper Color", "Paper Color", False)
    paperColor.triggered.connect(lambda: editor.frameView.pageColor(QColorDialog.getColor()))
    
    homeToolbar.addActions([cut, copy])
    
    homeToolbar.addSeparator()
    
    homeToolbar.addWidget(font_family)
    homeToolbar.addWidget(font_size)
    
    homeToolbar.addSeparator()
    
    homeToolbar.addActions([bold, italic, underline, fontColor, textHighlightColor, bgColor, paperColor, bullet])


    # numbering menu start
    numbering_menu = QMenu(editor)
    
    bullet_num = build_action(numbering_menu, './Assets/icons/svg_bullet_number', "", "", False)
    bullet_num.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.Bullet_Num, None))
    
    bullet_num = build_action(numbering_menu, './Assets/icons/svg_bullet_number', "", "", False)
    bullet_num.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.Bullet_Num, None))
    bulletUpperA = build_action(numbering_menu, './Assets/icons/svg_bulletUA', "", "", False)
    bulletUpperA.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.BulletUA, None))
    bulletUpperR = build_action(numbering_menu, './Assets/icons/svg_bulletUR', "", "", False)
    bulletUpperR.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.BulletUR, None))

    numbering_menu.addActions([bullet_num, bulletUpperA, bulletUpperR])

    # cant directly add numbering menu to homeToolbar so this is required 
    numbering = QToolButton(editor)
    numbering.setIcon(QIcon('./Assets/icons/svg_bullet_number'))
    numbering.setIconSize(QSize(16,16))
    numbering.setPopupMode(QToolButton.MenuButtonPopup)
    numbering.setMenu(numbering_menu)
    
    homeToolbar.addWidget(numbering)
    
    # QActionGroup used to display that only one can be toggled at a time
    align_group = QActionGroup(homeToolbar)
    
    align_left = build_action(align_group,"./Assets/icons/svg_align_left","Align Left","Align Left", True)
    align_left.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.AlignLeft, None))
    align_center = build_action(align_group,"./Assets/icons/svg_align_center","Align Center","Align Center", True)
    align_center.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.AlignCenter, None))
    align_right = build_action(align_group, "./Assets/icons/svg_align_right", "Align Right", "Align Right", True)
    align_right.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.AlignRight, None))
    
    align_group.addAction(align_left)
    align_group.addAction(align_center)
    align_group.addAction(align_right)
    homeToolbar.addActions(align_group.actions())

    homeToolbar.addSeparator()
    
    
    # insertToolbar code 
    insertToolbar = QToolBar()
    insertToolbar.setObjectName('insertToolbar')
    insertToolbar.setIconSize(QSize(16,16))
    insertToolbar.setStyleSheet('font-size: 10pt;')
    insertToolbar.setMovable(False)
    insertToolbar.setVisible(False)
    editor.addToolBar(Qt.ToolBarArea.TopToolBarArea, insertToolbar)
    
    table = build_button(insertToolbar, './Assets/icons/svg_table', " Table ", "Add a Table", False)
    table.clicked.connect(editor.frameView.toolbar_table)
    
    insertSpace = build_button(insertToolbar, './Assets/icons/svg_insert_space', "Insert Space", "Insert Space", False)
    
    screensnip = build_button(insertToolbar, './Assets/icons/svg_screensnip', " Screensnip ", "Screensnip", False)
    screensnip.clicked.connect(editor.frameView.toolbar_snipScreen)
    
    pictures = build_button(insertToolbar, './Assets/icons/svg_pictures', " Pictures ", "Pictures", False)
    pictures.clicked.connect(editor.frameView.toolbar_pictures)

    hyperlink = build_button(insertToolbar, './Assets/icons/svg_hyperlink', " Hyperlink ", "Hyperlink", False)
    hyperlink.clicked.connect(editor.frameView.toolbar_hyperlink)
    
    insertToolbar.addWidget(table) 
    
    insertToolbar.addSeparator()
    
    insertToolbar.addWidget(insertSpace)
    
    insertToolbar.addSeparator()
    
    insertToolbar.addWidget(screensnip)
    insertToolbar.addWidget(pictures)
    
    insertToolbar.addSeparator()
    
    insertToolbar.addWidget(hyperlink)
    insertToolbar.addSeparator()
    
    # drawToolbar code
    drawToolbar = QToolBar()
    drawToolbar.setObjectName('drawToolbar')
    drawToolbar.setIconSize(QSize(16, 16))
    drawToolbar.setMovable(False)
    drawToolbar.setVisible(False)
    editor.addToolBar(Qt.ToolBarArea.TopToolBarArea, drawToolbar)
    
    undo = build_action(drawToolbar, './Assets/icons/svg_undo', "undo", "undo", False)
    undo.triggered.connect(editor.frameView.triggerUndo)

    redo = build_action(drawToolbar, './Assets/icons/svg_redo', "redo", "redo", False)
    # redo.triggered.connect(editor.frameView.triggerRedo)
    
    drawToolbar.addActions([undo, redo])
    
    drawToolbar.addSeparator()

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
    
def build_button(parent, icon_path, text, tooltip, checkable):
    button = QPushButton(parent)
    button.setIcon(QIcon(icon_path))
    button.setText(text)
    button.setToolTip(tooltip)
    button.setCheckable(checkable)
    return button
