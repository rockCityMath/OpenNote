from Modules.EditorSignals import editorSignalsInstance

class Clipboard:
    def __init__(self):
        self.copiedWidgetState = None
        self.copiedWidgetClass = None

        editorSignalsInstance.widgetCopied.connect(self.copyWidgetEvent)

    def copyWidgetEvent(self, draggableContainer):
        widget = draggableContainer.childWidget

        self.copiedWidgetClass = type(widget)
        self.copiedWidgetState = widget.__getstate__()

    def getWidgetToPaste(self):
        widgetState = self.copiedWidgetState
        widgetClass = self.copiedWidgetClass

        newWidget = widgetClass.__new__(widgetClass) # Get uninitialized instance of widget class
        newWidget.__setstate__(widgetState)          # Initialize the widget instance with its setstate method

        return newWidget
