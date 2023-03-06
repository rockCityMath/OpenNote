import pickle

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
    path, _ = QFileDialog.getSaveFileName(
        editor,
        'Save notebook as',
        '',
        'OpenNote (*.on)'
    )
    notebook.path = path
    save(editor, notebook)
   