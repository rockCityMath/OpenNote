from PyQt6.QtCore import *

from PyQt6.QtWidgets import *


class Undo:
    def __init__(self, parameter):
        self.parameter = parameter

    def redo(self):
        # Implement the operation that this command represents
        print(self.parameter+'redo')

    def undo(self):
        # Implement the undo operation for this command
        print(self.parameter+'undo')

# print(print(issubclass(PageUndo, QUndoCommand)))