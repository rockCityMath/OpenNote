import pickle
from threading import Timer
from PySide6.QtWidgets import QFileDialog
from datetime import datetime
from copy import copy
import os

# Leaving this to take in editor in case we want to store state or something
def save(editor):

    for p in editor.notebook.pages:
        print(p.title)

    # If user wants to save, make them choose a real filename
    # if notebook.path.endswith(".ontemp"):
    #     saveAs(editor, notebook)

    editor.notebook.title = editor.notebookTitleView.toPlainText()
    if editor.notebook.path:       # If a file does not exist, call saveAs to create one
        file = open(editor.notebook.path, "wb")
        pickle.dump(editor.notebook, file)
    else:
        saveAs(editor)

def saveAs(editor): # debt: Make this open to the Saves folder
    path, accept = QFileDialog.getSaveFileName(
        editor,
        'Save notebook as',
        editor.notebook.title,
        'OpenNote (*.on)'
    )
    if accept:
        # old_path = copy(editor.notebook.path)
        editor.notebook.path = path
        editor.notebook.autosaver = Autosaver(editor) # ????
        save(editor)

        # if old_path.endswith(".ontemp"):
        #     os.remove(old_path) # Remove temp file when saved successfully

# Autosave the program once every n seconds if a change has been made
class Autosaver:
    saveInterval = 5 # Seconds
    enabled = False # For testing/debugging

    def __init__(self, editor):
        self.timer = None
        self.editor = editor
        self.notebook = editor.notebook
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
def saveToTempFile(editor):
    # Build and set file and path name
    if editor.notebook.path == None:
        currentDatetime = datetime.now()
        tempFileName = currentDatetime.strftime("%d-%m-%Y_%H-%M-%S")
        editor.notebook.title = tempFileName
        editor.notebook.path = os.getcwd() + "\\Saves\\" + tempFileName + ".ontemp" # If this doesnt work on mac, use path.join()
    # Save
    store_section(editor)
    file = open(editor.notebook.path, "wb")
    pickle.dump(editor.notebook, file)
