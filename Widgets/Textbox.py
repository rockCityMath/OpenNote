from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from Modules.Enums import TextBoxStyles
FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

class TextboxWidget(QTextEdit):
    def __init__(self, x, y, w = 100, h = 100, t = 'new text!'):
        super().__init__()

        self.setGeometry(x, y, w, h)                       # This sets geometry of DraggableObject
        self.setText(t)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.persistGeometry = self.geometry()
        # self.setBackgroundColor(QColor.Red)

    def changeBackgroundColorEvent(self, color: QColor):
        print("NEW COLOR: ", color)
        # self.setStyleSheet()
        print(color.getRgb())
        rgb = color.getRgb()
        self.setStyleSheet(f'background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]});')

    def changeFontColorEvent(self, color: QColor):
        print("NEW COLOR: ", color)
        self.setTextColor(color)

    def changeFontEvent(self, font: QFont):
        print("NEW FONT: ", font)
        self.setCurrentFont(font)

    def changeFontSizeEvent(self, size: int):
        print("CHANGEFONT: " + str(size))
        self.setFontPointSize(size)

    def changeFontBoldEvent(self):
        self.setFontWeight(QFont.Bold)

    def changeFontItalicEvent(self):
        self.setFontItalic(True)

    def changeFontUnderlineEvent(self):
        self.setFontUnderline(True)

    @staticmethod
    def new(clickPos: QPoint):
        return TextboxWidget(clickPos.x(), clickPos.y())

    def newGeometryEvent(self, newGeometry: QRect):
        self.persistGeometry = newGeometry

    def __getstate__(self):
        data = {}

        # this is wierd, but dragcontainer position is seperate from this one, but we want that position
        # this widgets pos can be set in newGeometryEvent I think but it flickers too much
        data['geometry'] = self.persistGeometry
        data['content'] = self.toHtml()
        return data

    def __setstate__(self, data):
        self.__init__(data['geometry'].x(), data['geometry'].y(), data['geometry'].width(), data['geometry'].height(), data['content'])
        # print(type(self.__init__(data['geometry'].x(), data['geometry'].y(), data['geometry'].width(), data['geometry'].height(), data['content'])))

    def customMenuItems(self,menu):
      def build_action(parent, icon_path, action_name, set_status_tip, set_checkable):
          action = QAction(QIcon(icon_path), action_name, parent)
          action.setStatusTip(set_status_tip)
          action.setCheckable(set_checkable)
          return action

      toolbar = QToolBar()
      toolbar.setIconSize(QSize(25, 25))
      toolbar.setMovable(False)

      font = QFontComboBox()
      font.currentFontChanged.connect(lambda x: self.setCurrentFont(font.currentFont() if x else self.currentFont()))

      size = QComboBox()
      size.addItems([str(fs) for fs in FONT_SIZES])
      size.currentIndexChanged.connect(lambda x: self.setFontPointSize(float(x + 10) if x else self.fontPointSize()))

      bold = build_action(toolbar, 'assets/icons/svg_font_bold', "Bold", "Bold", True)
      bold.toggled.connect(lambda x: self.setFontWeight(700 if x else 500))

      italic = build_action(toolbar, 'assets/icons/svg_font_italic', "Italic", "Italic", True)
      italic.toggled.connect(lambda x: self.setFontItalic(True if x else False))

      underline = build_action(toolbar, 'assets/icons/svg_font_underline', "Underline", "Underline", True)
      underline.toggled.connect(lambda x: self.setFontUnderline(True if x else False))

      toolbar.addWidget(font)
      toolbar.addWidget(size)
      toolbar.addActions([bold, italic, underline])
      qwa = QWidgetAction(menu)
      qwa.setDefaultWidget(toolbar)

      return [qwa]
