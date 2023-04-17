from PySide6.QtCore import *
from PySide6.QtGui import *

class EditorSignals(QObject):

    # Cant be statically typed because importing the classes causes circular imports

    pageChanged = Signal(object) # Recieves PageModel
    sectionChanged = Signal(object) # Receives SectionModel
    widgetAdded = Signal(object) # Receives DraggableContainer

    # Recieves any widget model, and the section model to add the instance of DraggableContainer to
    widgetShouldLoad = Signal(object, object)

editorSignalsInstance = EditorSignals()
