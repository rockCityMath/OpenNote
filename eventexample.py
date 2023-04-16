from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys

class PageModel:
    def __init__(self, name: str, sections: str):
        self.name = name
        self.sections = sections

class SectionModel:
    def __init__(self, name: str, pages: str):
        self.name = name
        self.pages = pages

class NotebookEventHandler(QObject):
    changePage = Signal(PageModel)
    changeSection = Signal(SectionModel)

NEH = NotebookEventHandler()

class PageView(QWidget):
    def __init__(self):
        super().__init__()
        self.neh = NEH
        self.setWindowTitle("PageView")
        self.neh.changePage.connect(self.changePage)

    def mousePressEvent(self, event):
        self.neh.changePage.emit(PageModel("page 1", "page with sections"))

class SectionView(QWidget):
    def __init__(self):
        super().__init__()
        self.neh = NEH
        self.neh.changePage.connect(self.changePage)
        self.setWindowTitle("SectionView")

    def changePage(self, page: PageModel):
        print(page.name)

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('Emit signal')
        self.pageView = PageView()
        self.sectionView = SectionView()
        self.pageView.show()
        self.sectionView.show()
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
