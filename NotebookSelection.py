from modules import *
from widgets import *
from models.Notebook import Notebook

###DASHBOARD WINDOW### 

class NotebookSelection(QMainWindow):
    def __init__(self, e):
        super().__init__()
        self.e = e

    # window title and resizing
        self.setWindowTitle("OpenNote - Select Notebook")
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width * 1.5, self.screen_height * 1.5)

    # stylesheet
        with open('dashboard_styles.qss',"r") as fh:
          self.setStyleSheet(fh.read())

        toolbar = QToolBar()
        toolbar.setObjectName("dashboard_toolbar")
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    # display recent files
        recentTitle = QLabel("Recent Notebooks")
        container = QWidget()
        container.setObjectName("container")
        grid = QGridLayout()
        layout = QVBoxLayout()
        layout.addWidget(recentTitle)
        layout.addLayout(grid)
        recentTitle.setFixedHeight(30)
        grid.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(container)
        container.setLayout(layout)

        f = open('recent.txt','r')
        notebooks = f.readlines()
        row = 1
        col = 1
        for i in range(len(notebooks)):
            recentCard = QWidget()
            recentCard.setObjectName("recentCard")
            recentCard.setFixedSize(250, 250)
            recentTitle = QLabel(recentCard)
            recentTitle.setObjectName("recentTitle")
            title = notebooks[i].split('- ')
            recentTitle.setText(title[1])
            grid.addWidget(recentCard,row,col)
            if col == 4:
                col=0
                row+=1
            col+=1

    ###TOOLBAR ACTIONS###

    # title
        title = QLabel("OpenNote")
        title.setObjectName("dashboard_title")

    # create
        self.create_notebook_action = self.create_action(self, './images/svg/arrow-down.svg', "Create Notebook", "Create Notebook", False)
        self.create_notebook_action.triggered.connect(self.create_notebook)

    # load
        self.open_file_action = self.create_action(self, './images/svg/arrow-down.svg', "Load Notebook", "Load Notebook", False)
        self.open_file_action.triggered.connect(self.load_notebook)

    # add actions to toolbar
        toolbar.addWidget(title)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)
        toolbar.addActions([self.create_notebook_action, self.open_file_action])

    ###FUNCTIONS - DASHBOARD###
    # helper function to make creating actions easier (see toolbar actions)
    def create_action(self, parent, icon_path, action_name, set_status_tip, set_checkable):
        action = QAction(QIcon(icon_path), action_name, parent)
        action.setStatusTip(set_status_tip)
        action.setCheckable(set_checkable)
        return action

    # save currently open file as...
    def create_notebook(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save notebook as',
            '',
            filter = "OpenNote (*.on)"
        )
        title = os.path.basename(path)
        self.notebook = Notebook(None, title)
        self.notebook.location = path
        self.notebook.save()

        recent = self.notebook.location + '/ - ' + self.notebook.title+'\n'
        # addToRecent(recent)

        self.w = MainWindow(self.notebook, False)
        self.w.show()  
        notebookSelectionWindow.close()  

    # open file
    def load_notebook(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self, 
            caption = 'Open Notebook',
            filter = "OpenNote (*.on)"
        )
        self.notebook = Notebook.load(path)

        recent = self.notebook.location + '/ - ' + self.notebook.title+'\n'
        # addToRecent(recent)


        

        self.e.notebookSelected.emit(self.notebook)


        # self.w = MainWindow(self.notebook, True)
        # self.w.show()  
        self.close()  #Should this be in charge of closing it


# Need????
class RecentCard(QWidget):
    def __init__(self, title_loc):
        super().__init__()
        global rwidgets