
from PyQt6.QtCore import *

from PyQt6.QtWidgets import *
from modules.object import *

class Undo:
    def __init__(self, parameter):
        self.parameter = parameter


    def undo(self, editor):
        # Implement the undo operation for this command
        if self.parameter['action']=='move':
            print('move obj to old location')
        elif self.parameter['action']=='create':
            print('delete object')



