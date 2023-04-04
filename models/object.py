# Draggable objects that can be used in the editor
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from enum import Enum
import os

# Draggable object modes
class Mode(Enum):
    NONE = 0,
    MOVE = 1,
    RESIZETL = 2,
    RESIZET = 3,
    RESIZETR = 4,
    RESIZER = 5,
    RESIZEBR = 6,
    RESIZEB = 7,
    RESIZEBL = 8,
    RESIZEL = 9

# Styles for different states of the textbox
class TextBoxStyles(Enum):
    INFOCUS = "border: 0.5px dotted rgba(0, 0, 0, .5); background-color: rgba(0, 0, 0, 0)"
    OUTFOCUS = "border: none; background-color: rgba(0, 0, 0, 0);"

# Holds clipboard object info, QT things can't be copied by value :(
class ClipboardObject:
    def __init__(self, width, height, html, type, undo_name, cols=0, rows = 0):
        self.width = width
        self.height = height
        self.html = html
        self.undo_name = undo_name
        self.type = type
        self.rows = rows
        self.cols = cols

# Based off https://wiki.qt.io/Widget-moveable-and-resizeable <3
class DraggableObject(QWidget):
    menu = None
    mode = Mode.NONE
    position = None
    inFocus = Signal(bool)
    outFocus = Signal(bool)
    newGeometry = Signal(QRect)

    # Parent should be called editor, its always the editor
    def __init__(self, parent, editor, p, cWidget):
        super().__init__(parent=parent)
        # self.menu = get_object_menu(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setVisible(True)
        self.setAutoFillBackground(False)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setFocus()
        self.move(p)
        self.old_x = 0
        self.old_y = 0
        self.name = cWidget.objectName()
        self.editor = editor
        self.vLayout = QVBoxLayout(self)
        self.setChildWidget(cWidget)
        self.childWidget = cWidget # Probably better to findChildren()...
        self.m_infocus = True
        self.m_showMenu = False
        self.m_isEditing = True
        self.installEventFilter(parent)
        self.setGeometry(cWidget.geometry())
        self.old_state = {}

        if isinstance(cWidget, ImageObj):
            self.object_type = 'image'
            self.menu = get_object_menu(parent)

        elif isinstance(cWidget, ImageObject):
            self.object_type = 'image_object'
            self.menu = get_object_menu(parent)

        elif isinstance(cWidget, TextBox):
            self.object_type = 'text'
            self.menu = get_object_menu(parent)

        else: # debt: there should be a better else
            self.object_type = 'table' # these should probably be an enum everywhere
            self.menu = table_object_menu(parent)
            self.childWidget.setEditTriggers(QTableWidget.DoubleClicked) # Connect the itemDoubleClicked signal of the table widget to the mouseDoubleClickEvent slot

    def setChildWidget(self, cWidget):
        if cWidget:
            self.childWidget = cWidget
            self.childWidget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            self.childWidget.setParent(self)
            self.childWidget.releaseMouse()
            self.vLayout.addWidget(cWidget)
            self.vLayout.setContentsMargins(0,0,0,0)

    def popupShow(self, pt: QPoint):
        global_ = self.mapToGlobal(pt)
        self.m_showMenu = True
        self.menu.exec(global_)
        self.m_showMenu = False

    def focusInEvent(self, a0: QFocusEvent):

        if hasattr(self, 'childWidget'): # Widget not present on first focus
            if self.object_type == 'text':
                self.childWidget.setStyleSheet(TextBoxStyles.INFOCUS.value)

        self.m_infocus = True
        p = self.parentWidget()
        p.installEventFilter(self)
        p.repaint()
        self.inFocus.emit(True)

    def focusOutEvent(self, a0: QFocusEvent):
        self.childWidget.setAttribute(Qt.WA_TransparentForMouseEvents, True) # Events start going to parent when user focuses elsewhere

        self.setCursor(QCursor(Qt.ArrowCursor)) # This could be a open hand or other cursor also
        self.mode = Mode.MOVE # Not 100% sure this is correct

        if not self.m_isEditing:
            return
        if self.m_showMenu:
            return
        self.childWidget.setStyleSheet(TextBoxStyles.OUTFOCUS.value) # debt: Needs some kind of state manager or something
        self.outFocus.emit(False)
        self.m_infocus = False

    # Called on resize, was used to fill rectangle's background, leaving in case we want
    def paintEvent(self, e: QPaintEvent):
        return
#        painter = QPainter(self)
#        color = (r, g, b, a) = (255, 0, 0, 16)
#        painter.fillRect(e.rect(), QColor(r, g, b, a))
#
#        if self.m_infocus:
#            rect = e.rect()
#            rect.adjust(0,0,-1,-1)
#            painter.setPen(QColor(r, g, b))
#            painter.drawRect(rect)

    def mousePressEvent(self, e: QMouseEvent):
        self.position = QPoint(e.globalX() - self.geometry().x(), e.globalY() - self.geometry().y())

        # Undo related
        self.old_x = e.globalX()
        self.old_y = e.globalY()
        self.old_state = {'type':'object','action':'move','name':self.name,'x':self.old_x,'y':self.old_y}

        if not self.m_isEditing:
            return
        if not self.m_infocus:
            return
        if not e.buttons() and Qt.LeftButton:
            self.setCursorShape(e.pos())
            return
        if e.button() == Qt.RightButton:
            self.popupShow(e.pos())
            e.accept()

    # On double click, send events to child and move cursor to end
    def mouseDoubleClickEvent(self, e: QMouseEvent):
        if self.object_type == "text" and self.childWidget.toPlainText() == '': # debt: What does this do
            self.editor.setFocus()
        else:
            self.childWidget.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            self.childWidget.setFocus()

            # Tables need doubleclick, text needs single? Not sure if thats how it works though
            if self.object_type == "text":
                self.childWidget.mousePressEvent(e)
            elif self.object_type == "table":
                self.childWidget.mouseDoubleClickEvent(e)

            # Would be ideal if the user could click in the textbox to move the cursor, but the focus events are tricky...
            if self.object_type == 'text':
                self.childWidget.moveCursor(QTextCursor.End)
                self.childWidget.setStyleSheet(TextBoxStyles.INFOCUS.value)

    def keyPressEvent(self, e: QKeyEvent):
        if not self.m_isEditing: return
        return

    # Determine which cursor to show and which mode to be in when user is interacting with the box
    def setCursorShape(self, e_pos: QPoint):
        diff = 10 # Amount of padding from the edge where resize cursors will show

        # Not allowing resizable images for now
        if self.object_type == 'image' or self.object_type == 'image_object': # debt: remove "image" references
            self.setCursor(QCursor(Qt. ArrowCursor))
            self.mode = Mode.MOVE
            return

        # Dont set cursor shapes on empty textbox
        if self.object_type != "text" or self.childWidget.toPlainText() != '':
            # Left - Bottom
            if (((e_pos.y() > self.y() + self.height() - diff) and # Bottom
                (e_pos.x() < self.x() + diff)) or # Left
            # Right-Bottom
            ((e_pos.y() > self.y() + self.height() - diff) and # Bottom
            (e_pos.x() > self.x() + self.width() - diff)) or # Right
            # Left-Top
            ((e_pos.y() < self.y() + diff) and # Top
            (e_pos.x() < self.x() + diff)) or # Left
            # Right-Top
            (e_pos.y() < self.y() + diff) and # Top
            (e_pos.x() > self.x() + self.width() - diff)): # Right
                # Left - Bottom
                if ((e_pos.y() > self.y() + self.height() - diff) and # Bottom
                (e_pos.x() < self.x()
                    + diff)): # Left
                    self.mode = Mode.RESIZEBL
                    self.setCursor(QCursor(Qt.SizeBDiagCursor))
                    # Right - Bottom
                if ((e_pos.y() > self.y() + self.height() - diff) and # Bottom
                (e_pos.x() > self.x() + self.width() - diff)): # Right
                    self.mode = Mode.RESIZEBR
                    self.setCursor(QCursor(Qt.SizeFDiagCursor))
                # Left - Top
                if ((e_pos.y() < self.y() + diff) and # Top
                (e_pos.x() < self.x() + diff)): # Left
                    self.mode = Mode.RESIZETL
                    self.setCursor(QCursor(Qt.SizeFDiagCursor))
                # Right - Top
                if ((e_pos.y() < self.y() + diff) and # Top
                (e_pos.x() > self.x() + self.width() - diff)): # Right
                    self.mode = Mode.RESIZETR
                    self.setCursor(QCursor(Qt.SizeBDiagCursor))
            # check cursor horizontal position
            elif ((e_pos.x() < self.x() + diff) or # Left
                (e_pos.x() > self.x() + self.width() - diff)): # Right
                if e_pos.x() < self.x() + diff: # Left
                    self.setCursor(QCursor(Qt.SizeHorCursor))
                    self.mode = Mode.RESIZEL
                else: # Right
                    self.setCursor(QCursor(Qt.SizeHorCursor))
                    self.mode = Mode.RESIZER
            # check cursor vertical position
            elif ((e_pos.y() > self.y() + self.height() - diff) or # Bottom
                (e_pos.y() < self.y() + diff)): # Top
                if e_pos.y() < self.y() + diff: # Top
                    self.setCursor(QCursor(Qt.SizeVerCursor))
                    self.mode = Mode.RESIZET
                else: # Bottom
                    self.setCursor(QCursor(Qt.SizeVerCursor))
                    self.mode = Mode.RESIZEB
            else:
                self.setCursor(QCursor(Qt. ArrowCursor))
                self.mode = Mode.MOVE

    def mouseReleaseEvent(self, e: QMouseEvent):
        self.editor.undo_stack.append(self.old_state)
        self.parentWidget().autosaver.onChangeMade()
        QWidget.mouseReleaseEvent(self, e)

    def leaveEvent(self, e: QMouseEvent):
        QWidget.leaveEvent(self, e)

        # debt: Comparison after the "and" is an attempt to keep the border when the focus is on a tables qlineedit cell
        if self.parentWidget().focusWidget() != self.childWidget and (type(self.parentWidget().focusWidget()) != QLineEdit):
            self.childWidget.setStyleSheet(TextBoxStyles.OUTFOCUS.value)

    # Determine how to handle the mouse being moved inside the box
    def mouseMoveEvent(self, e: QMouseEvent):
        QWidget.mouseMoveEvent(self, e)

        # Show textbox and table border hover
        if self.object_type != 'image_object':
            self.childWidget.setStyleSheet(TextBoxStyles.INFOCUS.value)

        if not self.m_isEditing:
            return
        if not self.m_infocus:
            return
        if not e.buttons() and Qt.LeftButton:
            p = QPoint(e.x() + self.geometry().x(), e.y() + self.geometry().y())
            self.setCursorShape(p)
            return

        if (self.mode == Mode.MOVE or self.mode == Mode.NONE) and e.buttons() and Qt.LeftButton:
            toMove = e.globalPos() - self.position
            if toMove.x() < 0:return
            if toMove.y() < 0:return
            if toMove.x() > self.parentWidget().width() - self.width(): return

            # Dont move outside the editor frame
            if(toMove.x() < self.parentWidget().width() - self.parentWidget().frame.width()):
                return
            if(toMove.y() < self.parentWidget().height() - self.parentWidget().frame.height()):
                return
            if(toMove.y() > self.parentWidget().frame.height() + 20):
                return

            self.move(toMove)
            self.newGeometry.emit(self.geometry())
            self.childWidget.setStyleSheet(TextBoxStyles.INFOCUS.value)
            self.parentWidget().repaint()
            return
        if (self.mode != Mode.MOVE) and e.buttons() and Qt.LeftButton:

            # Not allowing resizable images for now
            if self.object_type == 'image' or self.object_type == 'image_object':
                return
            if self.mode == Mode.RESIZETL: # Left - Top
                newwidth = e.globalX() - self.position.x() - self.geometry().x()
                newheight = e.globalY() - self.position.y() - self.geometry().y()
                toMove = e.globalPos() - self.position
                self.resize(self.geometry().width() - newwidth, self.geometry().height() - newheight)
                self.move(toMove.x(), toMove.y())
            elif self.mode == Mode.RESIZETR: # Right - Top
                newheight = e.globalY() - self.position.y() - self.geometry().y()
                toMove = e.globalPos() - self.position
                self.resize(e.x(), self.geometry().height() - newheight)
                self.move(self.x(), toMove.y())
            elif self.mode== Mode.RESIZEBL: # Left - Bottom
                newwidth = e.globalX() - self.position.x() - self.geometry().x()
                toMove = e.globalPos() - self.position
                self.resize(self.geometry().width() - newwidth, e.y())
                self.move(toMove.x(), self.y())
            elif self.mode == Mode.RESIZEB: # Bottom
               self.resize(self.width(), e.y())
            elif self.mode == Mode.RESIZEL: # Left
                newwidth = e.globalX() - self.position.x() - self.geometry().x()
                toMove = e.globalPos() - self.position
                self.resize(self.geometry().width() - newwidth, self.height())
                self.move(toMove.x(), self.y())
            elif self.mode == Mode.RESIZET:# Top
               newheight = e.globalY() - self.position.y() - self.geometry().y()
               toMove = e.globalPos() - self.position
               self.resize(self.width(), self.geometry().height() - newheight)
               self.move(self.x(), toMove.y())
            elif self.mode == Mode.RESIZER: # Right
                self.resize(e.x(), self.height())
            elif self.mode == Mode.RESIZEBR:# Right - Bottom
                self.resize(e.x(), e.y())
            self.parentWidget().repaint()
        self.newGeometry.emit(self.geometry())

class TextBox(QTextEdit):
    def __init__(self, editor, x, y, w, h, t):
        super().__init__(editor)

        self.editor = editor
        self.type = 'text'
        self.setStyleSheet(TextBoxStyles.OUTFOCUS.value) # debt: this gets set everywhere
        self.setGeometry(x, y, w, h) # This sets geometry of DraggableObject
        self.setText(t)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.show()

    # Set the textbox as selected so that the editor can change font attributes
    def mousePressEvent(self, event):
        self.editor.selected = self
        QTextEdit.mousePressEvent(self, event)

    # When user starts typing in new box, expand its size
    def keyPressEvent(self, event):
        if len(self.toPlainText()) == 0:
            self.resize(100, 100)
            self.parentWidget().resize(100, 100)
            self.setStyleSheet(TextBoxStyles.INFOCUS.value)
        QTextEdit.keyPressEvent(self, event)

class TableObject(QTableWidget):
    def __init__(self, editor, x, y,w,h, rows, cols):
            super().__init__(rows, cols, editor)
            #self.setEditTriggers(QTableWidget.DoubleClicked) # debt: What is this
            self.rows=rows
            self.cols=cols
            self.editor = editor
            self.type = 'table'
            self.setStyleSheet(TextBoxStyles.OUTFOCUS.value)
            self.setGeometry(x, y, w, h) # This sets geometry of DraggableObject
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.show()

    # Clicking into the cells is offset for some reason, correcting it
    def mouseDoubleClickEvent(self, e):
        corrected_pos = QPoint(e.pos().x()-25, e.pos().y()-35)
        new_event = QMouseEvent(QEvent.MouseButtonDblClick, corrected_pos, e.button(), e.buttons(), e.modifiers())
        self.setFocus()
        self.setStyleSheet(TextBoxStyles.INFOCUS.value) # Not ideal
        QTableWidget.mouseDoubleClickEvent(self, new_event)


class ImageObj(QTextEdit):
    def __init__(self, editor, x, y, w, h, path):
        super().__init__(editor)

        self.type = 'image'
        self.path = path
        self.setReadOnly(True) # Dont let the user delete the image in its HTML form
        self.setGeometry(x, y, w, h)
        fragment = QTextDocumentFragment.fromHtml(f"<img src={path} height='%1' width='%2'>")
        self.textCursor().insertFragment(fragment)
        self.show()

class ImageObject(QLabel):
    def __init__(self, editor, x, y, w, h, q_image):
        super().__init__(editor)
        self.type = "image_object"
        self.setPixmap(QPixmap(q_image)) # Wierd, but seems to be the best way
        self.setGeometry(x, y, w, h)

def table_object_menu(editor):
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

    return object_menu

# Non DraggableObject things still use this | debt: do we need?
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

def copy_object(editor):
    for o in range(len(editor.object)):
        if (editor.object[o] == editor.focusWidget()):

            # Store the object that was clicked on in the editor's clipboard
            ob = editor.object[o]
            undo_name = ob.objectName()+'(1)'
            if ob.object_type == 'image':
                editor.clipboard_object = ClipboardObject(ob.childWidget.frameGeometry().width(), ob.childWidget.frameGeometry().height(), ob.childWidget.path, ob.object_type, undo_name) # TODO: move name
            elif ob.object_type == 'image_object':
                print("Copying new images is unsupported...")
            elif ob.object_type == 'text':
                editor.clipboard_object = ClipboardObject(ob.childWidget.frameGeometry().width(), ob.childWidget.frameGeometry().height(), ob.childWidget.toHtml(), ob.object_type, undo_name)
            else:
                editor.clipboard_object = ClipboardObject(ob.childWidget.frameGeometry().width(), ob.childWidget.frameGeometry().height(), ob.childWidget.toHtml(), ob.object_type, undo_name, editor.object[o].cols, editor.object[o].rows)

def add_r(editor): # debt: what is this?
    pass
def add_c(editor):
    pass
def del_r(editor):
    pass
def del_c(editor):
    pass

def cut_object(editor):
    if editor.focusWidget().object_type == 'image_object':
        print("Cutting new images is unsupported...")
        return
    copy_object(editor)
    delete_object(editor)
