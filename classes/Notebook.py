from datetime import datetime 
from Page import Page
from DragItem import DragItem
class Notebook:
    def __init__(self, name):
        self._name=name
        self._pages={}#accepts page classes
        self._dateCreated=datetime.now()
        self._dateEdited=''
   
    #adds page to a dict
    def addPage(self, page:Page): ##adds page object
        self._pages[page.getName()]=page
        self._dateEdited=datetime.now()
    
    def renameNotebook(self,newName):
        self._name=newName
        return self._name
    
    #deletes page from dict
    def delPage(self, pageName):
        if pageName in self._pages:
            del self._pages[pageName]
            self._dateEdited=datetime.now()
            return 0
        return -1
    
    #lists all pages
    def listPages(self):
        return self._pages

    #gets createdDate
    def getDateCreated(self):
        return self._dateCreated
    def getDateEdited(self):
        return self._dateEdited
    
    #not sure how it should work
    def save():
        pass
    def load():
        pass
    
#tests
notebook = Notebook('page 1')

#adding pages and testing them
print('adding pages and testing them----------')
notebook.addPage(Page('page_1'))
notebook.addPage(Page('page_2'))
print(notebook.listPages())
print()

#adding adding draggable items
print('adding adding draggable items to page-----------')
pages = notebook.listPages()
pages['page_1'].addItem(DragItem(1))
pages['page_1'].addItem(DragItem(2))
pages['page_1'].addItem(DragItem(3))
print(pages['page_1'].listItems())
print()


#deleting page and testing it
print('deleting page and testing it-------------')
notebook.delPage('page_1')
print(notebook.listPages())
print()