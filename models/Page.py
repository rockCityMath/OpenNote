from datetime import datetime
from models.DragItem import DragItem
from models.util import UniqueList
import pickle

class Page:
    def __init__(self, title="Untitled"):
        self.title = title
        self.dateCreated = str(datetime.now())
        self.items = set()
        # self.parent = None
        # self.children = UniqueList()

    # def setChild(self, page):
    #     if page.parent != None:
    #         page.parent.children.remove(page)

    #     page.parent = self
    #     self.children.append(page)

    def dictify(self):
        megadict = {}
        megadict['title'] = self.title
        megadict['dateCreated'] = self.dateCreated
        megadict['items'] = []
        for item in self.items:
            megadict['items'].append(pickle.dumps(item.dictify()))
        return megadict
    
    def dedictify(self,dict):
        self.title = dict['title']
        self.dateCreated = dict['dateCreated']
        self.items=set()
        for item in  dict['items']:
            itemObj = pickle.loads(item)
            self.items.add(DragItem(itemObj['pos']))
        
