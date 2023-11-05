from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

import os
import importlib
import sys

from Modules.Multiselect import Multiselector, MultiselectMode
from Models.DraggableContainer import DraggableContainer
from Widgets.Textbox import TextboxWidget
from Modules.EditorSignals import editorSignalsInstance
from Widgets.Image import ImageWidget
from Modules.Screensnip import SnippingWidget
from Widgets.Table import *
from Modules.Clipboard import Clipboard
from Modules.Undo import UndoHandler
from Widgets.Link import LinkWidget
from Widgets.Link import LinkDialog



# Handles all widget display (could be called widget view, but so could draggablecontainer)
class EditorFrameView(QWidget):

    def __init__(self, editor):
        super(EditorFrameView, self).__init__()

        self.editor = editor # Store reference to the editor (QMainWindow)
        self.editorFrame = QFrame(editor)
        self.editorFrame.setStyleSheet("background-color: white;")

        # Layout for the editor frame
        layout = QVBoxLayout(self)
        layout.addWidget(self.editorFrame)
        layout.setContentsMargins(0, 0, 0, 0)

        editorSignalsInstance.sectionChanged.connect(self.sectionChangedEvent)
        editorSignalsInstance.widgetShouldLoad.connect(self.loadWidgetEvent)
        editorSignalsInstance.widgetRemoved.connect(self.removeWidgetEvent)
        editorSignalsInstance.widgetCut.connect(self.cutWidgetEvent)

        # Modularized functionality for the editorFrame and its widgets
        self.clipboard = Clipboard()
        self.undoHandler = UndoHandler()
        self.multiselector = Multiselector(self)

        self.installEventFilter(self.multiselector)

        # Undo setup
        #self.shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        #self.shortcut.setContext(Qt.ApplicationShortcut)
        #self.shortcut.activated.connect(self.triggerUndo)

        print("BUILT FRAMEVIEW")
        
    def triggerUndo(self):
        print("triggerUndo Called")
        self.undoHandler.undo
        self.undoHandler.undoWidgetDelete.connect(self.undoWidgetDeleteEvent) 

    def pasteWidget(self, clickPos):
        widgetOnClipboard = self.clipboard.getWidgetToPaste()

        dc = DraggableContainer(widgetOnClipboard, self)
        self.undoHandler.pushCreate(dc)
        editorSignalsInstance.widgetAdded.emit(dc)  # Notify section that widget was added
        editorSignalsInstance.changeMade.emit()
        dc.move(clickPos.x(), clickPos.y())
        dc.show()

    def snipScreen(self, clickPos):
        def onSnippingCompleted(imageMatrix):            # Called after screensnipper gets image
            self.editor.setWindowState(Qt.WindowActive)
            self.editor.showMaximized()
            if imageMatrix is None:
                return

            widgetModel = ImageWidget.newFromMatrix(clickPos, imageMatrix)
            dc = DraggableContainer(widgetModel, self)
            self.undoHandler.pushCreate(dc)
            editorSignalsInstance.widgetAdded.emit(dc)   # Notify the current section and editorFrame that a widget was added
            dc.show()

        # Begin screensnip
        self.editor.setWindowState(Qt.WindowMinimized)
        self.snippingWidget = SnippingWidget()
        self.snippingWidget.onSnippingCompleted = onSnippingCompleted
        self.snippingWidget.start(clickPos)

    def newWidgetOnSection(self, widgetClass, clickPos):
        print("ADDWIDGET: ", widgetClass)
        try:
            widget = widgetClass.new(clickPos)          # All widget classes implement .new() static method
            dc = DraggableContainer(widget, self)
            dc.show()

            self.undoHandler.pushCreate(dc)             # Push to undo stack
            editorSignalsInstance.widgetAdded.emit(dc)  # Notify the current section that a widget was added
            editorSignalsInstance.changeMade.emit()
            dc.mouseDoubleClickEvent(None)              # Enter the child widget after adding

        except Exception as e:
            print("Error adding widget: ", e)

    # When the DC geometry is changed, tell the undoHandler
    def newGeometryOnDCEvent(self, dc):
        self.undoHandler.pushGeometryChange(dc, dc.previousGeometry)
        editorSignalsInstance.changeMade.emit()

    # Special case for adding a widget by undoing a delete, since position is already set
    def undoWidgetDeleteEvent(self, widget):
        print("UNDO DELETE EVENT")
        try:
            dc = DraggableContainer(widget, self)
            dc.show()
            editorSignalsInstance.widgetAdded.emit(dc)  # Notify the current section that a widget was added

        except Exception as e:
            print("Error adding widget: ", e)

    def removeWidgetEvent(self, draggableContainer):
        self.undoHandler.pushDelete(draggableContainer)
        editorSignalsInstance.changeMade.emit()
        draggableContainer.deleteLater()

    def cutWidgetEvent(self, draggableContainer):
        editorSignalsInstance.widgetCopied.emit(draggableContainer)
        editorSignalsInstance.widgetRemoved.emit(draggableContainer)

    # Loading a preexisting (saved) widget into the frame inside a DraggableContainer
    # Then add that DC instance reference to the sectionModel's widgets[] for runtime
    def loadWidgetEvent(self, widgetModel, sectionModel):
        dc = DraggableContainer(widgetModel, self)
        sectionModel.widgets.append(dc)
        print("LOADED CONTENT: ", widgetModel)

    def sectionChangedEvent(self, sectionModel):
        print("FRAME: NEW SECTION TITLE: " + sectionModel.title)

        # Hide all old widgets
        for c in self.children():
            if isinstance(c, DraggableContainer):
                print(c)
                c.hide()

        # Show all new widgets
        for widget in sectionModel.widgets:
            print(widget)
            widget.show()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:

            # If releasing mouse after drawing multiselect area
            if self.multiselector.mode == MultiselectMode.IS_DRAWING_AREA:
                self.multiselector.finishDrawingArea(event)

            # Releasing the mouse after clicking to add text
            else:
                print("CREATE DRAGGABLE CONTAINER")
                self.newWidgetOnSection(TextboxWidget, event.pos())

    def mousePressEvent(self, event):
        print("EDITORFRAME MOUSEPRESS")
        editor = self.editor

        # Open context menu on right click
        if event.buttons() == Qt.RightButton:
            frame_menu = QMenu(self)

            paste = QAction("Paste", editor)
            paste.triggered.connect(lambda: self.pasteWidget(event.pos()))
            frame_menu.addAction(paste)

            add_image = QAction("Add Image", self)
            add_image.triggered.connect(lambda: self.newWidgetOnSection(ImageWidget, event.pos()))
            frame_menu.addAction(add_image)

            add_table = QAction("Add Table", editor)
            add_table.triggered.connect(lambda: self.newWidgetOnSection(TableWidget, event.pos()))
            #add_table.triggered.connect(self.show_table_popup)
            frame_menu.addAction(add_table)

            take_screensnip = QAction("Snip Screen", editor)
            take_screensnip.triggered.connect(lambda: self.snipScreen(event.pos()))
            frame_menu.addAction(take_screensnip)

            add_custom_widget = QAction("Add Custom Widget", editor)
            add_custom_widget.triggered.connect(lambda: self.addCustomWidget(event))
            frame_menu.addAction(add_custom_widget)

            insert_Link = QAction("Insert Link", editor)
            insert_Link.triggered.connect(lambda: self.newWidgetOnSection(LinkWidget,event.pos()))
            frame_menu.addAction(insert_Link)

            frame_menu.exec(event.globalPos())

    def toolbar_table(self):
        print("toolbar_table pressed")
        clickPos = QPoint(0, 0)
        self.newWidgetOnSection(TableWidget, clickPos)
        
    def toolbar_hyperlink(self):
        print("toolbar_hyperlink pressed")
        clickPos = QPoint(0, 0)
        self.newWidgetOnSection(LinkWidget, clickPos)

    def addCustomWidget(self, e):
        def getCustomWidgets():
            customWidgets = {} # dict where entries are {name: class}

            # Check for files ending in .py, import them, and add their attribtues to the dict
            # Should add checks that the plugin implements required methods
            pluginDirectory = os.path.join(os.path.dirname(os.getcwd()), "PluginWidgets")

            for filename in os.listdir(pluginDirectory):
                if filename[-3:]!=".py": continue
                className = filename[:-3]

                module = importlib.__import__(f"{className}")

                c = getattr(module,className)
                customWidgets[className]=c

            return customWidgets.items()

        pluginMenu = QMenu(self)

        for customWidget in getCustomWidgets():
            item_action = QAction(customWidget[0], self)
            def tmp(c, pos):
                return lambda: self.newWidgetOnSection(c, pos)
            item_action.triggered.connect(tmp(customWidget[1], e.pos()))
            pluginMenu.addAction(item_action)

        pluginMenu.exec(e.globalPos())

    def mouseMoveEvent(self, e): # This event is only called after clicking down on the frame and dragging
        # Set up multi-select on first move of mouse drag
        if self.multiselector.mode != MultiselectMode.IS_DRAWING_AREA:
                self.multiselector.beginDrawingArea(e)

        # Resize multi-select widget on mouse every proceeding mouse movement (dragging)
        else:
            self.multiselector.continueDrawingArea(e)

    def slot_action1(self, item):
        print("Action 1 triggered")

