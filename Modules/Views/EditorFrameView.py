from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from Modules.Enums import WidgetType
from Modules.ObjectActions import add_object, paste_object
from Modules.Multiselect import Multiselector, MultiselectMode
from Models.DraggableContainer import DraggableContainer
# from Models.NotebookModel import NotebookModel

# Ideally this would just interact with the NotebookModel but i dont have that in me rn
class EditorFrameView(QWidget):
    def __init__(self, editor):
        super(EditorFrameView, self).__init__()

        self.editor = editor # Reference to the editor (QMainWindow)
        self.editorFrame = QFrame(editor)
        self.editorFrame.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)
        layout.addWidget(self.editorFrame)
        layout.setContentsMargins(0, 0, 0, 0)

        self.multiselector = Multiselector(self)

        print("BUILT FRAMEVIEW")

    def eventFilter(self, object, event):

        # Only recieves events from DraggableContainers rn, but may need to recieve others at some point
        if isinstance(object, DraggableContainer):
            multiselector = self.multiselector

            # If clicking on an object
            if event.type() == QEvent.MouseButtonPress:
                if multiselector.mode == MultiselectMode.HAS_SELECTED_OBJECTS:
                    multiselector.beginDragIfObjectSelected(object, event)

            if event.type() == QEvent.MouseMove:
                if multiselector.mode == MultiselectMode.IS_DRAGGING_OBJECTS:
                    multiselector.dragObjects(event)
                    return True # Keep the event from going to the draggablecontainer so it doesnt have that mousemoveevent run on it too

            # If in object-moving mode, and the mouse is released, reset all multiselecting
            if event.type() == QEvent.MouseButtonRelease and isinstance(object, DraggableContainer):
                if multiselector.mode == MultiselectMode.IS_DRAGGING_OBJECTS:
                    multiselector.finishDraggingObjects()

            # After the selection is made, its possible that the user moves in and out of selected textboxes,
            # This will remove their focus border, this mitigates that. Note: Do not let this run when the object is moving, its too expensive bc too many paint events
            if multiselector.mode != MultiselectMode.NONE and multiselector.mode != MultiselectMode.IS_DRAGGING_OBJECTS and event.type() == QEvent.Paint:
                multiselector.focusObjectIfInMultiselect()

            return False

        else:
            return False

    def mouseReleaseEvent(self, event):
        editor = self.editor

        if event.button() == Qt.LeftButton:

            # If releasing mouse after drawing multiselect area
            if self.multiselector.mode == MultiselectMode.IS_DRAWING_AREA:
                self.multiselector.finishDrawingArea(event)

            # Releasing the mouse after clicking to add text
            else:
                o = len(editor.object) - 1
                if len(editor.object) > 0:
                    if editor.notebook.page[editor.page].section[editor.section].object[o].type == WidgetType.TEXT:
                        if editor.object[o].childWidget.toPlainText() == '':
                            editor.object[o].deleteLater()
                            editor.object.pop(o)
                            editor.notebook.page[editor.page].section[editor.section].object.pop(o)
                            editor.autosaver.onChangeMade()
                add_object(editor, event, WidgetType.TEXT)
                editor.object[len(editor.object) - 1].childWidget.setFocus()

    def mousePressEvent(self, event):
        editor = self.editor

        # Open context menu on right click
        if event.buttons() == Qt.RightButton:
            editor.setFocus()
            if editor.section > -1:
                frame_menu = QMenu(editor)

                add_image = QAction("Add Image", editor)
                add_image.triggered.connect(lambda: add_object(editor, event, WidgetType.IMAGE))
                frame_menu.addAction(add_image)

                add_table = QAction("Add Table", editor)
                add_table.triggered.connect(lambda: add_object(editor, event, WidgetType.TABLE))
                frame_menu.addAction(add_table)

                paste = QAction("Paste", editor)
                paste.triggered.connect(lambda: paste_object(editor, event))
                frame_menu.addAction(paste)

                take_screensnip = QAction("Snip Screen", editor)
                take_screensnip.triggered.connect(lambda: editor.snipArea({'x': event.pos().x(), 'y': event.pos().y()}))
                frame_menu.addAction(take_screensnip)

                frame_menu.exec(event.globalPos())

    def mouseMoveEvent(self, event): # This event is only called after clicking down on the frame and dragging

        # Set up multi-select on first move of mouse drag
        if self.multiselector.mode != MultiselectMode.IS_DRAWING_AREA:
            self.multiselector.beginDrawingArea(event)

        # Resize multi-select widget on mouse every proceeding mouse movement (dragging)
        else:
            self.multiselector.continueDrawingArea(event)
