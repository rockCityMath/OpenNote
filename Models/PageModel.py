import uuid

class PageModel:
    def __init__(self, title, parentUuid = 0):
        self.title = title
        self.parentUuid = parentUuid
        self.sections = []
        self.uuid = uuid.uuid4()

    @staticmethod
    def newRootPage():
        rootPage = PageModel("Notebook Pages")
        rootPage.uuid = 0
        return rootPage
