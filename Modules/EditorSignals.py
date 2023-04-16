from PySide6.QtCore import *
from PySide6.QtGui import *

from Models.PageModel import PageModel
from Models.SectionModel import SectionModel

class EditorSignals(QObject):
    pageChanged = Signal(PageModel)
    sectionChanged = Signal(SectionModel)

editorSignalsInstance = EditorSignals()
