from Widgets.Textbox import TextboxWidget
from Models.DraggableContainer import DraggableContainer

class SectionModel:
    def __init__(self, title: str):
        self.title = title
        self.widgets = [] # DraggableContainer[]


    def showWidgets(self):
        print("SectionModel.showWidgets()")
        # for widget in self.widgets:
        #     widget.show()
