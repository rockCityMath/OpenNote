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
	#leaving undefined for now
	def save():
		pass

	def load():
		pass
