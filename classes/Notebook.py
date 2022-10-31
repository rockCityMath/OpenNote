from datetime import datetime 
import json
from classes.util import UniqueList
class Notebook:
	def __init__(self, title="Untitled"):
		self.title=title
		self.pages=UniqueList()#no dups
		self.location=None
		self.dateCreated=datetime.now()
		self.dateEdited=datetime.now()
   
	#not sure how it should work
	#leaving undefined for now
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
     

