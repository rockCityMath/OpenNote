from PySide6.QtWidgets import QFrame, QMenu, QWidget
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction
from Modules.Enums import WidgetType
from Modules.ObjectActions import add_object, paste_object
from Modules.Enums import TextBoxStyles

class EditorFrame(QFrame):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setStyleSheet("background-color: white;")

        # MOST SHOULD BE MODES
        self.isMultiselecting = False # If user is drawing multiselecting (specifically drawing the multiselect)
        self.isMultiObjectMoving = False # User has selected their objects
        self.isMovingObjects = False # User has clicked on an object and is dragging the selected objects
        self.multiSelectWidget = None # Draws the multiselect
        self.multiSelectStartLocalPos = None
        self.multiSelectStartGlobalPos = None
        self.selectedObjects = [] # All objects selected by multiselect
        self.firstSelectionEventPos = None # Event that started the movement (objects should move relative to this)
        self.firstSelectedObject = None
        self.randomOffset = None

    def mouseReleaseEvent(self, event):
        editor = self.editor

        if event.button() == Qt.LeftButton:

            # If finishing a multiselect
            if self.isMultiselecting:

                # Get all DraggableContainers in the selection
                for o in editor.object:

                    # Map all positions to global for correct coord checks
                    ob_tl_pos = o.mapToGlobal(QPoint(0, 0)) # Object top left corner
                    start_pos = self.multiSelectStartGlobalPos
                    end_pos = event.globalPos()

                    # If object x + width is between start and end x, and object y + height is between start and end y
                    if ob_tl_pos.x() > start_pos.x() and ob_tl_pos.x() + o.width() < end_pos.x():
                        if ob_tl_pos.y() > start_pos.y() and ob_tl_pos.y() + o.height() < end_pos.y():
                            self.selectedObjects.append(o)

                # Enter multi-object move mode
                if len(self.selectedObjects) > 0:
                    self.isMultiObjectMoving = True

                # Reset multiselecting
                self.isMultiselecting = False
                self.multiSelectWidget.hide()
                self.multiSelectWidget = None

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
        if not self.isMultiselecting:
            self.isMultiselecting = True
            self.multiSelectWidget = QWidget(self)
            self.multiSelectWidget.setStyleSheet(TextBoxStyles.INFOCUS.value)
            self.multiSelectWidget.setGeometry(event.pos().x(), event.pos().y(), 0, 0)
            self.multiSelectWidget.show()
            self.multiSelectStartLocalPos = event.pos()
            self.multiSelectStartGlobalPos = event.globalPos()

        # Resize multi-select widget on mouse every proceeding mouse movement (dragging)
        else:
            width = event.pos().x() - self.multiSelectStartLocalPos.x()
            height = event.pos().y() - self.multiSelectStartLocalPos.y()
            self.multiSelectWidget.resize(width, height)
