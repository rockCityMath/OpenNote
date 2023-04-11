from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from Modules.BuildUI import *
from Modules.Save import Autosaver
from Modules.Screensnip import SnippingWidget
from Modules.ObjectActions import *
from Models.DraggableContainer import DraggableContainer
from Modules.Enums import TextBoxStyles

from Models.Notebook import Notebook

# models.notebook.Notebook is where all Notebook and Object data is stored
# models.object.* are models for Widgets used in the editor
#   Notebook Objects and Widgets from these models share params (geometry, text, image path, etc.)
#   Pickle will save the Notebook object
#   The editor will create and destroy Widgets per Page/Section (see modules.page.change_section, modules.load.build)
#       A Section's Widgets also exist in self.object, ordered by time of creation

class Editor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.notebook = Notebook('Untitled Notebook')    # Current notebook object
        self.object = []                        # List of Widgets on current Page/Section
        self.page = -1                          # Index of current Page (New notebook has no pages: set to -1)
        self.section = -1                       # Index of current Section (New notebook has no sections: set to -1)
        self.selected = None                    # Selected object (for font attributes of TextBox)

        self.autosaver = Autosaver(self, self.notebook)  # Object with method for indicating changes and determining if we should autosave
        self.undo_stack = [] #QUndoStack()
        self.temp_buffer = []
        self.shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut.setContext(Qt.ApplicationShortcut)
        self.shortcut.activated.connect(self.undo_event)
        self.setFocus()
        self.snippingWidget = SnippingWidget(app=QApplication.instance())
        self.snippingWidget.onSnippingCompleted = self.onSnippingCompleted

        build_ui(self)

    # Do this on multiselect object instead
    def eventFilter(self, object, event):

        if isinstance(object, DraggableContainer):

            # If clicking on an object
            if event.type() == QEvent.MouseButtonPress:

                # If in multi-object moving mode
                if self.frame.isMultiObjectMoving:

                    # If clicking on selected object
                    if object in self.frame.selectedObjects:
                        self.frame.isMovingObjects = True # is in object moving mode
                        self.frame.firstSelectionEventPos = event.pos() # position of the click inside the selected widget
                        self.frame.firstSelectedObject = self.frame.selectedObjects[0]
                        self.frame.randomOffset = object.pos() - self.frame.firstSelectedObject.pos()

            # If dragging objects in object-move mode
            if event.type() == QEvent.MouseMove and self.frame.isMovingObjects and isinstance(object, DraggableContainer):
                for o in reversed(self.frame.selectedObjects): # fuck it, reversed

                    # Position of the first object's top left corner + the offset of the click inside the selected object - the position of the current object
                    offsetPositionFromInitObject = self.frame.selectedObjects[0].pos() + self.frame.firstSelectionEventPos - o.pos()
                    toMove = event.globalPos() - offsetPositionFromInitObject

                    # For some reason it will kind of attempt to move the objects as if the last object in the array was selected by the user
                    # So offset that, then add a y offset becase it does something weird with that too
                    toMove = toMove - self.frame.randomOffset - QPoint(0, 20)

                    # Dont go out of bounds - super wierd behavoir
                    if toMove.x() < 0: return True
                    if toMove.y() < 0: return True
                    if toMove.x() > o.parentWidget().width() - o.width(): return True
                    if(toMove.x() < o.parentWidget().width() - o.parentWidget().frame.width()): return True
                    if(toMove.y() < o.parentWidget().height() - o.parentWidget().frame.height()): return True
                    if(toMove.y() > o.parentWidget().frame.height() + 20): return True

                    o.move(toMove)
                    o.newGeometry.emit(o.geometry())
                    o.childWidget.setStyleSheet(TextBoxStyles.INFOCUS.value)

                return True # Keep the event from going to the draggablecontainer so it doesnt have that mousemoveevent run on it too

            # If in object-moving mode, and the mouse is released, reset all multiselecting
            if event.type() == QEvent.MouseButtonRelease and self.frame.isMovingObjects and isinstance(object, DraggableContainer):
                print("Released")

                # CLEAN THIS
                self.frame.isMultiselecting = False
                self.frame.isMultiObjectMoving = False
                self.frame.isMovingObjects = False
                self.frame.multiSelectWidget = None
                self.frame.multiSelectStartLocalPos = None
                self.frame.multiSelectStartGlobalPos = None
                for rem in self.frame.selectedObjects:
                    rem.childWidget.setStyleSheet(TextBoxStyles.OUTFOCUS.value)
                self.frame.selectedObjects = []
                self.frame.firstSelectionEventPos = None
                self.frame.firstSelectedObject = None
                self.frame.randomOffset = None
                self.frame.isFirstMove = True

            # On any paint event, make sure selected objects keep their border | Not ideal but...
            if event.type() == QEvent.Paint and self.frame.isMultiObjectMoving and object in self.frame.selectedObjects:
                object.childWidget.setStyleSheet(TextBoxStyles.INFOCUS.value)

            return False

        else:
            return False

    # When user finishes screensnip, bring back main window and add image to notebook
    def onSnippingCompleted(self, image_matrix):
        self.setWindowState(Qt.WindowActive)
        self.showMaximized()
        if image_matrix is None:
            return

        pos = self.snippingWidget.event_pos
        add_snip(self, pos, image_matrix)

    def snipArea(self, event_pos):
        self.setWindowState(Qt.WindowMinimized)
        self.snippingWidget.start(event_pos)

    # Drag object event
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        obj = self.focusWidget()
        self.temp_buffer.append({'type':'object','action':'move','name':obj.objectName(),'x':event.pos().x(),'y':event.pos().y()})

    def focusInEvent(self, event):
        self.repaint()

    def undo_event(self):
        if len(self.undo_stack)>0:
            pop_item = self.undo_stack.pop(-1)
            if pop_item['type']=='object':
                index = 0
                for i in range(len(self.notebook.page[self.page].section[self.section].object)):
                    if pop_item['name']==self.notebook.page[self.page].section[self.section].object[i].name:
                        index=i
                #TODO instead of object[0] i need to find object by name
                if pop_item['action'] == 'move':
                    params = self.notebook.page[self.page].section[self.section].object[index]
                    params.x = pop_item['x']
                    params.y = pop_item['y']
                    self.notebook.page[self.page].section[self.section].object[index] = params

                    self.object[index].deleteLater()

                    self.object.pop(index)
                    #deleting in old position
                    build_object(self,params)
                    self.autosaver.onChangeMade()
                elif pop_item['action'] == 'create':
                    self.object[index].deleteLater()
                    self.object.pop(index)
                    self.notebook.page[self.page].section[self.section].object.pop(index)
                    self.autosaver.onChangeMade()
                else:
                    # self.object.append(pop_item['data'])
                    self.notebook.page[self.page].section[self.section].object.append(pop_item['data'])
                    build_object(self,pop_item['data'])
                    self.autosaver.onChangeMade()
