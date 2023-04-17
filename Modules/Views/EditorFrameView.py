from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from Modules.Enums import WidgetType
from Modules.ObjectActions import add_object, paste_object
from Modules.Multiselect import Multiselector, MultiselectMode
from Models.DraggableContainer import DraggableContainer
from Widgets.Textbox import TextboxWidget
from Modules.EditorSignals import editorSignalsInstance

# Handles all widget display (could be called widget view, but so could draggablecontainer)
class EditorFrameView(QWidget):
    def __init__(self, editor):
        super(EditorFrameView, self).__init__()

        self.editor = editor # Reference to the editor (QMainWindow)
        self.editorFrame = QFrame(editor)
        self.editorFrame.setStyleSheet("background-color: white;")

        # Layout for the editor frame
        layout = QVBoxLayout(self)
        layout.addWidget(self.editorFrame)
        layout.setContentsMargins(0, 0, 0, 0)

        # Layout where widgets are displayed
        # self.widgetsLayout = QVBoxLayout(self.editorFrame)
        # widgetsLayoutContainerWidget = QWidget()
        # self.widgetsLayout.addWidget(widgetsLayoutContainerWidget)
        # self.widgetsLayout.setContentsMargins(0, 0, 0, 0)

        editorSignalsInstance.sectionChanged.connect(self.sectionChangedEvent)
        editorSignalsInstance.widgetShouldLoad.connect(self.loadWidget)

        self.multiselector = Multiselector(self)

        print("BUILT FRAMEVIEW")

    # Loading a preexisting widget from its model into the frame
    def loadWidget(self, widgetModel):
        print("WILL LOAD WIDGET TYPE: " + str(type(widgetModel)))

    def sectionChangedEvent(self, sectionModel):
        print("FRAME KNOWS SECTION CHANGED")
        print("FRAME: NEW SECTION TITLE: " + sectionModel.title)
        print("FRAME: SECTION'S WIDGET COUNT: ", len(sectionModel.widgets))

        # Hide all old widgets (DraggableContainers)
        for c in self.children():
            if isinstance(c, DraggableContainer) and c.isVisible():
                print(c)
                c.hide()

        # Show all new widgets (DraggableContainers)
        for widget in sectionModel.widgets:
            print(widget)
            widget.show()



    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonRelease:
            print("EAT MOUSE RELEASE FROM DC")
            return True
        return False
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
                # They shouldnt show on construction
                text = TextboxWidget(event.pos().x(), event.pos().y())
                dc = DraggableContainer(text, self)

                editorSignalsInstance.widgetAdded.emit(dc)  # Notify the section view that this widget was added to the current section
                # dc.show()
                # text.show()

                # o = len(editor.object) - 1
                # if len(editor.object) > 0:
                #     if editor.notebook.page[editor.page].section[editor.section].object[o].type == WidgetType.TEXT:
                #         if editor.object[o].childWidget.toPlainText() == '':
                #             editor.object[o].deleteLater()
                #             editor.object.pop(o)
                #             editor.notebook.page[editor.page].section[editor.section].object.pop(o)
                #             editor.autosaver.onChangeMade()
                # add_object(editor, event, WidgetType.TEXT)
                # editor.object[len(editor.object) - 1].childWidget.setFocus()

    def mousePressEvent(self, event):
        print("EDITORFRAME MOUSEPRESS")
        editor = self.editor

        # Open context menu on right click
        if event.buttons() == Qt.RightButton:
            # editor.setFocus()
            frame_menu = QMenu(self)

            add_image = QAction("Add Image", editor)
            add_image.triggered.connect(lambda: print("ADD IMAGE"))
            frame_menu.addAction(add_image)

            add_table = QAction("Add Table", editor)
            add_table.triggered.connect(lambda: print("ADD TABLE"))
            frame_menu.addAction(add_table)

            paste = QAction("Paste", editor)
            paste.triggered.connect(lambda: print("PASTE"))
            frame_menu.addAction(paste)

            take_screensnip = QAction("Snip Screen", editor)
            take_screensnip.triggered.connect(lambda: print("SNIP SCREEN"))
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
