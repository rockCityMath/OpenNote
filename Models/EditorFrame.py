from PySide6.QtWidgets import QFrame, QMenu, QWidget
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction
from Modules.Enums import WidgetType
from Modules.ObjectActions import add_object, paste_object
from Modules.Enums import TextBoxStyles
from Modules.Multiselect import Multiselector, MultiselectMode

class EditorFrame(QFrame):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setStyleSheet("background-color: white;")
        self.multiselector = Multiselector(self)

    def mouseReleaseEvent(self, event):
        editor = self.editor

        if event.button() == Qt.LeftButton:
            if self.multiselector.mode == MultiselectMode.IS_DRAWING_AREA:
                self.multiselector.finishDrawingArea(event)

            # If clicking to add text
            else:
                o = len(editor.object) - 1
                if len(editor.object) > 0:
                    if editor.notebook.page[editor.page].section[editor.section].object[o].type == WidgetType.TEXT:
                        if editor.object[o].childWidget.toPlainText() == '':
                            editor.object[o].deleteLater()
                            editor.object.pop(o)
                            editor.notebook.page[editor.page].section[editor.section].object.pop(o)
                            editor.autosaver.onChangeMade()
                add_object(editor, event, WidgetType.TEXT)
                editor.object[len(editor.object) - 1].childWidget.setFocus()

    def mousePressEvent(self, event):
        editor = self.editor

        # Open context menu on right click
        if event.buttons() == Qt.RightButton:
            editor.setFocus()
            if editor.section > -1:
                frame_menu = QMenu(editor)

                add_image = QAction("Add Image", editor)
                add_image.triggered.connect(lambda: add_object(editor, event, WidgetType.IMAGE))
                frame_menu.addAction(add_image)

                add_table = QAction("Add Table", editor)
                add_table.triggered.connect(lambda: add_object(editor, event, WidgetType.TABLE))
                frame_menu.addAction(add_table)

                paste = QAction("Paste", editor)
                paste.triggered.connect(lambda: paste_object(editor, event))
                frame_menu.addAction(paste)

                take_screensnip = QAction("Snip Screen", editor)
                take_screensnip.triggered.connect(lambda: editor.snipArea({'x': event.pos().x(), 'y': event.pos().y()}))
                frame_menu.addAction(take_screensnip)

                frame_menu.exec(event.globalPos())

    def mouseMoveEvent(self, event): # This event is only called after clicking down on the frame and dragging

        # Set up multi-select on first move of mouse drag | Only supporting top-left to bottom-right multiselecting rn
        if self.multiselector.mode != MultiselectMode.IS_DRAWING_AREA:
            self.multiselector.beginDrawingArea(event)

        # Resize multi-select widget on mouse every proceeding mouse movement (dragging)
        else:
            self.multiselector.continueDrawingArea(event)
