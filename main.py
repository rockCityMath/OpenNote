import sys

from screens.editor import Editor

from PySide6.QtWidgets import *

if __name__ == "__main__":
    app = QApplication()

    editor = Editor()
    editor.show()

    sys.exit(app.exec())