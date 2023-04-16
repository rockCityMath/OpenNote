from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class PageModel:
    def __init__(self, name: str, sections: str):
        self.name = name
        self.sections = sections

class SectionModel:
    def __init__(self, name: str, pages: str):
        self.name = name
        self.pages = pages

class NotebookEventHandler(QObject):

    closeApp = pyqtSignal()
    changePage = pyqtSignal(PageModel)
    changeSection = pyqtSignal(SectionModel)


class PageView(QWidget):
    def __init__(self):
        super().__init__()

class SectionView(QWidget):
    def __init__(self):
        super().__init__()

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.c = Communicate()
        self.c.closeApp.connect(self.closeEvent)

        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('Emit signal')
        self.show()

    def closeEvent(self, event):
        print(event)

    def mousePressEvent(self, event):

        self.c.closeApp.emit(event)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
