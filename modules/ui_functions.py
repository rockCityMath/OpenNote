from main import *

class UIFunctions(QMainWindow):
    def openNotebook(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self, 
            caption = 'Open Notebook',
            filter = self.filterTypes
        )
        self.notebook = Notebook.load(path)
        recent = self.notebook.location + '/ - ' + self.notebook.title+'\n'
        addToRecent(recent)

        self.editor.setText(self.notebook.pages[0].text)
        self.update_title()
        self.update_notebook_title()

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
        recent = self.notebook.location + '/ - ' + self.notebook.title+'\n'
        addToRecent(recent)