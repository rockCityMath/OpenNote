from models.notebook import *
from models.object import *
from PySide6.QtWidgets import *
import random
import cv2
import os
from datetime import datetime

#needed to create a dialogue for user to write number of cols and rows for a user
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

    if type == 'text':
        #default_text = '...'
        default_height = 35
        default_width = 10

        # Create textbox and add to notebook
        text = TextBox(editor, x, y, default_width, default_height, '')
        text.setObjectName(undo_name)
        editor.notebook.page[editor.page].section[editor.section].object.append(Text(undo_name, x, y, default_width, default_height, ''))
        drag = DraggableObject(editor, editor, QPoint(x, y), text)

        editor.object.append(drag)
        
        # Undo related

        cmd = {'type':'object','name':undo_name, 'action':'create'}
        editor.undo_stack.append(cmd)
    if type == 'image':

        # Get path from user
        path, _ = QFileDialog.getOpenFileName(editor, 'Add Image')
        if path == "": return

        # Get image size
        image_blob = cv2.imread(path)
        h, w, _ = image_blob.shape

        # Create image and add to notebook
        image = ImageObj(editor, x, y, w, h, path)

        editor.notebook.page[editor.page].section[editor.section].object.append(Image(undo_name, x, y, w, h, path))
        drag = DraggableObject(editor,editor, QPoint(x, y), image)
        editor.object.append(drag)

        # Undo related
        image.setObjectName(undo_name)
        cmd = {'type':'object','name':undo_name, 'action':'create'}
        editor.undo_stack.append(cmd)
    if type == 'table':
        default_height = 200
        default_width = 200
        dialog = CreateTableDialog()
        if dialog.exec_() == QDialog.Accepted:
            rows, cols = dialog.getTableSize()
            table = TableObject(editor, x,y,default_width,default_height,rows,cols)
            table.setObjectName(undo_name)
            editor.notebook.page[editor.page].section[editor.section].object.append(Table(undo_name, x,y,default_width,default_height,rows,cols))
            drag = DraggableObject(editor, editor, QPoint(x, y), table)

            editor.object.append(drag)
            # Undo related
            cmd = {'type':'object','name':undo_name, 'action':'create'}
            editor.undo_stack.append(cmd)      

            
        editor.autosaver.onChangeMade()

def add_snip(editor, event_pos, image_blob):
    x = event_pos['x'] + 250
    y = event_pos['y'] + 130

    # Name for undo
    random_number = random.randint(100, 999)
    undo_name = 'imagebox-'+str(random_number)

    # Use datetime to generate ss image filename, save to local directory
    currentDatetime = datetime.now()
    fileName = currentDatetime.strftime("%d-%m-%Y_%H-%M-%S") + ".png"
    if (not os.path.exists(os.getcwd() + "/screenshots")):
        os.makedirs(os.getcwd() + "/screenshots")

    path = os.getcwd() + "/screenshots/" + fileName
    cv2.imwrite(path, image_blob)

    # Create image and add to notebook
    h, w, _ = image_blob.shape
    image = ImageObj(editor, x, y, w, h, path)
    image.setStyleSheet(TextBoxStyles.INFOCUS.value)
    editor.notebook.page[editor.page].section[editor.section].object.append(Image(undo_name, x, y, w, h, path))
    drag = DraggableObject(editor,editor, QPoint(x, y), image)
    editor.object.append(drag)
    editor.autosaver.onChangeMade()

def paste_object(editor, event):
    if isinstance(editor.clipboard_object, ClipboardObject):
        x = event.pos().x() + 250
        y = event.pos().y() + 130
        w = editor.clipboard_object.width
        h = editor.clipboard_object.height
        t = editor.clipboard_object.html
        n = editor.clipboard_object.undo_name
        cols = editor.clipboard_object.cols
        rows = editor.clipboard_object.rows
        if editor.clipboard_object.type == 'image':
            image = ImageObj(editor, x, y, w, h, t)
            image.setStyleSheet(TextBoxStyles.INFOCUS.value)
            image.setObjectName(n)
            editor.notebook.page[editor.page].section[editor.section].object.append(Image(n, x, y, w, h, t))
            drag = DraggableObject(editor,editor, QPoint(x, y), image)
            editor.object.append(drag)


        elif editor.clipboard_object.type == 'text':
            text = TextBox(editor, x, y, w, h, t)
            text.setStyleSheet(TextBoxStyles.INFOCUS.value)
            text.setObjectName(n)
            editor.notebook.page[editor.page].section[editor.section].object.append(Text(n, x, y, w, h, t))
            drag = DraggableObject(editor,editor, QPoint(x, y), text)
            editor.object.append(drag)

        else:
            table = TableObject(editor, x,y,w,h,rows,cols)
            table.setObjectName(n)
            editor.notebook.page[editor.page].section[editor.section].object.append(Table(n, x,y,w,h,rows,cols))
            drag = DraggableObject(editor, editor, QPoint(x, y), table)
            editor.object.append(drag)
            text.setObjectName(n)

        # Undo related
        cmd = {'type':'object','name':n, 'action':'create'}
        editor.undo_stack.append(cmd)
        editor.autosaver.onChangeMade()

    elif editor.clipboard_object == None:
        return
    else: # Because anything thats not a QTextEdit prob wont work like this
        print("ERROR: Pasting unsupported object.")

# Create Widget of (type) with (params) from models.Notebook.Page[x].Section[x]
# Case 1: When a Notebook is loaded, function is called for every
#         Object in models.Notebook.Page[0].Section[0]
# Case 2: When a user selects a new Page or Section in the editor
def build_object(editor, params):
    if params.type == 'text':
        text = TextBox(editor, params.x, params.y, params.w, params.h, params.text)
        drag = DraggableObject(editor,editor, QPoint(params.x, params.y), text)
        editor.object.append(drag)

    if params.type == "image":
        image = ImageObj(editor, params.x, params.y, params.w, params.h, params.path)
        drag = DraggableObject(editor,editor, QPoint(params.x, params.y), image)
        editor.object.append(drag)
    if params.type == 'table':
        table = TableObject(editor, params.x, params.y, params.w, params.h,params.rows,params.cols)
        drag = DraggableObject(editor, editor, QPoint(params.x, params.y), table)
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