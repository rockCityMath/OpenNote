from datetime import datetime 
# from DragItem import DragItem
class Page:
    def __init__(self,title):
        self._title=title
        self._dateCreated=datetime.now()
        self._dateEdited=''
        
        self._items = {} #hashmap where key is uid and value is DraiItem object
        self._parentName='' #parent uid
        self._childNames=[] #array of strings of child uids
    
    
    def listItems(self):
        return self._items
    
    def addItem(self, item):
        self._items[item.getUid()]=item
        self._dateEdited=datetime.now()
        return 0
        
    def remove(self, itemId):
        if itemId in self._items:
            del self._items[itemId]
            self._dateEdited=datetime.now()
            return 0
        else:
            return -1
        
    def getName(self):
        return self._title
        
    def setParent(self, parent):
        self._parentName=parent
        
    #getParent name or parent object?
    def getParent(self):
        return self._parentName

    def addChild(self, child):
        self._childNames.append(child)   
             
    def getChildren(self):
        return self._childNames

    #do we need them?
    def save(self):
        pass
    def load(self):
        pass
    
