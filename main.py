import sys, os

from modules import *
from models import *

def addToRecent(recent):
    f = open("recent.txt", "r")
    content = f.read()
    f.close()
    if recent not in content:
        f = open("recent.txt", "a")
        f.write(recent)
        f.close()

# When a notebook is selected (notebook selection event emits a notebook)
def onNotebookSelected(notebook):
    global notebookEditorWindow
    if notebookEditorWindow != None:
        notebookEditorWindow.close()

    # Add notebook to recents
    recent = notebook.location + '/ - ' + notebook.title+'\n'
    addToRecent(recent)

    # Open selected notebook in window
    notebookEditorWindow = NotebookEditor(notebook)
    notebookEditorWindow.show()  

## Start Application ##
if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Instantialize notebook editor window
    global notebookEditorWindow
    notebookEditorWindow = None

    # Global events (event object is imported from event model, should prob do this different)
    e.notebookSelected.connect(onNotebookSelected)

    # Show the initial notebook selection
    notebookSelectionWindow = NotebookSelectionDashboard()
    notebookSelectionWindow.show()

    sys.exit(app.exec())