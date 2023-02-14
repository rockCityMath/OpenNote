import sys, os

from modules import *
from models import *
import importlib

global PluginItems

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
    global PluginItems
    if notebookEditorWindow != None:
        notebookEditorWindow.close()

    # Add notebook to recents
    recent = notebook.location + '/ - ' + notebook.title+'\n'
    addToRecent(recent)

    # Open selected notebook in window
    notebookEditorWindow = NotebookEditor(notebook,PluginItems)
    notebookEditorWindow.show()  

## Start Application ##
if __name__ == "__main__":

    global PluginItems
    PluginItems = {}
    for filename in os.listdir("./items"):
        if filename[-3:]!=".py": continue
        className = filename[:-3]
				#begin magic
        module = importlib.__import__(f"items.{className}")
        c = getattr(getattr(module,className),className)
				#end magic
        PluginItems[className]=c

    for k in PluginItems.keys():
        print(k)
        
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
