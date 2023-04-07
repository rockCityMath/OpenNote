class Notebook:
    def __init__(self, title):
        self.path = None
        self.title = title
        self.page = []

# I'm leaving this because it's gonna be kinda how plugins work 
# Want to create a new Object to be used in the editor?
# Add a class here with params to create a new savable object
# Add a class in models.object.py to create a widget to be used in the editor
# Add a case to modules.object.add_object and modules.object.build_object
# Add a case to modules.section.store_section
