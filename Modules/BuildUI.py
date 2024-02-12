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
def build_ui(self):
    print("Building UI...")

    
    #self.selfFrameView = selfFrameView(self)
    #self.statusBar = self.statusBar()
    build_window(self)
    build_menubar(self)
    build_toolbar(self)
    #build_test_toolbar(self)

    # Application's main layout (grid)
    gridLayout = QGridLayout()
    gridContainerWidget = QWidget()
    self.setCentralWidget(gridContainerWidget)
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
    leftSideLayout.addWidget(self.notebookTitleView, 0)
    leftSideLayout.addWidget(self.pageView, 1) # Page view has max stretch factor
    rightSideLayout.addWidget(self.sectionView, 0)
    rightSideLayout.addWidget(self.frameView, 1) # Frame view has max stretch factor

    # Add L+R container's widgets to the main grid
    gridLayout.addWidget(leftSideContainerWidget, 0, 0)
    gridLayout.addWidget(rightSideContainerWidget, 0, 1)

    addSectionButton = QPushButton("Add Section")
    #add functionality e.g. addSectionButton.clcicked.connect(self.add_section_function)
    leftSideLayout.addWidget(addSectionButton)

    
    
def build_window(self):
    self.setWindowTitle("OpenNote")
    self.setWindowIcon(QIcon('./Assets/OpenNoteLogo.png'))
    self.setAcceptDrops(True)
    with open('./Styles/styles.qss',"r") as fh:
        self.setStyleSheet(fh.read())

def build_menubar(self):
    file = self.menuBar().addMenu('&File')
    plugins = self.menuBar().addMenu('&Plugins')

    new_file = build_action(self, './Assets/icons/svg_file_open', 'New Notebook', 'New Notebook', False)
    new_file.setShortcut(QKeySequence.StandardKey.New)
    new_file.triggered.connect(lambda: new(self))

    open_file = build_action(self, './Assets/icons/svg_file_open', 'Open Notebook', 'Open Notebook', False)
    open_file.setShortcut(QKeySequence.StandardKey.Open)
    open_file.triggered.connect(lambda: load(self))

    save_file = build_action(self, './Assets/icons/svg_file_save', 'Save Notebook', 'Save Notebook', False)
    save_file.setShortcut(QKeySequence.StandardKey.Save)
    save_file.triggered.connect(lambda: save(self))

    save_fileAs = build_action(self, './Assets/icons/svg_file_save', 'Save Notebook As...', 'Save Notebook As', False)
    save_fileAs.setShortcut(QKeySequence.fromString('Ctrl+Shift+S'))
    save_fileAs.triggered.connect(lambda: saveAs(self))

    add_widget = build_action(self, './Assets/icons/svg_question', 'Add Custom Widget', 'Add Custom Widget', False)

    file.addActions([new_file, open_file, save_file, save_fileAs])
    plugins.addActions([add_widget])

def build_toolbar(self):
    toolbar = QToolBar()
    toolbar.setIconSize(QSize(16, 16))
    toolbar.setMovable(False)
    self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    '''
    tabs = QTabWidget()
    tabs.addTab(self.homeTabUI(), "Home")
    layout.addWidget(tabs)
    '''
    #create tab bar
    tab_bar = QTabBar(self)
    toolbar.addWidget(tab_bar)

    #create tabs
    home_tab = tab_bar.addTab("Home")
    insert_tab = tab_bar.addTab("Insert")
    draw_tab = tab_bar.addTab("Draw")
    view_tab = tab_bar.addTab("View")

    '''centralWidget = QWidget(self)
    self.setCentralWidget(centralWidget)
    layout = QVBoxLayout(centralWidget)
    layout.addWidget(tab_bar)

    home_toolbar = QToolBar("Home Toolbar", self)
    home_toolbar.addAction("Action 1")

    layout.addWidget(home_toolbar)   ''' 

    #separates toolbar with a line break
    spacer = QWidget()
    spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    toolbar_undo = build_action(toolbar, './Assets/icons/svg_undo', "undo", "undo", False)
    toolbar_undo.triggered.connect(self.frameView.triggerUndo)


    redo = build_action(toolbar, './Assets/icons/svg_redo', "redo", "redo", False)
    


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

    textboxColor = build_action(toolbar, './Assets/icons/svg_textboxColor', "Text Box Color", "Text Box Color", True)
    textboxColor.toggled.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.TextboxColor, QColorDialog.getColor()))

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
    table.triggered.connect(self.frameView.toolbar_table)

    hyperlink = build_action(toolbar, './Assets/icons/svg_hyperlink', "Hyperlink", "Hyperlink", False)
    hyperlink.triggered.connect(self.frameView.toolbar_hyperlink)

    bullets = build_action(toolbar, './Assets/icons/svg_bullets', "Bullets", "Bullets", False)

    bullet_reg = build_action(toolbar, './Assets/icons/svg_bullets', "Bullet List", "Bullet List", False)
    bullet_reg.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.Bullet, None))

    bullet_num = build_action(toolbar, './Assets/icons/svg_bullet_number', "Bullet List", "Bullet List", False)
    bullet_num.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.Bullet_Num, None))

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
    toolbar.addActions([table, hyperlink, bullet_reg, bullet_num])

    #-------- BG Color -----------
    bgColor = build_action(toolbar, './Assets/icons/svg_bullets', "Bullets", "Bullets", False)

    bgColor_menu = QMenu(self)

    bgColor = QToolButton(self)
    bgColor.setIcon(QIcon('./Assets/icons/svg_font_bucket'))
    bgColor.setPopupMode(QToolButton.InstantPopup)
    bgColor.setMenu(bgColor_menu)
    presetColors = ['blue', '#ffcc00', '#66ff66', '#3399ff']
    for color in presetColors:
        presetAction = QAction(color, self)
        bgColor_menu.addAction(presetAction)
    toolbar.addWidget(bgColor)

    #-----------------------------
    bullets_menu = QMenu(self)

    bulletUpperA = build_action(bullets_menu, './Assets/icons/svg_bulletUA', "", "", False)
    bulletUpperA.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.BulletUA, None))

    bulletUpperR = build_action(bullets_menu, './Assets/icons/svg_bulletUR', "", "", False)
    bulletUpperR.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.BulletUR, None))

    bullets_menu.addAction(bulletUpperA)
    bullets_menu.addAction(bulletUpperR)

    bullets = QToolButton(self)
    bullets.setIcon(QIcon('./Assets/icons/svg_bullets'))
    bullets.setPopupMode(QToolButton.InstantPopup)
    bullets.setMenu(bullets_menu)

    toolbar.addWidget(bullets)

    #toolbar.setStyleSheet("QToolBar { background-color: #FFFFFF; }")

def homeTabUI(self):
    homeTab = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(QCheckBox("General Option 1"))
    layout.addWidget(QCheckBox("General Option 2"))
    homeTab.setLayout(layout)
    return homeTab

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