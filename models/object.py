# Draggable objects that can be used in the editor
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from enum import Enum

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
    def __init__(self, width, height, html, type, undo_name):
        self.width = width
        self.height = height
        self.html = html
        self.undo_name = undo_name
        self.type = type

# Based off https://wiki.qt.io/Widget-moveable-and-resizeable <3
class DraggableObject(QWidget):
    menu = None
    mode = Mode.NONE
    position = None
    inFocus = Signal(bool)
    outFocus = Signal(bool)
    newGeometry = Signal(QRect)

    # Parent should be called editor, its always the editor
    def __init__(self, parent, p, cWidget):
        super().__init__(parent=parent)

        self.menu = get_object_menu(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setVisible(True)
        self.setAutoFillBackground(False)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setFocus()
        self.move(p)

        self.vLayout = QVBoxLayout(self)
        self.setChildWidget(cWidget)
        self.childWidget = cWidget # Probably better to findChildren()...
        self.m_infocus = True
        self.m_showMenu = False
        self.m_isEditing = True
        self.installEventFilter(parent)
        self.setGeometry(cWidget.geometry())

        if isinstance(cWidget, ImageObj): self.object_type = 'image' # cleaner to do this here
        else: self.object_type = 'text' # these should probably be an enum everywhere

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
        self.childWidget.setStyleSheet(TextBoxStyles.OUTFOCUS.value)
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
        self.childWidget.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.childWidget.setFocus()

        # Would be ideal if the user could click in the textbox to move the cursor, but the focus events are tricky...
        self.childWidget.moveCursor(QTextCursor.End)
        self.childWidget.setStyleSheet(TextBoxStyles.INFOCUS.value)

    def keyPressEvent(self, e: QKeyEvent):
        if not self.m_isEditing: return
        return

    # Determine which cursor to show and which mode to be in when user is interacting with the box
    def setCursorShape(self, e_pos: QPoint):
        diff = 10 # Amount of padding from the edge where resize cursors will show

        # Not allowing resizable images for now
        if self.object_type == 'image':
            self.setCursor(QCursor(Qt. ArrowCursor))
            self.mode = Mode.MOVE
            return

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
        self.parentWidget().autosaver.onChangeMade()
        QWidget.mouseReleaseEvent(self, e)

    # Determine how to handle the mouse being moved inside the box
    def mouseMoveEvent(self, e: QMouseEvent):
        QWidget.mouseMoveEvent(self, e)
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
            self.parentWidget().repaint()
            return
        if (self.mode != Mode.MOVE) and e.buttons() and Qt.LeftButton:

            # Not allowing resizable images for now
            if self.object_type == 'image':
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
    def __init__(self, editor, x, y, w, h, text):
        super().__init__(editor)

        self.editor = editor
        self.type = 'text'
        self.setStyleSheet(TextBoxStyles.OUTFOCUS.value)
        self.setGeometry(x, y, w, h) # This sets geometry of DraggableObject
        self.setText(text)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.show()

        self.textChanged.connect(lambda: editor.autosaver.onChangeMade())

class ImageObj(QTextEdit):
    def __init__(self, editor, x, y, w, h, path):
        super().__init__(editor)

        self.type = 'image'
        self.path = path
        self.setReadOnly(True) # Dont let the user delete the image in its HTML form
        self.setGeometry(x, y, w, h)
        fragment = QTextDocumentFragment.fromHtml(f"<img src={path} height='%1' width='%2'>")
        self.textCursor().insertFragment(fragment)
#        self.mouseDoubleClickEvent = lambda event: drag(editor, event)
#        self.setContextMenuPolicy(Qt.CustomContextMenu)
#        self.customContextMenuRequested.connect(lambda event: object_menu(editor, event))
        self.show()

# Select TextBox for font styling
def select(editor, event):
    editor.selected = editor.focusWidget()

def drag(editor, event):
    if (event.buttons() == Qt.LeftButton):
        drag = QDrag(editor)
        mimeData = QMimeData()
        drag.setMimeData(mimeData)
        drag.exec(Qt.MoveAction)

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

# Non DraggableObject things still use this
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
            undo_name = ob.objectName()+'(1)'
            if ob.object_type == 'image':
                editor.clipboard_object = ClipboardObject(ob.childWidget.frameGeometry().width(), ob.childWidget.frameGeometry().height(), ob.childWidget.path, ob.object_type, undo_name) # TODO: move name
            else:
                editor.clipboard_object = ClipboardObject(ob.childWidget.frameGeometry().width(), ob.childWidget.frameGeometry().height(), ob.childWidget.toHtml(), ob.type, undo_name)


def cut_object(editor):
    copy_object(editor)
    delete_object(editor)

