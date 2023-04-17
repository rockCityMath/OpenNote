from PySide6.QtCore import *
from PySide6.QtGui import *
from typing import Any

class EditorSignals(QObject):

    # Cant be statically typed because importing the classes causes circular imports

    pageChanged = Signal(Any) # Recieves PageModel
    sectionChanged = Signal(Any) # Receives SectionModel
    widgetAdded = Signal(Any) # Receives DraggableContainer
    widgetShouldLoad = Signal(Any) # Recieves any widget model

editorSignalsInstance = EditorSignals()
