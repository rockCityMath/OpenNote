from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from Modules.Enums import WidgetType

class ImageWidget(QLabel):
    def __init__(self, editor, x, y, w, h, image_matrix):
        super().__init__(editor)
        self.type = WidgetType.IMAGE
        self.image_matrix = image_matrix

        # Image matrix from cv2 -> QImage -> QPixmap on this label
        bytes_per_line = 3 * w # When resizing is implemented, this may need to be calc. from matrix shape
        q_image = QImage(image_matrix.data, w, h, bytes_per_line, QImage.Format_BGR888)
        q_pixmap = QPixmap(q_image)
        self.setPixmap(q_pixmap)

        self.setGeometry(x, y, w, h)

class ImagePickleable():
    def __init__(self,name, x, y, w, h, image_matrix):
        self.name = name
        self.x = x                         
        self.y = y
        self.w = w
        self.h = h
        self.image_matrix = image_matrix   
        self.type = WidgetType.IMAGE        

