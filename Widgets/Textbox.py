from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from Modules.EditorSignals import editorSignalsInstance

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

class TextboxWidget(QTextEdit):
    def __init__(self, x, y, w = 15, h = 30, t = ''):
        super().__init__()

        self.setGeometry(x, y, w, h)                       # This sets geometry of DraggableObject
        self.setText(t)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textChanged.connect(self.textChangedEvent)
        self.setStyleSheet('background-color: rgba(0, 0, 0, 0);')
        self.setTextColor('black')
        
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            # A click occurred outside the QTextEdit
            self.clearFocus()
            cursor = self.textCursor()
            cursor.clearSelection()
            self.setTextCursor(cursor)

        return super().eventFilter(obj, event)

        
    
    def textChangedEvent(self):
        if len(self.toPlainText()) < 2:
            self.resize(100, 100)

    @staticmethod
    def new(clickPos: QPoint):
        return TextboxWidget(clickPos.x(), clickPos.y())

    def __getstate__(self):
        data = {}

        data['geometry'] = self.parentWidget().geometry()
        data['content'] = self.toHtml()
        data['stylesheet'] = self.styleSheet()
        return data

    def __setstate__(self, data):
        self.__init__(data['geometry'].x(), data['geometry'].y(), data['geometry'].width(), data['geometry'].height(), data['content'])
        self.setStyleSheet(data['stylesheet'])

    def checkEmpty(self):
        if len(self.toPlainText()) < 1:
            return True
        return False

    def customMenuItems(self):
        def build_action(parent, icon_path, action_name, set_status_tip, set_checkable):
            action = QAction(QIcon(icon_path), action_name, parent)
            action.setStatusTip(set_status_tip)
            action.setCheckable(set_checkable)
            return action

        toolbarTop = QToolBar()
        toolbarTop.setIconSize(QSize(25, 25))
        toolbarTop.setMovable(False)

        toolbarBottom = QToolBar()
        toolbarBottom.setIconSize(QSize(25, 25))
        toolbarBottom.setMovable(False)

        font = QFontComboBox()
        font.currentFontChanged.connect(lambda x: self.setCurrentFontCustom(font.currentFont() if x else self.currentFont()))

        size = QComboBox()
        size.addItems([str(fs) for fs in FONT_SIZES])
        size.currentIndexChanged.connect(lambda x: self.setFontPointSizeCustom(FONT_SIZES[x] if x else self.fontPointSize()))

        bold = build_action(toolbarBottom, 'assets/icons/svg_font_bold', "Bold", "Bold", True)
        bold.toggled.connect(lambda x: self.setFontWeightCustom(700 if x else 500))

        italic = build_action(toolbarBottom, 'assets/icons/svg_font_italic', "Italic", "Italic", True)
        italic.toggled.connect(lambda x: self.setFontItalicCustom(True if x else False))
        

        underline = build_action(toolbarBottom, 'assets/icons/svg_font_underline', "Underline", "Underline", True)
        underline.toggled.connect(lambda x: self.setFontUnderlineCustom(True if x else False))

        fontColor = build_action(toolbarBottom, 'assets/icons/svg_font_color', "Font Color", "Font Color", False)
        fontColor.triggered.connect(lambda: self.setTextColorCustom(QColorDialog.getColor()))

        bgColor = build_action(toolbarBottom, 'assets/icons/svg_font_bucket', "Background Color", "Background Color", False)
        #bgColor.triggered.connect(lambda: self.setBackgroundColor(QColorDialog.getColor()))
        bgColor.triggered.connect(lambda: self.changeBackgroundColorEvent(QColorDialog.getColor()))
        textboxColor = build_action(toolbarBottom, 'assets/icons/svg_textboxColor', "Background Color", "Background Color", False)
        textboxColor.triggered.connect(lambda: self.changeTextboxColorEvent(QColorDialog.getColor()))

        toolbarTop.addWidget(font)
        toolbarTop.addWidget(size)
        toolbarBottom.addActions([bold, italic, underline, fontColor, bgColor, textboxColor])
        qwaTop = QWidgetAction(self)
        qwaTop.setDefaultWidget(toolbarTop)
        qwaBottom = QWidgetAction(self)
        qwaBottom.setDefaultWidget(toolbarBottom)

        return [qwaTop, qwaBottom]

    def setFontItalicCustom(self, italic: bool):
        if not self.applyToAllIfNoSelection(lambda: self.setFontItalic(italic)):
            print("setFontItalicCustom Called")
            self.setFontItalic(italic)

    def setFontWeightCustom(self, weight: int):
        if not self.applyToAllIfNoSelection(lambda: self.setFontWeight(weight)):
            self.setFontWeight(weight)

    def setFontUnderlineCustom(self, underline: bool):
        if not self.applyToAllIfNoSelection(lambda: self.setFontUnderline(underline)):
            self.setFontUnderline(underline)

    def setCurrentFontCustom(self, font: QFont):
        if not self.applyToAllIfNoSelection(lambda: self.setCurrentFontCustom(font)):
            self.setCurrentFont(font)

    def setFontPointSizeCustom(self, size):
        if not self.applyToAllIfNoSelection(lambda: self.setFontPointSize(size)):
            self.setFontPointSize(size)

    def setTextColorCustom(self, color):
        print(color)
        if not self.applyToAllIfNoSelection(lambda: self.setTextColor(color)):
            self.setTextColor(color)

    def setBackgroundColor(self, color: QColor):
        rgb = color.getRgb()
        self.setStyleSheet(f'background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]});')

    # If no text is selected, apply to all, else apply to selection
    def applyToAllIfNoSelection(self, func):
        if len(self.textCursor().selectedText()) != 0:
            return False

        # Select all text
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)

        # Run function
        func()

        # Unselect all text
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)
        return True

    def attributeChangedSlot(attribute, value):
        if attribute == editorSignalsInstance.ChangedWidgetAttribute.FontBold:
            print("Font Bold Signal")
    def slot_action2(self):
        print("Action 2 Triggered")
        font = QFont()
        font.setItalic(True)
        self.setFont(font)

    def changeFontSizeEvent(self, weight):
        print("changeFontSizeEvent Called")
        self.setFontWeightCustom(weight)
    
    #for communicating the signal editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontItalic, None)
    #current issue for Event Functions: Only affects highlighted


    def changeFontItalicEvent(self):

        cursor = self.textCursor()
        current_format = cursor.charFormat()
        
        #Checks if currently selected text is italics
        is_italic = current_format.fontItalic()
        
        #toggles the italics 
        current_format.setFontItalic(not is_italic)

        #Apply modified format to selected text
        cursor.setCharFormat(current_format)

        #Update text cursor with modified format
        self.setTextCursor(cursor)

    def changeFontBoldEvent(self):
        cursor = self.textCursor()
        current_format = cursor.charFormat()
        
        #Checks if currently selected text is bold
        is_bold = current_format.fontWeight() == 700
        
        #toggles the italics 
        if is_bold:
            current_format.setFontWeight(500)
        else:
            current_format.setFontWeight(700)
        #Apply modified format to selected text
        cursor.setCharFormat(current_format)

        #Update text cursor with modified format
        self.setTextCursor(cursor)

    def changeFontUnderlineEvent(self):
        cursor = self.textCursor()
        current_format = cursor.charFormat()
        
        #Checks if currently selected text is bold
        is_underlined = current_format.fontUnderline()

        #toggles the underline
        current_format.setFontUnderline(not is_underlined)

        #Apply modified format to selected text
        cursor.setCharFormat(current_format)

        #Update text cursor with modified format
        self.setTextCursor(cursor)

    def changeFontSizeEvent(self, value):
        #todo: when textbox is in focus, font size on toolbar should match the font size of the text
        cursor = self.textCursor()
        current_format = cursor.charFormat()

        current_format.setFontPointSize(value)
        cursor.setCharFormat(current_format)

        self.setTextCursor(cursor)

    def changeFontEvent(self, font_style):
        cursor = self.textCursor()
        current_format = cursor.charFormat()
        current_format.setFont(font_style)

        cursor.setCharFormat(current_format)

        
        self.setTextCursor(cursor)

    # Changes font text color 
    def changeFontColorEvent(self, new_font_color):

        cursor = self.textCursor()
        current_format = cursor.charFormat()

        color = QColor(new_font_color)
        current_format.setForeground(color)

        cursor.setCharFormat(current_format)
        
        #to not get stuck on highlighted text
        self.deselectText()
        #self.setTextCursor(cursor)

    # Changes color of whole background
    def changeBackgroundColorEvent(self, color: QColor):
        #if self.hasFocus():
        rgb = color.getRgb()
        self.setStyleSheet(f'background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]});')
        self.deselectText()
    
    # Changes textbox background color
    def changeTextboxColorEvent(self, new_bg_color):
        cursor = self.textCursor()
        current_format = cursor.charFormat()

        color = QColor(new_bg_color)
        current_format.setBackground(color)

        cursor.setCharFormat(current_format)
        self.deselectText()

            #self.setTextCursor(cursor)

    # Used to remove text highlighting
    def deselectText(self):
        
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)
    
    # Adds bullet list to text
    def changeBulletEvent(self):
        #put bullet function here  
        print("bullet press")