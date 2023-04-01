from models.notebook import *
from models.object import *
# from modules.undo import *
from PySide6.QtWidgets import *
import random


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
        random_number = random.randint(100, 999)
        name = 'textbox-'+str(random_number)
        text.setObjectName(name)
        editor.notebook.page[editor.page].section[editor.section].object.append(Text(name,x, y, w, h, t))
        editor.object.append(text)  
        cmd = {'type':'object','name':name, 'action':'create'}
        editor.undo_stack.append(cmd)
    if type == 'image':
        path, _ = QFileDialog.getOpenFileName(
            editor,
            'Add Image',
        )
        random_number = random.randint(100, 999)
        name = 'imagebox-'+str(random_number)
        text.setObjectName(name)
        if path == "":
            return
        image = ImageObj(editor, x, y, w+100, h+100, path)
        editor.notebook.page[editor.page].section[editor.section].object.append(Image(name,x, y, w, h, t))
        editor.object.append(image)
        cmd = {'type':'object','name':name, 'action':'create'}
        editor.undo_stack.append(cmd)
    editor.autosaver.onChangeMade()

def add_snip(editor, event_pos, path):

    # Defaults for object
    x = event_pos['x'] + 250
    y = event_pos['y'] + 130
    w = 100
    h = 100
    t = "..."

    image = ImageObj(editor, x, y, w+100, h+100, path)
    editor.notebook.page[editor.page].section[editor.section].object.append(Text(x, y, w, h, t))
    editor.object.append(image)
    cmd = Undo({'type':'image', 'action':'create'})
    editor.undo_stack.append(cmd)

    editor.autosaver.onChangeMade()

def paste_object(editor, event):
    if isinstance(editor.clipboard_object, ClipboardObject):
        x = event.pos().x() + 250
        y = event.pos().y() + 130
        w = editor.clipboard_object.width
        h = editor.clipboard_object.height
        t = editor.clipboard_object.html

        text = TextBox(editor, x, y, w, h, t)
        editor.object.append(text)
        editor.notebook.page[editor.page].section[editor.section].object.append(Text(x, y, w, h, t))

        cmd = Undo({'type':'clipboard', 'action':'paste'})
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
        editor.object.append(text)

    if params.type == "image":
        image = ImageObj(editor, params.x, params.y, params.w, params.h, params.path)
        editor.object.append(image)

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

