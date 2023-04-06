import sys

from Models.Editor import Editor
from Modules.Load import load_most_recent_notebook

from PySide6.QtWidgets import *

if __name__ == "__main__":
    app = QApplication()

    editor = Editor()
    load_most_recent_notebook(editor)
    editor.showMaximized()

    sys.exit(app.exec())