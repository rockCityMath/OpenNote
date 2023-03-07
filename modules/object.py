from models.notebook import *
from models.object import *

from PySide6.QtWidgets import *

# When a user creates a new Object (TextBox, ImageObj, etc.)
# 1 Create a Widget of (type)
# 2 Create an Object of (type) and add it to models.Notebook.Page[x].Section[x]
# 3 Add Widget to editor.object list (List of widgets in Page[current], Section[current])
def add_object(editor, event, type):

    # Defaults for object
    x = event.pos().x() + 250
    y = event.pos().y() + 130
    w = 100
    h = 100
    t = '...'

    if type == 'text':
        text = TextBox(editor, x, y, w, h, t)
        editor.notebook.page[editor.page].section[editor.section].object.append(Text(x, y, w, h, t))
        editor.object.append(text)  

    if type == 'image':
        path, _ = QFileDialog.getOpenFileName(
            editor, 
            'Add Image',
        )
        image = ImageObj(editor, x, y, w+100, h+100, path)
        editor.notebook.page[editor.page].section[editor.section].object.append(Text(x, y, w, h, t))
        editor.object.append(image)

    editor.autosaver.onChangeMade()

# Create Widget of (type) with (params) from models.Notebook.Page[x].Section[x]
# Case 1: When a Notebook is loaded, function is called for every 
#         Object in models.Notebook.Page[0].Section[0]
# Case 2: When a user selects a new Page or Section in the editor
def build_object(editor, params):
    if params.type == 'text':
        text = TextBox(editor, params.x, params.y, params.w, params.h, params.text)
        editor.object.append(text)

    if params.type == "image":
        image = ImageObj(editor, params.x, params.y, params.w, params.h, params.path)
        editor.object.append(image)