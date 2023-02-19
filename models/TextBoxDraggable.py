from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from pprint import pprint

class TextBoxDraggable(QTextEdit):
    def __init__(self, parent, x, y, imagePath):
        super().__init__(parent)
        self.setStyleSheet("border: 1px dashed #000;")

        #if text
        if imagePath == None:
            self.setGeometry(x, y, 260, 45)
            self.isMoving = False

        #if image
        else:
            self.setGeometry(x, y, 260, 45)
            fragment = QTextDocumentFragment.fromHtml(f"<img src={imagePath} height='%1' width='%2'>")
            self.textCursor().insertFragment(fragment)
            self.resize(300, 300)
        
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.isMoving = True
            mimeData = QMimeData()
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec_(Qt.MoveAction)

    # def __getstate__(self):
    #     del self.copyAvailable
    #     del self.currentCharFormatChanged
    #     del self.cursorPositionChanged
    #     del self.customContextMenuRequested
    #     del self.destroyed
    #     del self.isMoving
    #     del self.objectNameChanged
    #     del self.redoAvailable
    #     del self.selectionChanged
    #     del self.textChanged
    #     del self.undoAvailable
    #     del self.windowIconChanged
    #     del self.windowIconTextChanged
    #     del self.windowTitleChanged

    #     self.__dict__["x"] = self.x()
    #     self.__dict__["y"] = self.y()
    #     self.__dict__["parent"] = self.parent()
        
    #     pprint(self.__dict__)
    #     return self.__dict__
        
    # def __setstate__(self, dict):
    #     pprint(dict)
    #     self.__init__(self.__dict__.parent, self.__dict__.x, self.__dict__.y)
    #     self.__dict__.update(dict)