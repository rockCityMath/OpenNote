from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# delete dc
class UndoActionCreate:
    def __init__(self, draggableContainer):
        self.draggableContainer = draggableContainer

# recreate dc and widget model inside?
class UndoActionDelete:
    def __init__(self, widgetClass, widgetState):
        self.widgetClass = widgetClass
        self.widgetState = widgetState

# apply old geometry
class UndoActionGeometryChange:
    def __init__(self, draggableContainer, oldGeometry):
        self.draggableContainer = draggableContainer
        self.oldGeometry = oldGeometry

# undo things must be called before the draggablecontainer is modified
class UndoHandler:
    def __init__(self):
        self.undoStack = []

    def pushCreate(self, draggableContainer):
        self.undoStack.append(UndoActionCreate(draggableContainer))
        print("PUSHED CREATE")

    def pushDelete(self, draggableContainer):
        widget = draggableContainer.childWidget
        widgetClass = type(widget)
        widgetState = widget.getState()
        self.undoStack.append(UndoActionDelete(widgetClass, widgetState))
        print("PUSHED DELETE")

    def pushGeometryChange(self, draggableContainer, oldGeometry):
        self.undoStack.append(UndoActionGeometryChange(draggableContainer))
        print("PUSHED GEOMETRY CHANGE")

    def undo(self):
        print("UNDO CALLED")
        if len(self.undoStack) == 0:
            return

        undoAction = self.undoStack.pop()
        if isinstance(undoAction, UndoActionCreate):
            # delete the dc
            undoAction.draggableContainer.deleteLater()
            print("UNDO CREATE ", type(undoAction.draggableContainer.childWidget))

        elif isinstance(undoAction, UndoActionDelete):
            # recreate the dc and widget model inside
            widget = undoAction.widgetClass
            print("UNDO DELETE ", widget)


        elif isinstance(undoAction, UndoActionGeometryChange):
            # apply old geometry
            print("UNDO GEO CHANGE ", undoAction.draggableContainer.childWidget)

