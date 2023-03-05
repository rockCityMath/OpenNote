# Draggable objects that can be used in the editor

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class TextBox(QTextEdit):
    def __init__(textbox, editor, x, y, w, h, text):
        super().__init__(editor)

        textbox.setStyleSheet("border: 1px dashed #000;")
        textbox.setGeometry(x, y, w, h)
        textbox.setText(text)
        textbox.isMoving = False
        textbox.mouseReleaseEvent = editor.select
        textbox.show()
        
    def mouseMoveEvent(self, event): 
        
        #TODO: Reimpliment selecting text by highlighting

        if (event.buttons() == Qt.RightButton):
            drag = QDrag(self)
            mimeData = QMimeData()
            drag.setMimeData(mimeData)
            drag.exec(Qt.MoveAction)   

class ImageObj(QTextEdit):
    def __init__(image, editor, x, y, w, h, path):
        super().__init__(editor)

        image.setGeometry(x, y, w, h)
        fragment = QTextDocumentFragment.fromHtml(f"<img src={path} height='%1' width='%2'>")
        image.textCursor().insertFragment(fragment)
        image.show()

    def mouseMoveEvent(self, event): 
        if (event.buttons() == Qt.RightButton):
            drag = QDrag(self)
            mimeData = QMimeData()
            drag.setMimeData(mimeData)
            drag.exec(Qt.MoveAction)   


    
