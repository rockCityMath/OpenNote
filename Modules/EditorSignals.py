from PySide6.QtCore import *
from PySide6.QtGui import *
from enum import Enum

class ChangedWidgetAttribute(Enum):
    BackgroundColor = 0
    FontColor = 1
    Font = 2
    FontSize = 3
    FontBold = 4
    FontItalic = 5
    FontUnderline = 6

# Cant be statically typed because importing the classes causes circular imports

class EditorSignals(QObject):

    pageChanged = Signal(object) # Recieves PageModel
    sectionChanged = Signal(object) # Receives SectionModel

    # Recieves DraggableContainer
    widgetAdded = Signal(object)
    widgetRemoved = Signal(object)
    widgetCopied = Signal(object)

    # Recieves any widget model, and the section model to add the instance of DraggableContainer to
    widgetShouldLoad = Signal(object, object)

    # Receives (ChangedWidgetAttribute, value)
    widgetAttributeChanged = Signal(object, object)

editorSignalsInstance = EditorSignals()
