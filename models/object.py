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
        #textbox.mouseDoubleClickEvent = lambda x: object_menu(editor, x)
        textbox.mouseDoubleClickEvent = lambda x: dragEvent(editor, x)
        textbox.setContextMenuPolicy(Qt.CustomContextMenu)
        textbox.show()

class ImageObj(QTextEdit):
    def __init__(image, editor, x, y, w, h, path):
        super().__init__(editor)

        image.setGeometry(x, y, w, h)
        fragment = QTextDocumentFragment.fromHtml(f"<img src={path} height='%1' width='%2'>")
        image.textCursor().insertFragment(fragment)
        image.mousePressEvent = lambda x: object_menu(editor, x)
        image.mouseDoubleClickEvent = lambda x: dragEvent(editor, x)
        image.show()

def dragEvent(self, event): 

    if (event.buttons() == Qt.LeftButton):
        drag = QDrag(self)
        mimeData = QMimeData()
        drag.setMimeData(mimeData)
        drag.exec(Qt.MoveAction)   

def object_menu(editor, event):
    if event.buttons() == Qt.LeftButton:
        editor.selected = editor.focusWidget()
    if event.buttons() == Qt.RightButton:
        object_menu = QMenu(editor)

        delete = QAction("Delete", editor)
        delete.triggered.connect(lambda: delete_object(editor))
        object_menu.addAction(delete)

        object_menu.exec(event.globalPos())

def delete_object(editor):
    print("delete")