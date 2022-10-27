

class UniqueList(collections.MutableSequence):
	def __init__(self,itr=()):
		self._list = list()
		self._map = set()
		for item in itr:
			if item in self._map:
				self._list.remove(item)
				self._list.append(item)
			else:
				self._list.append(item)
				self._map.add(item)
	
	def __len__(self):
		return len(self._list)
	
	def __contains__(self,item):
		return item in self._map

	def __getitem__(self,idx):
		return self._list[idx]

	def __setitem__(self,idx,item):
		if self._list[idx]==item: return

		if item not in self._map:
			self._list[idx]=item
			self._map.add(item)
			return

		cidx = self._list.index(item)
		self._list[cidx]=None
		self._list[idx]=item
		self._list.remove(None)
	
	def __delitem__(self,idx):
		self._map.remove(self._list[idx])
		del self._list[idx]
		
	def append(self,item):
		if item in self._list:
			self._list.remove(item)
		self._list.append(item)
		self._map.add(item)
	
	def remove(self,item):
		self._list.remove(item)
		self._map.remove(item)

	def insert(self,idx,item):
		if item not in self._map:
			self._list.insert(idx,item)
			self._map.add(item)
			return

		cidx=self._list.index(item)
		self._list[cidx]=None
		self._list.insert(idx,item)
		self._list.remove(None)
