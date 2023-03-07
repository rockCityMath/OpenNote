import pickle
from threading import Timer

from modules.section import store_section

from PySide6.QtWidgets import QFileDialog

# Dump models.notebook.Notebook into .on file
def save(editor, notebook):
    editor.notebook.title = editor.notebook_title.toPlainText()
    store_section(editor)   # Add objects from user's current section to models.notebook.Notebook
    if notebook.path:       # If a file does not exist, call saveAs to create one
        file = open(notebook.path, "wb")
        pickle.dump(notebook, file)
    else:
        saveAs(editor, notebook)

def saveAs(editor, notebook):
    path, accept = QFileDialog.getSaveFileName(
        editor,
        'Save notebook as',
        editor.notebook.title,
        'OpenNote (*.on)'
    )
    if accept:
        notebook.path = path
        editor.autosaver = Autosaver(editor, notebook)
        save(editor, notebook)

# Autosave the program once every n seconds if a change has been made
class Autosaver:
    saveInterval = 10 # Seconds

    def __init__(self, editor, notebook):
        self.timer = None
        self.editor = editor
        self.notebook = notebook
        self.changeMade = False

    def onChangeMade(self):        
        if((not self.changeMade) and (self.notebook.path != None)): 
            self.changeMade = True
            self.timer = Timer(self.saveInterval, self.onAutosave)
            self.timer.start()

    def onAutosave(self):
        self.changeMade = False
        save(self.editor, self.notebook)

    # Dont pickle these objects
    def __getstate__(self):
        return None
    
    def __setstate__(self):
        return None 
   