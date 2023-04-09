# Holds clipboard object info, QT things can't be copied by value :(
class Clipboard:
    def __init__(self, width, height, data, type, undo_name, row=0, col=0):
        self.width = width
        self.height = height
        self.data = data # data should contain everything the object needs to be reconstructed 
        self.type = type
        self.undo_name = undo_name
        self.row=row
        self.col=col
        
