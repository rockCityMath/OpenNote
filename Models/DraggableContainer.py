from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from enum import Enum

from Modules.Enums import *
from Modules.ObjectMenus import *
from Widgets.Table import TableWidget
from Widgets.Textbox import TextboxWidget
from Widgets.Image import ImageWidget

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

# Object that wraps a child widget and makes it draggable/resizable
# Based off https://wiki.qt.io/Widget-moveable-and-resizeable <3
class DraggableContainer(QWidget):
    menu = None
    mode = Mode.NONE
    position = None
    inFocus = Signal(bool)
    outFocus = Signal(bool)
    newGeometry = Signal(QRect)

    def __init__(self, editor, p, cWidget):
        super().__init__(parent=editor)
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
        self.vLayout = QVBoxLayout(self)
        self.setChildWidget(cWidget)
        self.childWidget = cWidget # Probably better to findChildren()...
        self.m_infocus = True
        self.m_showMenu = False
        self.m_isEditing = True
        self.installEventFilter(editor)
        self.setGeometry(cWidget.geometry())
        self.old_state = {}
        self.newGeometry.connect(self.newGeometryEvent)

        # ***** Pls read before adding anything here  ****
        # In the interest of plugins (especially) and further modularity the DraggableContainer probably shouldnt be concerned with what widget type exactly is in it's child
        # The container should have functionality "modes" eg: visual (images), editable (text, tables) | (or something similar)
        # Or, the signals from this container get passed to the child widget, and it can do what it wants with them?
        # Meaning we probably shouldnt tie anymore widget-specific logic into here because it will have to merge into a "mode" or come out
        if isinstance(cWidget, ImageWidget):
            self.child_object_type = WidgetType.IMAGE
            self.menu = get_object_menu(self.parentWidget())

        elif isinstance(cWidget, TextboxWidget):
            self.child_object_type = WidgetType.TEXT
            self.menu = get_object_menu(self.parentWidget())

        elif isinstance(cWidget, TableWidget):
            self.child_object_type = WidgetType.TABLE
            self.menu = table_object_menu(self.parentWidget())
            self.childWidget.setEditTriggers(QTableWidget.DoubleClicked) # Connect the itemDoubleClicked signal of the table widget to the mouseDoubleClickEvent slot

        else:
            print("An unsupported widget was added to the editor, this will break things.")
            quit()

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

    # This is probably sort of how we should let objects handle events (but without caring about child object type)
    def newGeometryEvent(self, e):
        if self.child_object_type == WidgetType.IMAGE:
            self.childWidget.newGeometryEvent(e, self) # Give reference to this container to the child



    def focusInEvent(self, a0: QFocusEvent):
        if hasattr(self, 'childWidget'): # Widget not present on first focus
            if self.child_object_type == WidgetType.TEXT:
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
        if self.child_object_type == WidgetType.TEXT and self.childWidget.toPlainText() == '': # debt: What does this do
            self.parentWidget().setFocus()
        else:
            self.childWidget.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            self.childWidget.setFocus()

            # Tables need doubleclick, text needs single? Not sure if thats how it works though
            if self.child_object_type == WidgetType.TEXT:
                self.childWidget.mousePressEvent(e)
            elif self.child_object_type == WidgetType.TABLE:
                self.childWidget.mouseDoubleClickEvent(e)

            # Would be ideal if the user could click in the textbox to move the cursor, but the focus events are tricky...
            if self.child_object_type == WidgetType.TEXT:
                self.childWidget.moveCursor(QTextCursor.End)
                self.childWidget.setStyleSheet(TextBoxStyles.INFOCUS.value)

    def keyPressEvent(self, e: QKeyEvent):
        if not self.m_isEditing: return
        return

    # Determine which cursor to show and which mode to be in when user is interacting with the box
    def setCursorShape(self, e_pos: QPoint):
        diff = 10 # Amount of padding from the edge where resize cursors will show

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
        self.parentWidget().undo_stack.append(self.old_state)
        self.parentWidget().autosaver.onChangeMade()
        QWidget.mouseReleaseEvent(self, e)

    def leaveEvent(self, e: QMouseEvent):
        QWidget.leaveEvent(self, e)

        # debt: Comparison after the "and" is an attempt to keep the border when the focus is on a table's qlineedit cell
        if self.parentWidget().focusWidget() != self.childWidget and (type(self.parentWidget().focusWidget()) != QLineEdit):
            self.childWidget.setStyleSheet(TextBoxStyles.OUTFOCUS.value)

    # Determine how to handle the mouse being moved inside the box
    def mouseMoveEvent(self, e: QMouseEvent):
        QWidget.mouseMoveEvent(self, e)

        # Dont need mouse move events on empty textbox
        if self.child_object_type == WidgetType.TEXT and self.childWidget.toPlainText() == '':
            return

        # Dont show border on images
        if self.child_object_type != WidgetType.IMAGE:
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

            print("Real tomove: " + str(toMove))

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

        # debt: To make images resize better, ImageWidget should probaly implement this and setCursorShape
        # So that it can make the cursor move with the corners of pixmap and not corners of this container
        if (self.mode != Mode.MOVE) and e.buttons() and Qt.LeftButton:
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
