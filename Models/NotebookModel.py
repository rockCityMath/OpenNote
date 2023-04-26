class NotebookModel:
    def __init__(self, title):
        self.path = None
        self.title = title
        self.pages = []  # PageModel[]
