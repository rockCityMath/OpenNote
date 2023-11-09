from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]


class LinkWidget(QLabel):
    def __init__(self, x, y, l, d, w = 15, h = 30):
        super().__init__()

        self.setGeometry(x, y, w, h) 
        self.setStyleSheet('font-size: 20px')
        self.setOpenExternalLinks(True)


        self.setText(f'<a href="{l}">{d}</a>')
        #self.setParent(parent)

    @staticmethod
    def new(clickPos: QPoint):
        dialog = LinkDialog()

        if dialog.exec_() == QDialog.Accepted:
            link_address, display_text = dialog.get_link_data()

        print(link_address)

        return LinkWidget(clickPos.x(), clickPos.y(), link_address, display_text)

    def __getstate__(self):
        data = {}

        data['geometry'] = self.parentWidget().geometry()
        #data['content'] = self.toHtml()
        data['stylesheet'] = self.styleSheet()
        return data

    def __setstate__(self, data):
        self.__init__(data['geometry'].x(), data['geometry'].y(), data['geometry'].width(), data['geometry'].height(), data['content'])
        self.setStyleSheet(data['stylesheet'])
    
class LinkDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Link")
        layout = QVBoxLayout()

        self.link_label = QLabel("Link Address:")
        self.link_textbox = QLineEdit()
        self.display_label = QLabel("Display Text:")
        self.display_textbox = QLineEdit()

        layout.addWidget(self.link_label)
        layout.addWidget(self.link_textbox)
        layout.addWidget(self.display_label)
        layout.addWidget(self.display_textbox)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def get_link_data(self):
        link_address = self.link_textbox.text()
        display_text = self.display_textbox.text()
        return link_address, display_text



