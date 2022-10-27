from datetime import datetime 
from Page import Page
from DragItem import DragItem
from util import UniqueList

class Notebook:
	def __init__(self, name="Untitled"):
		self.name=name
		self.pages=UniqueList()#no dups
				self.location=None
		self.dateCreated=datetime.now()
		self.dateEdited=datetime.now()
   
	#not sure how it should work
	def save():
		pass

	def load():
		pass
	
#tests notebook = Notebook('page 1')

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
