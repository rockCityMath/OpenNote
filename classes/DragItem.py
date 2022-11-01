class DragItem:
	def __init__(self,pos):
		self.pos=pos
	
	def draw(self,page):
		pass
	
	def dictify(self):
		return {"pos":self.pos}

	def dedictify(self,dict):
		self.pos=dict['pos']
		
