from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from Modules.Enums import *
from Modules.EditorSignals import editorSignalsInstance, ChangedWidgetAttribute
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

# Object that wraps a child widget and makes it draggable/resizable (read: manages geometry)
# Based off https://wiki.qt.io/Widget-moveable-and-resizeable <3
class DraggableContainer(QWidget):
    menu = None
    mode = Mode.NONE
    position = None
    outFocus = Signal(bool)
    newGeometry = Signal(QRect)

    def __init__(self, childWidget, editorFrame):
        super().__init__(parent=editorFrame)

        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAutoFillBackground(False)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setFocus()
        self.old_x = 0
        self.old_y = 0
        self.vLayout = QVBoxLayout(self)
        self.setChildWidget(childWidget)
        self.m_showMenu = False
        self.m_isEditing = True
        # self.installEventFilter(editorFrame)
        self.setGeometry(childWidget.geometry())
        self.old_state = {}
        self.isSelected = False

        self.previousGeometry = self.geometry() # for undo

        self.childWidgetActive = False
        self.menu = self.buildDragContainerMenu()

        if hasattr(self.childWidget, "newGeometryEvent"): self.newGeometry.connect(childWidget.newGeometryEvent)
        editorSignalsInstance.widgetAttributeChanged.connect(self.widgetAttributeChanged)

    def setChildWidget(self, childWidget):
        if childWidget:
            self.childWidget = childWidget
            self.childWidget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            self.childWidget.setParent(self)
            self.childWidget.releaseMouse()
            self.childWidget.installEventFilter(self)
            self.vLayout.addWidget(childWidget)
            self.vLayout.setContentsMargins(0,0,0,0)

    def eventFilter(self, obj, event):

        # If child widget resized itsself, resize this drag container, not ideal bc child resizes on hover
        if isinstance(event, QResizeEvent):
            self.resize(self.childWidget.size())
        return False

    def popupShow(self, pt: QPoint):
        global_ = self.mapToGlobal(pt)
        self.m_showMenu = True
        self.menu.exec(global_)
        self.m_showMenu = False

    def mousePressEvent(self, e: QMouseEvent):
        self.position = QPoint(e.globalX() - self.geometry().x(), e.globalY() - self.geometry().y())

        print("DC MOUSE PRESS")

        # Undo related
        # self.old_x = e.globalX()
        # self.old_y = e.globalY()
        # self.old_state = {'type':'object','action':'move','name':self.name,'x':self.old_x,'y':self.old_y}

        self.previousGeometry = self.geometry()

        if not self.m_isEditing:
            print("NOT EDIT")
            return
        if not e.buttons() and Qt.LeftButton:
            print("DC GOT MOUSE PRESS")
            self.setCursorShape(e.pos())
            return True
        if e.button() == Qt.RightButton:
            self.popupShow(e.pos())
            e.accept()

    # On double click, focus on child and make mouse events pass through this container to child
    def mouseDoubleClickEvent(self, e: QMouseEvent):
        self.childWidget.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.childWidget.setFocus()
        return

    def mouseReleaseEvent(self, e: QMouseEvent):
        # self.parentWidget().undo_stack.append(self.old_state)
        # self.parentWidget().autosaver.onChangeMade()

        self.parentWidget().newGeometryOnDCEvent(self)
        return True # Dont let the release go to the editor frame

    def leaveEvent(self, e: QMouseEvent):
        self.childWidget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setStyleSheet("border: none;")

        # Delete this DC if childWidget says it's empty
        if hasattr(self.childWidget, "checkEmpty"):
            if self.childWidget.checkEmpty():
                editorSignalsInstance.widgetRemoved.emit(self)

        # ???
        if self.childWidget.hasFocus():
            self.setFocus()

    def buildDragContainerMenu(self):
        menu = QMenu()

        delete = QAction("Delete", self)
        delete.triggered.connect(lambda: editorSignalsInstance.widgetRemoved.emit(self))
        menu.addAction(delete)

        copy = QAction("Copy", self)
        copy.triggered.connect(lambda: editorSignalsInstance.widgetCopied.emit(self))
        menu.addAction(copy)

        cut = QAction("Cut", self)
        cut.triggered.connect(lambda: print("CUT"))
        menu.addAction(cut)

        cut = QAction("Select", self)
        cut.triggered.connect(lambda: self.select)
        menu.addAction(cut)

        # Append widget specific menu items
        widgetCustomMenu = getattr(self.childWidget, "customMenuItems", None)
        if callable(widgetCustomMenu):
            widgetSpecificItems = self.childWidget.customMenuItems()
            for item in widgetSpecificItems:
                menu.addAction(item)

        return menu

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

    # Determine how to handle the mouse being moved inside the box
    def mouseMoveEvent(self, e: QMouseEvent):
        self.setStyleSheet("border: 1px dashed rgba(0, 0, 0, 0.5)")
        # QWidget.mouseMoveEvent(self, e) need??

        if not self.m_isEditing:
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

            self.move(toMove)
            self.newGeometry.emit(self.geometry())
            self.parentWidget().repaint()

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

    # Pass the event to the child widget if this container is focuesd, and childwidget implements the method to receive it
    def widgetAttributeChanged(self, changedWidgetAttribute, value):

        cw = self.childWidget

        if hasattr(cw, "changeFontSizeEvent") and (changedWidgetAttribute == ChangedWidgetAttribute.FontSize):
            cw.changeFontSizeEvent(value)

        if hasattr(cw, "changeFontBoldEvent") and (changedWidgetAttribute == ChangedWidgetAttribute.FontBold):
            cw.changeFontBoldEvent()

        if hasattr(cw, "changeFontItalicEvent") and (changedWidgetAttribute == ChangedWidgetAttribute.FontItalic):
            cw.changeFontItalicEvent()

        if hasattr(cw, "changeFontUnderlineEvent") and (changedWidgetAttribute == ChangedWidgetAttribute.FontUnderline):
            cw.changeFontUnderlineEvent()

        if hasattr(cw, "changeFontEvent") and (changedWidgetAttribute == ChangedWidgetAttribute.Font):
            cw.changeFontEvent(value)

        if hasattr(cw, "changeFontColorEvent") and (changedWidgetAttribute == ChangedWidgetAttribute.FontColor):
            cw.changeFontColorEvent(value)

        if hasattr(cw, "changeBackgroundColorEvent") and (changedWidgetAttribute == ChangedWidgetAttribute.BackgroundColor):
            cw.changeBackgroundColorEvent(value)

