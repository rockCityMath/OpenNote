# Draggable objects that can be used in the editor

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# Holds clipboard object info, QT things can't be copied by value :(
class ClipboardObject:
    def __init__(self, width, height, html):
        self.width = width
        self.height = height
        
        self.html = html

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

def object_menu(editor, event):
    object_menu = QMenu(editor)

    # Delete
    delete = QAction("Delete", editor)
    delete.triggered.connect(lambda: delete_object(editor))
    object_menu.addAction(delete)

    # Copy
    copy = QAction("Copy", editor)
    copy.triggered.connect(lambda: copy_object(editor))
    object_menu.addAction(copy)

    # Cut
    cut = QAction("Cut", editor)
    cut.triggered.connect(lambda: cut_object(editor))
    object_menu.addAction(cut)

    object_menu.exec(editor.focusWidget().viewport().mapToGlobal(event))

def delete_object(editor):
    try:
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
                editor.autosaver.onChangeMade()
                return
    except:
        return # Sometimes this logs an err to console that doesnt seem like it matters

def copy_object(editor):
    for o in range(len(editor.object)):
        if (editor.object[o] == editor.focusWidget()):

            # Store the object that was clicked on in the editor's clipboard 
            ob = editor.object[o]
            editor.clipboard_object = ClipboardObject(ob.frameGeometry().width(), ob.frameGeometry().height(), ob.toHtml())

def cut_object(editor):
    copy_object(editor)
    delete_object(editor)

