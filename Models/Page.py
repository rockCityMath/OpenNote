from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class Page:
    def __init__(self, editor, title):
        self.title = title
        self.sections = []

        self.childPages: Page = []
        self.childPageTabs = QVBoxLayout()

        # Display tab in notbook - adding a page to notebook adds to editor
        self.tabWidget = QPushButton(title)
        self.tabWidget.mousePressEvent = lambda event: editor.handlePageClick(self.tabWidget, self, event)
        self.tabWidget.setObjectName(title)
        editor.page_tabs.addWidget(self.tabWidget)
        editor.page_tabs.addLayout(self.childPageTabs)
