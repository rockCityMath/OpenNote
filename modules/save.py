import pickle
from threading import Timer
from modules.section import store_section
from PySide6.QtWidgets import QFileDialog
from datetime import datetime
from copy import copy
import os

# Dump models.notebook.Notebook into .on file
def save(editor, notebook):

    # If user wants to save, make them choose a real filename
    if notebook.path.endswith(".ontemp"):
        saveAs(editor, notebook)

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
        old_path = copy(notebook.path)
        notebook.path = path
        editor.autosaver = Autosaver(editor, notebook)
        save(editor, notebook)

        if old_path.endswith(".ontemp"):
            os.remove(old_path) # Remove temp file when saved successfully

# Autosave the program once every n seconds if a change has been made
class Autosaver:
    saveInterval = 5 # Seconds
    enabled = True # For testing/debugging

    def __init__(self, editor, notebook):
        self.timer = None
        self.editor = editor
        self.notebook = notebook
        self.changeMade = False

    def onChangeMade(self):
        if not self.changeMade:
            self.changeMade = True
            self.timer = Timer(self.saveInterval, self.onAutosave)
            self.timer.start()

    def onAutosave(self):
        if self.enabled:
            self.changeMade = False

            if (self.notebook.path == None or self.notebook.path.endswith(".ontemp")):
                saveToTempFile(self.editor, self.notebook)
            else:
                save(self.editor, self.notebook)

    # Dont pickle these objects
    def __getstate__(self):
        return None

    def __setstate__(self):
        return None

# Autosave saves to temp file if notebook hasn't been given a real name or path
def saveToTempFile(editor, notebook):
    # Build and set file and path name
    if notebook.path == None:
        currentDatetime = datetime.now()
        tempFileName = currentDatetime.strftime("%d-%m-%Y_%H-%M-%S")
        editor.notebook.title = tempFileName
        editor.notebook.path = os.getcwd() + "\\" + tempFileName + ".ontemp"
    # Save
    store_section(editor)
    file = open(notebook.path, "wb")
    pickle.dump(notebook, file)
