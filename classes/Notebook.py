from datetime import datetime
import json
from classes.util import UniqueList
from classes.Page import Page
class Notebook:
    def __init__(self, title="Untitled"):
        self.title = title
        self.pages = UniqueList()  # no dups
        self.location = '.'
        self.dateCreated = datetime.now()
        self.dateEdited = datetime.now()
    def save(self):
        megadict = {}
        megadict['title']=self.title
        megadict['pages']=[]
        megadict['dateCreated']=self.dateCreated.isoformat()
        for page in self.pages:
            if page.parent!=None: continue
            megadict['pages'].append(page.dictify())
        megadict['dateEdited']=datetime.now().isoformat()
        file = open(self.location,"w+")
        json.dump(megadict,file, sort_keys=True,indent=2)
  
    def load(self,loc):
        self.location=loc
        file = open(loc,'r')
        s = file.read()
        data = json.loads(s)
        self.title = data['title']
        arr=[]
        for page in data['pages']:
            arr.append(Page().dedictify(page))    
        self.pages = arr
        self.dateCreated = data['dateCreated']
        self.dateEdited = data ['dateEdited']