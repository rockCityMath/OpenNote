import pickle
from threading import Timer
from PySide6.QtWidgets import QFileDialog
from datetime import datetime
import os
from Modules.EditorSignals import editorSignalsInstance

# Leaving this to take in editor in case we want to store state or something
def save(editor):

    # If user wants to save, make them choose a real filename
    # Wierd w autosaver rn, since it calls this method, but if its autosaving to .ontemp it will hit this
    # if editor.notebook.path.endswith(".ontemp"):
    #     saveAs(editor)

    editor.notebook.title = editor.notebookTitleView.toPlainText()
    if editor.notebook.path:       # If a file does not exist, call saveAs to create one
        file = open(editor.notebook.path, "wb")
        nb = editor.notebook
        print("TYPE: ", type(nb))
        pickle.dump(nb, file)
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
        old_path = str(editor.notebook.path)
        editor.notebook.path = path
        save(editor)

        if old_path.endswith(".ontemp"):
            os.remove(old_path) # Remove temp file when saved successfully

# Autosave the program once every n seconds if a change has been made
class Autosaver:
    saveInterval = 5 # Seconds
    enabled = True # For testing/debugging

    def __init__(self, editor):
        self.editor = editor
        self.notebook = editor.notebook
        self.timer = None
        self.changedSinceLastSave = False
        editorSignalsInstance.changeMade.connect(self.onChangeMade)

    def onChangeMade(self):
        print("AUTOSAVE REC CHANGES")
        if not self.changedSinceLastSave:
            self.changedSinceLastSave = True
            self.timer = Timer(self.saveInterval, self.onAutosave)
            self.timer.start()

    def onAutosave(self):
        print("SAVE FROM AUTOSAVE")
        if self.enabled:
            self.changedSinceLastSave = False

            if (self.notebook.path == None):
                print("AUTOSAVE TO TEMP FILE")
                saveToTempFile(self.editor)
            else:
                print("AUTOSAVE TO FILE")
                save(self.editor)

# Autosave saves to temp file if notebook hasn't been given a real name or path
def saveToTempFile(editor):
    # Build and set file and path name
    if editor.notebook.path == None:
        currentDatetime = datetime.now()
        tempFileName = currentDatetime.strftime("%d-%m-%Y_%H-%M-%S")
        editor.notebook.title = tempFileName
        editor.notebook.path = os.getcwd() + "\\Saves\\" + tempFileName + ".ontemp" # If this doesnt work on mac, use path.join()

    file = open(editor.notebook.path, "wb")
    pickle.dump(editor.notebook, file)
