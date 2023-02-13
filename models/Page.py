from datetime import datetime 
from models.util import UniqueList
class Page:
	def __init__(self,title="Untitled"):
		self.title=title
		self.dateCreated=datetime.now()
		
		self.items = set()
		self.parent = None
		self.children=UniqueList()

		self.text = "" # temporary, remove when items (drag and drop) is implemented
		self.textedits = [] # all the text boxes (TextBoxDraggable)

	def setChild(self,page):
		#IMO we should just model this stuff at the UI level. add an indent field that just indents the page name
		#this breaks in any complex case
		if page.parent!=None:
			page.parent.children.remove(page)
		page.parent=self
		self.children.append(page)
  
