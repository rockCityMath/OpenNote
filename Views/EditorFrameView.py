from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from Modules.Multiselect import Multiselector, MultiselectMode
from Models.DraggableContainer import DraggableContainer
from Widgets.Textbox import TextboxWidget
from Modules.EditorSignals import editorSignalsInstance
from Widgets.Image import ImageWidget
from Modules.Screensnip import SnippingWidget
from Widgets.Table import TableWidget
from Modules.Clipboard import Clipboard
from Modules.Undo import UndoHandler

# Handles all widget display (could be called widget view, but so could draggablecontainer)
class EditorFrameView(QWidget):
    def __init__(self, editor):
        super(EditorFrameView, self).__init__()

        self.editor = editor # Store reference to the editor (QMainWindow)
        self.editorFrame = QFrame(editor)
        self.editorFrame.setStyleSheet("background-color: white;")

        # Layout for the editor frame
        layout = QVBoxLayout(self)
        layout.addWidget(self.editorFrame)
        layout.setContentsMargins(0, 0, 0, 0)

        editorSignalsInstance.sectionChanged.connect(self.sectionChangedEvent)
        editorSignalsInstance.widgetShouldLoad.connect(self.loadWidgetEvent)
        editorSignalsInstance.widgetRemoved.connect(self.removeWidgetEvent)

        # Modularized functionality for the editorFrame and its widgets
        self.multiselector = Multiselector(self)
        self.clipboard = Clipboard()
        self.undoHandler = UndoHandler()

        # Undo setup
        self.shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut.setContext(Qt.ApplicationShortcut)
        self.shortcut.activated.connect(self.undoHandler.undo)
        self.undoHandler.undoWidgetDelete.connect(self.undoWidgetDeleteEvent)

        print("BUILT FRAMEVIEW")

    def pasteWidget(self, clickPos):
        widgetOnClipboard = self.clipboard.getWidgetToPaste()

        dc = DraggableContainer(widgetOnClipboard, self)
        self.undoHandler.pushCreate(dc)
        editorSignalsInstance.widgetAdded.emit(dc)  # Notify section that widget was added
        dc.move(clickPos.x(), clickPos.y())
        dc.show()

    def snipScreen(self, clickPos):
        def onSnippingCompleted(imageMatrix):            # Called after screensnipper gets image
            self.editor.setWindowState(Qt.WindowActive)
            self.editor.showMaximized()
            if imageMatrix is None:
                return

            widgetModel = ImageWidget.newFromMatrix(clickPos, imageMatrix)
            dc = DraggableContainer(widgetModel, self)
            self.undoHandler.pushCreate(dc)
            editorSignalsInstance.widgetAdded.emit(dc)   # Notify the current section and editorFrame that a widget was added
            dc.show()

        # Begin screensnip
        self.editor.setWindowState(Qt.WindowMinimized)
        self.snippingWidget = SnippingWidget()
        self.snippingWidget.onSnippingCompleted = onSnippingCompleted
        self.snippingWidget.start(clickPos)

    def newWidgetOnSection(self, widgetClass, clickPos):
        print("ADDWIDGET: ", widgetClass)
        try:
            widget = widgetClass.new(clickPos)          # All widget classes implement .new() static method
            dc = DraggableContainer(widget, self)
            dc.show()

            self.undoHandler.pushCreate(dc)             # Push to undo stack
            editorSignalsInstance.widgetAdded.emit(dc)  # Notify the current section that a widget was added
            dc.mouseDoubleClickEvent(None)              # Enter the child widget after adding

        except Exception as e:
            print("Error adding widget: ", e)

    # When the DC geometry is changed, tell the undoHandler
    def newGeometryOnDCEvent(self, dc):
        self.undoHandler.pushGeometryChange(dc, dc.previousGeometry)

    # Special case for adding a widget by undoing a delete, since position is already set
    def undoWidgetDeleteEvent(self, widget):
        print("UNDO DELETE EVENT")
        try:
            dc = DraggableContainer(widget, self)
            dc.show()
            editorSignalsInstance.widgetAdded.emit(dc)  # Notify the current section that a widget was added

        except Exception as e:
            print("Error adding widget: ", e)

    def removeWidgetEvent(self, draggableContainer):
        self.undoHandler.pushDelete(draggableContainer)
        draggableContainer.deleteLater()

    # Loading a preexisting (saved) widget into the frame inside a DraggableContainer
    # Then add that DC instance reference to the sectionModel's widgets[] for runtime
    def loadWidgetEvent(self, widgetModel, sectionModel):
        dc = DraggableContainer(widgetModel, self)
        sectionModel.widgets.append(dc)
        print("LOADED CONTENT: ", widgetModel)

    def sectionChangedEvent(self, sectionModel):
        print("FRAME: NEW SECTION TITLE: " + sectionModel.title)

        # Hide all old widgets
        for c in self.children():
            if isinstance(c, DraggableContainer):
                print(c)
                c.hide()

        # Show all new widgets
        for widget in sectionModel.widgets:
            print(widget)
            widget.show()

        # probably move this to a multiselector class
        # Only recieves events from DraggableContainers rn, but may need to recieve others at some point
        # if isinstance(object, DraggableContainer):
        #     multiselector = self.multiselector

        #     # If clicking on an object
        #     if event.type() == QEvent.MouseButtonPress:
        #         print("EVENTFILTER TOOK EVENT")
        #         if multiselector.mode == MultiselectMode.HAS_SELECTED_OBJECTS:
        #             multiselector.beginDragIfObjectSelected(object, event)

        #     if event.type() == QEvent.MouseMove:
        #         if multiselector.mode == MultiselectMode.IS_DRAGGING_OBJECTS:
        #             multiselector.dragObjects(event)
        #             return True # Keep the event from going to the draggablecontainer so it doesnt have that mousemoveevent run on it too

        #     # If in object-moving mode, and the mouse is released, reset all multiselecting
        #     if event.type() == QEvent.MouseButtonRelease and isinstance(object, DraggableContainer):
        #         if multiselector.mode == MultiselectMode.IS_DRAGGING_OBJECTS:
        #             multiselector.finishDraggingObjects()

        #     # After the selection is made, its possible that the user moves in and out of selected textboxes,
        #     # This will remove their focus border, this mitigates that. Note: Do not let this run when the object is moving, its too expensive bc too many paint events
        #     if multiselector.mode != MultiselectMode.NONE and multiselector.mode != MultiselectMode.IS_DRAGGING_OBJECTS and event.type() == QEvent.Paint:
        #         multiselector.focusObjectIfInMultiselect()

        #     return False

        # else:
        #     return False

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:

            # If releasing mouse after drawing multiselect area
            if self.multiselector.mode == MultiselectMode.IS_DRAWING_AREA:
                self.multiselector.finishDrawingArea(event)

            # Releasing the mouse after clicking to add text
            else:
                self.newWidgetOnSection(TextboxWidget, event.pos())

    def mousePressEvent(self, event):
        print("EDITORFRAME MOUSEPRESS")
        editor = self.editor

        # Open context menu on right click
        if event.buttons() == Qt.RightButton:
            frame_menu = QMenu(self)

            add_image = QAction("Add Image", self)
            add_image.triggered.connect(lambda: self.newWidgetOnSection(ImageWidget, event.pos()))
            frame_menu.addAction(add_image)

            add_table = QAction("Add Table", editor)
            add_table.triggered.connect(lambda: self.newWidgetOnSection(TableWidget, event.pos()))
            frame_menu.addAction(add_table)

            paste = QAction("Paste", editor)
            paste.triggered.connect(lambda: self.pasteWidget(event.pos()))
            frame_menu.addAction(paste)

            take_screensnip = QAction("Snip Screen", editor)
            take_screensnip.triggered.connect(lambda: self.snipScreen(event.pos()))
            frame_menu.addAction(take_screensnip)

            frame_menu.exec(event.globalPos())



    def mouseMoveEvent(self, event): # This event is only called after clicking down on the frame and dragging
        return
        # Set up multi-select on first move of mouse drag
        # if self.multiselector.mode != MultiselectMode.IS_DRAWING_AREA:
        #     self.multiselector.beginDrawingArea(event)

        # # Resize multi-select widget on mouse every proceeding mouse movement (dragging)
        # else:
        #     self.multiselector.continueDrawingArea(event)
