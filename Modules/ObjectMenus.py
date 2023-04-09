from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from Models.Clipboard import Clipboard
from Modules.ObjectActions import *
from Modules.Enums import WidgetType

def table_object_menu(editor):
    object_menu = QMenu(editor)

    delete = QAction("Delete", editor)
    delete.triggered.connect(lambda: delete_object(editor))
    object_menu.addAction(delete)

    copy = QAction("Copy", editor)
    copy.triggered.connect(lambda: copy_object(editor))
    object_menu.addAction(copy)

    cut = QAction("Cut", editor)
    cut.triggered.connect(lambda: cut_object(editor))
    object_menu.addAction(cut)

    add_row = QAction("Add Row", editor)
    add_row.triggered.connect(lambda: add_r(editor))
    object_menu.addAction(add_row)

    add_col = QAction("Add Col", editor)
    add_col.triggered.connect(lambda: add_c(editor))
    object_menu.addAction(add_col)

    del_row = QAction("Del Row", editor)
    del_row.triggered.connect(lambda: del_r(editor))
    object_menu.addAction(del_row)

    del_col = QAction("Del Col", editor)
    del_col.triggered.connect(lambda: del_c(editor))
    object_menu.addAction(del_col)

    return object_menu

# Returns the menu to be put on the DraggableObject
def get_object_menu(editor):
    object_menu = QMenu(editor)

    delete = QAction("Delete", editor)
    delete.triggered.connect(lambda: delete_object(editor))
    object_menu.addAction(delete)

    copy = QAction("Copy", editor)
    copy.triggered.connect(lambda: copy_object(editor))
    object_menu.addAction(copy)

    cut = QAction("Cut", editor)
    cut.triggered.connect(lambda: cut_object(editor))
    object_menu.addAction(cut)

    return object_menu

def delete_object(editor):
    try:
        for o in range(len(editor.object)):
            if (editor.object[o] == editor.focusWidget()):

                editor.undo_stack.append(
                    {'type':'object',
                     'name':editor.notebook.page[editor.page].section[editor.section].object[o].name,
                     'action':'delete'
                     })

                # Remove Widget from editor
                editor.object[o].deleteLater()
                editor.object.pop(o)

                item = editor.notebook.page[editor.page].section[editor.section].object.pop(o)
                editor.undo_stack[-1]['data']=item
                editor.autosaver.onChangeMade()
                return
    except:
        return # Sometimes this logs an err to console that doesnt seem like it matters

# Store the object that was clicked on in the editor's clipboard
def copy_object(editor):
    for o in range(len(editor.object)):
        if (editor.object[o] == editor.focusWidget()):
            ob = editor.object[o]
            undo_name = ob.objectName()+'(1)' # debt: I feel like this will/does cause problems
            if ob.child_object_type == WidgetType.IMAGE:
                editor.clipboard_object = Clipboard(ob.childWidget.frameGeometry().width(), ob.childWidget.frameGeometry().height(), ob.childWidget.image_matrix , ob.child_object_type, undo_name)
            elif ob.child_object_type == WidgetType.TEXT:
                editor.clipboard_object = Clipboard(ob.childWidget.frameGeometry().width(), ob.childWidget.frameGeometry().height(), ob.childWidget.toHtml(), ob.child_object_type, undo_name)
            else:
                data = {'rows':ob.childWidget.rows, 'cols':ob.childWidget.cols, 'data': ob.childWidget.t}
                editor.clipboard_object = Clipboard(ob.childWidget.frameGeometry().width(), ob.childWidget.frameGeometry().height(), data, ob.child_object_type, undo_name)

def add_r(editor):
    pass
def add_c(editor):
    pass
def del_r(editor):
    pass
def del_c(editor):
    pass

def cut_object(editor):
    copy_object(editor)
    delete_object(editor)
