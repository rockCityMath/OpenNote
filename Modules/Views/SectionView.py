from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from Models.SectionModel import SectionModel

from typing import List
from functools import partial

# Page view and controller
class SectionView(QWidget):
    def __init__(self, sectionModels: List[SectionModel]):
        super(SectionView, self).__init__()

        self.sectionModels: List[SectionModel] # Reference to the current section models

        # The tabbed section widget
        self.tabs = QTabBar(self)

        # Layout that holds this view
        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tabs.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.openMenu)
        self.tabs.currentChanged.connect(self.changeSection)
        self.isLoading = False

        self.loadSections(sectionModels)
        print("BUILT SECTIONVIEW")

    def loadSections(self, sectionModels: List[SectionModel]):
        print("LOADING SECTIONS")
        self.isLoading = True

        for i in range(self.tabs.count()):
            self.tabs.removeTab(0)

        for s in sectionModels:
            addedTabIndex = self.tabs.addTab(s.title)
            self.tabs.setTabData(addedTabIndex, s)

        self.isLoading = False
        self.tabs.setCurrentIndex(0)
        self.changeSection(0)
        self.sectionModels = sectionModels  # Update the view's stored reference to the tabModels

    def openMenu(self, position: QPoint):

        clickedSectionIndex = self.tabs.tabAt(position)
        sectionModel = self.tabs.tabData(clickedSectionIndex)

        menu = QMenu()
        addSectionAction = menu.addAction(self.tr("Add Section"))
        addSectionAction.triggered.connect(partial(self.addSection, sectionModel, clickedSectionIndex))

        deleteSectionAction = menu.addAction(self.tr("Delete Section"))
        deleteSectionAction.triggered.connect(partial(self.deleteSection, sectionModel, clickedSectionIndex))

        renameSectionAction = menu.addAction(self.tr("Rename Section"))
        renameSectionAction.triggered.connect(partial(self.renameSection, sectionModel, clickedSectionIndex))

        menu.exec(self.tabs.mapToGlobal(position))

    def addSection(self, sectionModel: SectionModel, clickedSectionIndex: int):
        print("ADD TAB")

        addedSectionIndex = self.tabs.addTab("New Section")                  # Add section to UI
        self.tabs.moveTab(addedSectionIndex, clickedSectionIndex + 1)        # Move to right of right clicked section

        newSectionModel = SectionModel("New Section")                        # Create new SectionModel
        self.tabs.setTabData(addedSectionIndex, newSectionModel)             # Set new SectionModel as section data

        self.sectionModels.insert(clickedSectionIndex + 1, newSectionModel)  # Insert new SectionModel into list of section models

    def deleteSection(self, sectionModel: SectionModel, clickedSectionIndex: int):
        print("DELETE SECTION")
        self.tabs.removeTab(clickedSectionIndex)                            # Remove section from UI
        self.sectionModels.pop(clickedSectionIndex)                         # Remove section from list of section models

    def renameSection(self, sectionModel: SectionModel, clickedSectionIndex: int):
        print("RENAME SECTION")
        newName, accept = QInputDialog.getText(self, 'Change Section Title', 'Enter new title of section: ')
        if accept:
            self.tabs.setTabText(clickedSectionIndex, newName)        # Rename section in UI
            self.sectionModels[clickedSectionIndex].title = newName   # Rename section in SectionModel

    def changeSection(self, sectionIndex: int):
        if self.isLoading:  # Dont change sections while loading in new tabs
            return

        sectionModel = self.tabs.tabData(sectionIndex)
        print("NEW SECTION :", sectionModel.title)

        sectionModel.showWidgets()


