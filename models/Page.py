# Pages are 'child' objects of a Notebook object
# Page.section is an array of Section objects
class Page:
    def __init__(self, title):
        self.title = title
        self.section = []