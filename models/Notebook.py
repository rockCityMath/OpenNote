from datetime import datetime
from models.Page import Page
from models.DragItem import DragItem
from models.util import UniqueList
import pickle

class Notebook:
    def __init__(self, title="Untitled"):
        self.title = title
        self.pages = UniqueList()  # no dups
        self.location = None
        self.dateCreated = str(datetime.now())
        self.dateEdited = str(datetime.now())

    def save(self):
        megadict = {}
        megadict['title'] = self.title
        megadict['pages'] = []
        megadict['dateCreated'] = self.dateCreated
        for page in self.pages:
            # if page.parent != None:
            #     continue
            megadict['pages'].append(pickle.dumps(page.dictify()))

        megadict['dateEdited'] = str(datetime.now())
        

        file = open(self.location, "wb")
        pickle.dump(megadict,file)
        # json.dump(megadict, file, sort_keys=True,	indent=2)

    def load(self, loc):
        file = open(loc,'rb')
        object = pickle.load(file)
  
        self.title = object['title']
        self.dateCreated=object['dateCreated']
        self.dateEdited=object['dateEdited']
        for page in object['pages']:
            pageObj = pickle.loads(page)
            page = Page()
            page.dedictify(pageObj)
       
            self.pages.append(page)