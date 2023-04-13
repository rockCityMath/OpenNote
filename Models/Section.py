# Sections are 'child' objects of a Page object
# Section.object is an array of below objects
class Section:
    def __init__(self, title):
        self.title = title

        # NEW: Changed this to objects
        self.widgets = []
