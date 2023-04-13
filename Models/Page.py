from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class Page:
    def __init__(self, editor, title):
        self.title = title
        self.sections = []

        # Display tab in notbook - adding a page to notebook adds to editor
        self.tabWidget = QPushButton(title)
        self.tabWidget.mousePressEvent = lambda event: editor.handlePageClick(self.tabWidget, event)
        self.tabWidget.setObjectName(title)
        editor.page_tabs.addWidget(self.tabWidget)
