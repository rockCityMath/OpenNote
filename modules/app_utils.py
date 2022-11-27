from main import *

# Helper function to make creating actions easier (see toolbar actions)
def create_action(self, parent, icon_path, action_name, set_status_tip, set_checkable):
    action = QAction(QIcon(icon_path), action_name, parent)
    action.setStatusTip(set_status_tip)
    action.setCheckable(set_checkable)
    return action

# Helper function to update window title based on open notebook
def update_title(self):
    self.setWindowTitle(self.notebook.title + " - OpenNote")

# Helper function to update notebook_title label based on open notebook
def update_notebook_title(self):
    self.notebook_title.setText(self.notebook.title)

def block_signals(self, actions, b):
    for x in actions:
        x.blockSignals(b)

def font_color_action(self):
    self.color = self.color_dialog.getColor()
    self.editor.setTextColor(self.color)
    self.pal = QPalette()
    self.pal.setColor(QPalette.Normal, QPalette.ButtonText, self.color)
    self.font_color.setPalette(self.pal)

# Helper function to update toolbar options when text editor selection is changed
def update_format(self):
    self.block_signals(self.format_actions, True)

    self.font_family.setCurrentFont(self.editor.currentFont())
    self.font_size.setCurrentText(str(int(self.editor.fontPointSize())))

    self.italic_action.setChecked(self.editor.fontItalic())
    self.underline_action.setChecked(self.editor.fontUnderline())
    self.bold_action.setChecked(self.editor.fontWeight() == QFont.bold)

    self.block_signals(self.format_actions, False)

# Helper function to show error messages
def dialog_message(self, message):
    dlg = QMessageBox(self)
    dlg.setText(message)
    dlg.show() 
