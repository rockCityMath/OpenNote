# Sections are 'child' objects of a Page object
# Section.object is an array of below objects
class Section:
    def __init__(self, title):
        self.title = title

        self.widgets = []
