from enum import Enum

# Styles for different states of the textbox
class TextBoxStyles(Enum):
    INFOCUS = "border: 0.5px dotted rgba(0, 0, 0, .5); background-color: rgba(0, 0, 0, 0)"
    OUTFOCUS = "border: none; background-color: rgba(0, 0, 0, 0);"

class WidgetType(Enum):
    TEXT = 'text'
    IMAGE = 'image'
    TABLE = 'table'
