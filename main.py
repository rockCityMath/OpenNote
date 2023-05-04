import sys
import os

from Models.Editor import Editor
from Modules.Load import load_most_recent_notebook

from PySide6.QtWidgets import *

# Import the PluginWidgets directory here so the app can load/save them
pluginDirectory = os.path.join(os.path.dirname(os.getcwd()), "PluginWidgets")
sys.path.append(pluginDirectory)

if __name__ == "__main__":
    app = QApplication()

    editor = Editor()
    load_most_recent_notebook(editor)

    editor.showMaximized()

    sys.exit(app.exec())
