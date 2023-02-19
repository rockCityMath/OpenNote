from modules import *
from models import *

def openNotebook(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self, 
            caption = 'Open Notebook',
            filter = 'OpenNote (*.on)'
        )
        self.notebook = Notebook.load(path)
        recent = self.notebook.location + '/ - ' + self.notebook.title+'\n'
        # addToRecent(recent)

        #self.frame.textedit.setText(self.notebook.pages[0].text)
        self.setWindowTitle(self.notebook.title + " - OpenNote")
        self.notebookTitle.setText(self.notebook.title)

        e.notebookSelected.emit(self.notebook)

def saveNotebook(self):
    self.notebook.save()

def saveNotebookAs(self):
    path, _ = QFileDialog.getSaveFileName(
        self,
        'Save notebook as',
        '',
        self.filterTypes
    )
    self.notebook.save()