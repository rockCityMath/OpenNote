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
        textbox.mouseReleaseEvent = lambda pos: select(editor, pos)
        textbox.mouseDoubleClickEvent = lambda event: drag(editor, event)
        textbox.setContextMenuPolicy(Qt.CustomContextMenu)
        textbox.customContextMenuRequested.connect(lambda event: object_menu(editor, event))
        textbox.show()

class ImageObj(QTextEdit):
    def __init__(image, editor, x, y, w, h, path):
        super().__init__(editor)

        image.setGeometry(x, y, w, h)
        fragment = QTextDocumentFragment.fromHtml(f"<img src={path} height='%1' width='%2'>")
        image.textCursor().insertFragment(fragment)
        image.mouseDoubleClickEvent = lambda event: drag(editor, event)
        image.setContextMenuPolicy(Qt.CustomContextMenu)
        image.customContextMenuRequested.connect(lambda event: object_menu(editor, event))
        image.show()

# Select TextBox for font styling
def select(editor, event):
    editor.selected = editor.focusWidget()

def drag(editor, event): 
    if (event.buttons() == Qt.LeftButton):
        drag = QDrag(editor)
        mimeData = QMimeData()
        drag.setMimeData(mimeData)
        drag.exec(Qt.MoveAction)   

def object_menu(editor, pos):
    object_menu = QMenu(editor)

    delete = QAction("Delete", editor)
    delete.triggered.connect(lambda: delete_object(editor))
    object_menu.addAction(delete)

    object_menu.exec(editor.focusWidget().viewport().mapToGlobal(pos))

def delete_object(editor):

    for o in range(len(editor.object)):
        if (editor.object[o] == editor.focusWidget()):
            editor.undo_stack.append(
                {'type':'object',
                 'name':editor.object[o].objectName(), 
                 'action':'delete'
                 })
            # Remove Widget from editor
            editor.object[o].deleteLater()
            editor.object.pop(o)

            #Remove object from model
            item = editor.notebook.page[editor.page].section[editor.section].object.pop(o)
            editor.undo_stack[-1]['data']=item

            return

