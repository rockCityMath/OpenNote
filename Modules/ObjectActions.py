from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import random
import cv2

from Models.DraggableContainer import DraggableContainer
from Widgets.Textbox import TextboxWidget, TextboxPickleable
from Widgets.Image import ImageWidget, ImagePickleable
from Widgets.Table import TableWidget, TablePickleable
from Modules.Enums import TextBoxStyles, WidgetType

class CreateTableDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.rowsLineEdit = QLineEdit()
        self.colsLineEdit = QLineEdit()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Rows:"))
        layout.addWidget(self.rowsLineEdit)
        layout.addWidget(QLabel("Columns:"))
        layout.addWidget(self.colsLineEdit)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def getTableSize(self):
        rows = int(self.rowsLineEdit.text())
        cols = int(self.colsLineEdit.text())
        return rows, cols

# When a user creates a new Object (TextBox, ImageObj, etc.)
# 1 Create a Widget of (type)
# 2 Create an Object of (type) and add it to models.Notebook.Page[x].Section[x]
# 3 Add Widget to editor.object list (List of widgets in Page[current], Section[current])
def add_object(editor, event, type):
    x = event.pos().x() + 250
    y = event.pos().y() + 130

    # Name for undo
    random_number = random.randint(100, 999)
    undo_name = 'textbox-'+str(random_number)

    if type == WidgetType.TEXT:

        default_height = 35
        default_width = 10

        # Create textbox and add to notebook
        text = TextboxWidget(editor, x, y, default_width, default_height, '')
        text.setObjectName(undo_name)
        editor.notebook.page[editor.page].section[editor.section].object.append(TextboxPickleable(undo_name, x, y, default_width, default_height, ''))
        drag = DraggableContainer(editor, QPoint(x, y), text)

        editor.object.append(drag)

        # Undo related
        cmd = {'type':'object','name':undo_name, 'action':'create'}
        editor.undo_stack.append(cmd)

    if type == WidgetType.IMAGE:

        # Get path from user
        path, _ = QFileDialog.getOpenFileName(editor, 'Add Image')
        if path == "": return

        # Get image size
        image_matrix = cv2.imread(path)
        h, w, _ = image_matrix.shape

        # Create image and add to notebook
        h, w, _ = image_matrix.shape
        image = ImageWidget(editor, x, y, w, h, image_matrix)

        editor.notebook.page[editor.page].section[editor.section].object.append(ImagePickleable(undo_name, x, y, w, h, image_matrix))
        drag = DraggableContainer(editor, QPoint(x, y), image)
        editor.object.append(drag)
        editor.autosaver.onChangeMade()

    if type == WidgetType.TABLE:
        default_height = 200
        default_width = 200
        dialog = CreateTableDialog()
        if dialog.exec_() == QDialog.Accepted:
            rows, cols = dialog.getTableSize()
            table = TableWidget(editor, x,y,default_width,default_height,rows,cols)
            table.setObjectName(undo_name)
            editor.notebook.page[editor.page].section[editor.section].object.append(TablePickleable(undo_name, x,y,default_width,default_height,rows,cols))
            drag = DraggableContainer(editor, QPoint(x, y), table)
            editor.object.append(drag)

            # Undo related
            cmd = {'type':'object','name':undo_name, 'action':'create'}
            editor.undo_stack.append(cmd)

        editor.autosaver.onChangeMade()

def add_snip(editor, event_pos, image_matrix):
    x = event_pos['x'] + 250
    y = event_pos['y'] + 130

    # Name for undo
    random_number = random.randint(100, 999)
    undo_name = 'imagebox-'+str(random_number)

    # Create image and add to notebook
    h, w, _ = image_matrix.shape
    image = ImageWidget(editor, x, y, w, h, image_matrix)

    editor.notebook.page[editor.page].section[editor.section].object.append(ImagePickleable(undo_name, x, y, w, h, image_matrix))
    drag = DraggableContainer(editor, QPoint(x, y), image)
    editor.object.append(drag)
    editor.autosaver.onChangeMade()

def paste_object(editor, event):
    if hasattr(editor, 'clipboard_object'): # debt: Should be init to None on editor init
        x = event.pos().x() + 250
        y = event.pos().y() + 130
        w = editor.clipboard_object.width
        h = editor.clipboard_object.height
        rows  = editor.clipboard_object.row
        cols = editor.clipboard_object.col
        data = editor.clipboard_object.data # debt: Not immediately clear what's gonna be in here
        undo_name = editor.clipboard_object.undo_name

        if editor.clipboard_object.type == WidgetType.IMAGE:
            image = ImageWidget(editor, x, y, w, h, data)
            editor.notebook.page[editor.page].section[editor.section].object.append(ImagePickleable(undo_name, x, y, w, h, data))
            drag = DraggableContainer(editor, QPoint(x, y), image)
            editor.object.append(drag)
            editor.autosaver.onChangeMade()

        elif editor.clipboard_object.type == WidgetType.TEXT:
            text = TextboxWidget(editor, x, y, w, h, data)
            text.setStyleSheet(TextBoxStyles.INFOCUS.value)
            text.setObjectName(undo_name)
            editor.notebook.page[editor.page].section[editor.section].object.append(TextboxPickleable(undo_name, x, y, w, h, data))
            drag = DraggableContainer(editor, QPoint(x, y), text)
            editor.object.append(drag)

        else:
            table = TableWidget(editor, x,y,w,h,rows,cols,data)
            for i in range(rows):
                for j in range(cols):
                    table.setItem(i,j,QTableWidgetItem(data[i][j]))
            
            table.setObjectName(undo_name)
            editor.notebook.page[editor.page].section[editor.section].object.append(TablePickleable(undo_name, x,y,w,h,rows,cols,data))
            drag = DraggableContainer(editor, QPoint(x, y), table)
            editor.object.append(drag)

        # Undo related
        cmd = {'type':'object','name':undo_name, 'action':'create'}
        editor.undo_stack.append(cmd)
        editor.autosaver.onChangeMade()

    else:
        print("No object on clipboard...")

# Create Widget of (type) with (params) from models.Notebook.Page[x].Section[x]
# Case 1: When a Notebook is loaded, function is called for every
#         Object in models.Notebook.Page[0].Section[0]
# Case 2: When a user selects a new Page or Section in the editor
def build_object(editor, params):
    if params.type == WidgetType.TEXT:
        text = TextboxWidget(editor, params.x, params.y, params.w, params.h, params.text)
        drag = DraggableContainer(editor, QPoint(params.x, params.y), text)
        editor.object.append(drag)

    if params.type == WidgetType.TABLE:
        table = TableWidget(editor, params.x, params.y, params.w, params.h,params.rows,params.cols, params.t)
        for i in range(len(params.t)):
            for j in range(len(params.t[0])):
                table.setItem(i,j,QTableWidgetItem(params.t[i][j]))
            
        drag = DraggableContainer(editor, QPoint(params.x, params.y), table)
        editor.object.append(drag)

    if params.type == WidgetType.IMAGE:
        image = ImageWidget(editor, params.x, params.y, params.w, params.h, params.image_matrix)
        drag = DraggableContainer(editor, QPoint(params.x, params.y), image)
        editor.object.append(drag)

    if params.type == 'plugin':
        params.show()
        editor.object.append(params)

def add_plugin_object(editor, event, name, c):

    # Defaults for object
    x = event.pos().x() + 250
    y = event.pos().y() + 130
    w = 100
    h = 100

    inst = c(editor,x,y,w,h)
    editor.notebook.page[editor.page].section[editor.section].object.append(inst)
    editor.object.append(inst)
