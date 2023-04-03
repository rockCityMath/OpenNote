# There classes are what is saved by Pickle

# Notebook is a 'parent' object to Pages
# Notebook.page is an array of Page objects
class Notebook:
    def __init__(self, title):
        self.path = None
        self.title = title
        self.page = []

# Pages are 'child' objects of a Notebook object
# Page.section is an array of Section objects
class Page:
    def __init__(self, title):
        self.title = title
        self.section = []

# Sections are 'child' objects of a Page object
# Section.object is an array of below objects
class Section:
    def __init__(self, title):
        self.title = title
        self.object = []

class Text:
    def __init__(self,name, x, y, w, h, t):
        self.name=name
        self.x = x          # Stores geometry of models.object.TextBox widget
        self.y = y
        self.w = w
        self.h = h
        self.text = t    # Stores html of models.object.TextBox widget
        self.type = 'text'  # Type for modules.object.build_object
class Table:
    def __init__(self,name, x, y, w, h, rows, cols):
        self.name=name
        self.x = x          # Stores geometry of models.object.TextBox widget
        self.y = y
        self.w = w
        self.h = h
        self.type = 'table'  # Type for modules.object.build_object 
        self.rows = rows
        self.cols = cols
class Image:
    def __init__(self,name, x, y, w, h, path):
        self.name = name
        self.x = x          # Geometry of models.object.ImageObj widget
        self.y = y
        self.w = w
        self.h = h
        self.path = path    # Image path of models.object.ImageObj widget
        self.type = 'image' # Type for modules.object.build_object



# Want to create a new Object to be used in the editor?
# Add a class here with params to create a new savable object
# Add a class in models.object.py to create a widget to be used in the editor
# Add a case to modules.object.add_object and modules.object.build_object
# Add a case to modules.section.store_section
