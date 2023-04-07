from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from Modules.Enums import WidgetType

class ImageWidget(QLabel):
    def __init__(self, editor, x, y, w, h, image_matrix):
        super().__init__(editor)
        self.type = WidgetType.IMAGE
        self.image_matrix = image_matrix
        self.w = w
        self.h = h

        # Image matrix from cv2 -> QImage -> QPixmap on this label
        matrix_height, matrix_width, _ = image_matrix.shape # Calc dimensions from real image matrix, not the current widget geometry
        bytes_per_line = 3 * matrix_width
        q_image = QImage(image_matrix.data, matrix_width, matrix_height, bytes_per_line, QImage.Format_BGR888)
        self.q_pixmap = QPixmap(q_image)
        self.setPixmap(self.q_pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)) # Scale to widget geometry

        self.setGeometry(x, y, w, h)
    
    # Handle resize
    def newGeometryEvent(self, e, parent):
        new_w = e.width()
        new_h = e.height()
        if (self.w != new_w) or (self.h != new_h): # Not exactly sure how object's width and height attribute gets updated but this works 
            self.setPixmap(self.q_pixmap.scaled(new_w, new_h, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            pixmap_rect = self.pixmap().rect()
            w = pixmap_rect.width()
            h = pixmap_rect.height()
            parent.resize(w, h) # Set container to the size of the new scaled pixmap 
            

class ImagePickleable():
    def __init__(self,name, x, y, w, h, image_matrix):
        self.name = name
        self.x = x                         
        self.y = y
        self.w = w
        self.h = h
        self.image_matrix = image_matrix   
        self.type = WidgetType.IMAGE        

