from modules import *
from models import *

# Helper function to make creating actions easier (see toolbar actions)
def createAction(parent, icon_path, action_name, set_status_tip, set_checkable):
    action = QAction(QIcon(icon_path), action_name, parent)
    action.setStatusTip(set_status_tip)
    action.setCheckable(set_checkable)
    return action

# Helper function to update window title based on open notebook
def updateTitle(self):
    self.setWindowTitle(self.notebook.title + " - OpenNote")

# Helper function to update notebook_title label based on open notebook
def updateNotebookTitle(self):
    self.notebook_title.setText(self.notebook.title)