from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from Modules.Enums import TextBoxStyles
FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

class TextboxWidget(QTextEdit):
    def __init__(self, x, y, w = 15, h = 30, t = ''):
        super().__init__()

        self.setGeometry(x, y, w, h)                       # This sets geometry of DraggableObject
        self.setText(t)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textChanged.connect(self.textChangedEvent)

    def textChangedEvent(self):
        if len(self.toPlainText()) < 2:
            print("RESIZE TEXT")
            self.resize(100, 100)

    def changeBackgroundColorEvent(self, color: QColor):
        print("NEW COLOR: ", color)
        # self.setStyleSheet()
        print(color.getRgb())
        rgb = color.getRgb()
        self.setStyleSheet(f'background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]});')

    def changeFontColorEvent(self, color: QColor):
        self.setTextColor(color)
        self.removeSelection()

    def changeFontEvent(self, font: QFont):
        self.setCurrentFont(font)
        self.removeSelection()

    def changeFontSizeEvent(self, size: int):
        self.setFontPointSize(size)
        self.removeSelction()

    def changeFontBoldEvent(self):
        self.setFontWeight(QFont.Bold)
        self.removeSelection()

    def changeFontItalicEvent(self):
        self.setFontItalic(True)
        self.removeSelection()

    def changeFontUnderlineEvent(self):
        self.setFontUnderline(True)
        self.removeSelection()

    def removeSelection(self):
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)

    @staticmethod
    def new(clickPos: QPoint):
        return TextboxWidget(clickPos.x(), clickPos.y())

    def __getstate__(self):
        data = {}

        data['geometry'] = self.parentWidget().geometry()
        data['content'] = self.toHtml()
        return data

    def __setstate__(self, data):
        self.__init__(data['geometry'].x(), data['geometry'].y(), data['geometry'].width(), data['geometry'].height(), data['content'])

    def checkEmpty(self):
        if len(self.toPlainText()) < 1:
            return True
        return False

    def customMenuItems(self,actions,menu):
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
      font.currentFontChanged.connect(lambda x: self.setCurrentFont(font.currentFont() if x else self.currentFont()))

      size = QComboBox()
      size.addItems([str(fs) for fs in FONT_SIZES])
      size.currentIndexChanged.connect(lambda x: self.setFontPointSize(float(x + 10) if x else self.fontPointSize()))

      bold = build_action(toolbarBottom, 'assets/icons/svg_font_bold', "Bold", "Bold", True)
      bold.toggled.connect(lambda x: self.setFontWeight(700 if x else 500))

      italic = build_action(toolbarBottom, 'assets/icons/svg_font_italic', "Italic", "Italic", True)
      italic.toggled.connect(lambda x: self.setFontItalic(True if x else False))

      underline = build_action(toolbarBottom, 'assets/icons/svg_font_underline', "Underline", "Underline", True)
      underline.toggled.connect(lambda x: self.setFontUnderline(True if x else False))

      toolbarTop.addWidget(font)
      toolbarTop.addWidget(size)
      toolbarBottom.addActions([bold, italic, underline])
      qwaTop = QWidgetAction(menu)
      qwaTop.setDefaultWidget(toolbarTop)
      qwaBottom = QWidgetAction(menu)
      qwaBottom.setDefaultWidget(toolbarBottom)

      actions.insert(0,qwaBottom)
      actions.insert(0,qwaTop)
