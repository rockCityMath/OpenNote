import numpy as np
import cv2
from PIL import ImageGrab
from sys import platform

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# General widget from https://github.com/harupy/snipping-tool <3
class SnippingWidget(QWidget):
    is_snipping = False

    def __init__(self):
        super(SnippingWidget, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.parent = None
        self.screen = QApplication.instance().primaryScreen()
        self.setGeometry(0, 0, self.screen.size().width(), self.screen.size().height())
        self.begin = self.end = QPoint()
        self.onSnippingCompleted = None
        self.event_pos = None

    def start(self, event_pos):
        print("SnippingWidget.start")
        SnippingWidget.is_snipping = True
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        self.event_pos = event_pos
        self.show()
        print("SnippingWidget.start done")

    def paintEvent(self, event):
        qp = QPainter(self)
        if SnippingWidget.is_snipping:
            brush_color = (128, 128, 255, 100)
            lw = 3
            qp.setPen(QPen(QColor('black'), lw))
            qp.setBrush(QColor(*brush_color))
            rect = QRectF(self.begin, self.end)
            qp.drawRect(rect)

    def mousePressEvent(self, event):
        try:
            self.begin = event.pos()
            self.end = self.begin
            self.update()
        except Exception as e:
            print(f"Error handling mouse press event: {e}")

    def mouseMoveEvent(self, event):
        try:
            self.end = event.pos()
            self.update()
        except Exception as e:
            print(f"Error handling mouse move event: {e}")

    def mouseReleaseEvent(self, event):
        SnippingWidget.is_snipping = False
        QApplication.restoreOverrideCursor()
        x1, y1, x2, y2 = self.getSnipCoordinates()

        self.repaint()
        QApplication.processEvents()
        
        try:
            if platform == "darwin":
                img = ImageGrab.grab(bbox=( (x1 ) * 2, (y1 + 55 ) * 2, (x2 ) * 2, (y2 + 55) * 2))
            else:
                img = ImageGrab.grab(bbox=(x1 + 10, y1 + 30, x2 + 10, y2 + 40))
        except Exception as e:
            print(f"Error grabbing screenshot: {e}")
            img = None

        try:
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        except:
            print(f"Error converting screenshot to NumPy array: {e}")
            img = None

        if self.onSnippingCompleted is not None:
            self.onSnippingCompleted(img)

        self.close()

    def getSnipCoordinates(self):
        try:
            x1 = min(self.begin.x(), self.end.x())
            y1 = min(self.begin.y(), self.end.y())
            x2 = max(self.begin.x(), self.end.x())
            y2 = max(self.begin.y(), self.end.y())
            return x1, y1, x2, y2
        except Exception as e:
            print(f"Error getting snip coordinates {e}")
            return 0, 0, 0, 0    