from datetime import datetime 
from DragItem import DragItem
from util import UniqueList

class Page:
	def __init__(self,title="Untitled"):
		self.title=title
		self.dateCreated=datetime.now()
		
		self.items = set()
		self.parent = None
		self.children=UniqueList()

	def setChild(self,page):
		#IMO we should just model this stuff at the UI level. add an indent field that just indents the page name
		#this breaks in any complex case
		if page.parent!=None:
			page.parent.children.remove(page)
		page.parent=self
		self.children.append(page)
			
	
	def dictify(self):
		megadict = {}
		megadict['title']=self.title
		megadict['dateCreated']=self.dateCreated.isoformat()
		megadict['items']=[]
		for item in self.items:
			megadict['items'].append(item.dictify())

		megadict['children']=[]
		for child in self.children:
			megadict['children'].append(child.dictify())
		
		return megadict
