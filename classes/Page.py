from datetime import datetime 
from DragItem import DragItem

class Page:
    def __init__(self,title="Untitled"):
        self.title=title
        self.dateCreated=datetime.now()
        
        self.items = set()
        self.parent = None
        self.children=UniqueList()

    #do we need them?
		#not if we use pickle. but in future we may need them
    def save(self):
        pass
    def load(self):
        pass
    
