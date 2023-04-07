from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class ImageItem(QTextEdit):
    DisplayName = "Image"
    def __init__(self, editor, x, y, w, h, path=None):
        super().__init__(editor)
        if path==None:
            path, _ = QFileDialog.getOpenFileName(
                editor, 
                'Add Image',
            )

        self.setGeometry(x, y, w, h)
        self.path = path
        fragment = QTextDocumentFragment.fromHtml(f"<img src={path} height='%1' width='%2'>")
        self.textCursor().insertFragment(fragment)
        self.mouseDoubleClickEvent = lambda event: drag(editor, event)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda event: object_menu(editor, event))
        self.type="plugin"
        self.show()
    
    def __getstate__(self):
        data = {}
        data['pos'] = self.geometry()
        data['path'] = self.path

        return data

    def __setstate__(self,data):
        self.type='plugin'
        self.__data=data
      
    def restoreWidget(self,editor): #mega hack to deal with qt
        x,y,w,h = self.__data['pos'].getRect()
        self.__init__(editor,x,y,w,h,path=self.__data['path'])


    def deleteLater(self): #ultra hack
        self.hide()

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

            # Remove Widget from editor
            editor.object[o].deleteLater()
            editor.object.pop(o)

            #Remove object from model
            editor.notebook.page[editor.page].section[editor.section].object.pop(o)
            return
