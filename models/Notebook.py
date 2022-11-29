from datetime import datetime
from models.Page import Page
from models.DragItem import DragItem
from models.util import UniqueList
import pickle

class Notebook:
    def __init__(self, text, title):
        self.title = title
        self.pages = UniqueList()  # no dups
        self.location = None
        self.dateCreated = datetime.now()
        self.dateEdited = datetime.now()

    def save(self):
        file = open(self.location, "wb")
        pickle.dump(self, file)
        
    @staticmethod
    def load(loc):
        file = open(loc,'rb')
        return pickle.load(file)       