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
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.parent = None
        self.screen = QApplication.instance().primaryScreen()
        self.setGeometry(0, 0, self.screen.size().width(), self.screen.size().height())
        self.begin = QPoint()
        self.end = QPoint()
        self.onSnippingCompleted = None
        self.event_pos = None

    def start(self, event_pos):
        print("SnippingWidget.start")
        SnippingWidget.is_snipping = True
        self.setWindowOpacity(0.3)
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        self.event_pos = event_pos
        self.show()
        print("SnippingWidget.start done")

    def paintEvent(self, event):
        if SnippingWidget.is_snipping:
            brush_color = (128, 128, 255, 100)
            lw = 3
            opacity = 0.3
        else:
            self.begin = QPoint()
            self.end = QPoint()
            brush_color = (0, 0, 0, 0)
            lw = 0
            opacity = 0

        self.setWindowOpacity(opacity)
        qp = QPainter(self)
        qp.setPen(QPen(QColor('black'), lw))
        qp.setBrush(QColor(*brush_color))
        rect = QRectF(self.begin, self.end)
        qp.drawRect(rect)

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        SnippingWidget.is_snipping = False
        QApplication.restoreOverrideCursor()
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        self.repaint()
        QApplication.processEvents()

        if platform == "darwin":
            img = ImageGrab.grab(bbox=( (x1 ) * 2, (y1 + 55 ) * 2, (x2 ) * 2, (y2 + 55) * 2))
        else:
            img = ImageGrab.grab(bbox=(x1 + 10, y1 + 30, x2 + 10, y2 + 40))



        try:
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        except:
            img = None

        if self.onSnippingCompleted is not None:
            self.onSnippingCompleted(img)

        self.close()
