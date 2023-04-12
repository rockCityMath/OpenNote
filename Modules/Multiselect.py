from enum import Enum
from Modules.Enums import TextBoxStyles

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class MultiselectMode(Enum):
    NONE = 0,
    IS_DRAWING_AREA = 1,
    HAS_SELECTED_OBJECTS = 2,
    IS_DRAGGING_OBJECTS = 3

class Multiselector():
    def __init__(self, editorFrame):
        self.editorFrame = editorFrame

        self.drawingWidget = QWidget(editorFrame)  # Allows the user to see their selected area
        self.mode = MultiselectMode.NONE           # Tracks what state the multiselect is in

        self.drawAreaStartLocalPos = None          # Point where user starts drawing to select multiple objects
        self.drawAreaStartGlobalPos = None
        self.selectedObjects = []                  # All objects in the user's selected area
        self.dragInitEventPos = None               # Position of the event that started the dragging
        self.dragOffset = None                     # Offset of object that is used to drag the others from the first object in the editors list

    def beginDrawingArea(self, event):
        self.mode = MultiselectMode.IS_DRAWING_AREA
        self.drawingWidget.setStyleSheet(TextBoxStyles.INFOCUS.value)
        self.drawingWidget.setGeometry(event.pos().x(), event.pos().y(), 0, 0)
        self.drawingWidget.show()
        self.drawAreaStartLocalPos = event.pos()
        self.drawAreaStartGlobalPos = event.globalPos()

    def continueDrawingArea(self, event):
        width = event.pos().x() - self.drawAreaStartLocalPos.x()
        height = event.pos().y() - self.drawAreaStartLocalPos.y()

        self.drawingWidget.resize(width, height)

    def finishDrawingArea(self, event):
        editor = self.editorFrame.editor

        # Throw away if the area of the selection is negative (user dragged from bottom right to top left)
        if self.drawAreaStartGlobalPos.x() > event.globalPos().x() or self.drawAreaStartGlobalPos.y() > event.globalPos().y():
            self.drawingWidget.hide()
            self.finishDraggingObjects()
            # You could probably switch around the coordinates in here and modify drawing logic to support other drag directions
            return

        # Get all DraggableContainers in the selection
        for o in editor.object:

            # Map all positions to global for correct coord checks
            ob_tl_pos = o.mapToGlobal(QPoint(0, 0)) # Object top left corner
            start_pos = self.drawAreaStartGlobalPos
            end_pos = event.globalPos()

            # If object x + width is between start and end x, and object y + height is between start and end y
            if ob_tl_pos.x() > start_pos.x() and ob_tl_pos.x() + o.width() < end_pos.x():
                if ob_tl_pos.y() > start_pos.y() and ob_tl_pos.y() + o.height() < end_pos.y():
                    self.selectedObjects.append(o)

        if len(self.selectedObjects) > 0:
            self.mode = MultiselectMode.HAS_SELECTED_OBJECTS

        # Hide selection area
        self.drawingWidget.hide()

    def beginDragIfObjectSelected(self, object, event):
        if object in self.selectedObjects:
            self.mode = MultiselectMode.IS_DRAGGING_OBJECTS
            self.dragInitEventPos = event.pos()
            self.dragOffset = object.pos() - self.selectedObjects[0].pos()

    def dragObjects(self, event):

        # Get the position that each object would move to
        objectPositions = []
        for o in reversed(self.selectedObjects): # fuck it, reversed

            # You have to know this, focus
            # Position of the first (in the reversed array) object's top left corner + the offset of the click inside the selected object - the position of the object to move
            offsetPositionFromInitObject = self.selectedObjects[0].pos() + self.dragInitEventPos - o.pos()
            toMove = event.globalPos() - offsetPositionFromInitObject

            # For some reason it will kind of attempt to move the objects as if the last object in the array was selected by the user
            # So offset that, then add a y offset becase it does something weird with that too
            toMove = toMove - self.dragOffset - QPoint(0, 20)

            # If an object wants to move out of bounds, quit the loop and eat the event
            if toMove.x() < 0: return True
            if toMove.y() < 0: return True
            if toMove.x() > o.parentWidget().width() - o.width(): return True
            if(toMove.x() < o.parentWidget().width() - o.parentWidget().frame.width()): return True
            if(toMove.y() < o.parentWidget().height() - o.parentWidget().frame.height()): return True
            if(toMove.y() > o.parentWidget().frame.height() + 20): return True

            objectPositions.append(toMove)

        # If no objects would move out of bounds, perform the moves
        for i, o in enumerate(reversed(self.selectedObjects)):
            o.move(objectPositions[i])
            o.newGeometry.emit(o.geometry())

    def finishDraggingObjects(self):
        try:
            for o in self.selectedObjects:
                o.childWidget.setStyleSheet(TextBoxStyles.OUTFOCUS.value)
        except:
            pass # Generally only fails because the object references are gone so we want to exit anyways

        self.mode = MultiselectMode.NONE

        self.drawAreaStartLocalPos = None
        self.drawAreaStartGlobalPos = None
        self.selectedObjects = []
        self.dragInitEventPos = None
        self.dragOffset = None

    def focusObjectIfInMultiselect(self):

        # Exits multiselecting if the selected object references are no longer accessible
        try:
            for o in self.selectedObjects:
                o.childWidget.setStyleSheet(TextBoxStyles.INFOCUS.value)
        except:
            self.finishDraggingObjects()
