from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from Modules.Enums import WidgetType

import random
import cv2

class ImageWidget(QLabel):
    def __init__(self, x, y, w, h, image_matrix):
        super().__init__()
        self.image_matrix = image_matrix
        self.w = w
        self.h = h

        # Image matrix from cv2 -> QImage -> QPixmap on this label
        matrix_height, matrix_width, _ = image_matrix.shape # Calc dimensions from real image matrix, not the current widget geometry
        bytes_per_line = 3 * matrix_width
        q_image = QImage(image_matrix.data, matrix_width, matrix_height, bytes_per_line, QImage.Format_BGR888)
        self.q_pixmap = QPixmap(q_image)
        self.setPixmap(self.q_pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)) # Scale to widget geometry

        self.setGeometry(x, y, w, h) # this should get fixed
        self.persistantGeometry = self.geometry()

    # Handle resize
    def newGeometryEvent(self, newGeometry):
        new_w = newGeometry.width()
        new_h = newGeometry.height()
        if (self.w != new_w) or (self.h != new_h): # Not exactly sure how object's width and height attribute gets updated but this works
            self.setPixmap(self.q_pixmap.scaled(new_w, new_h, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            pixmap_rect = self.pixmap().rect()
            w = pixmap_rect.width()
            h = pixmap_rect.height()
            # parent.resize(w, h) # Set container to the size of the new scaled pixmap

        self.persistantGeometry = newGeometry

    @staticmethod
    def new(clickPos):

        # Get path from user
        path, _ = QFileDialog.getOpenFileName(QWidget(), 'Add Image')
        if path == "": return

        # Get image size
        image_matrix = cv2.imread(path)
        h, w, _ = image_matrix.shape

        # Create image and add to notebook
        h, w, _ = image_matrix.shape
        image = ImageWidget(clickPos.x(), clickPos.y(), w, h, image_matrix) # Note: the editorframe will apply pos based on event

        return image

    @staticmethod # Special staticmethod that screensnip uses
    def newFromMatrix(clickPos, imageMatrix):
        h, w, _ = imageMatrix.shape
        image = ImageWidget(clickPos.x(), clickPos.y(), w, h, imageMatrix)

        return image

    def __getstate__(self):
        state = {}
        state['geometry'] = self.persistantGeometry
        state['image_matrix'] = self.image_matrix
        return state

    def __setstate__(self, state):
        self.__init__(state['geometry'].x(), state['geometry'].y(), state['geometry'].width(), state['geometry'].height(), state['image_matrix'])
