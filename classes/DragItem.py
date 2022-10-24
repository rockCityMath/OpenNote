class DragItem:
    def __init__(self, uid:int):
        self._uid=uid
        self.pos=[2]
    
    def getUid(self):
        return self._uid
    
test = DragItem(1)
