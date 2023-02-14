# Event object
from PySide6 import QtCore
from .Notebook import *

class Event(QtCore.QObject):
    notebookSelected = QtCore.Signal(Notebook)

# Global event handler
e = Event()