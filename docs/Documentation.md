## The Plugin (Custom Widget) System

Any widget in PYQT is able to be added to the program as an interactable widget in the notebook.
Any custom widget is able to be added, deleted, saved, loaded, copied, pasted, moved, and resized out of the box.

To implement a custom widget follow these steps:
- Create a python file with a unique name.
- Inside the file, extend either:
    - A functional PYQT widget that was extended from a QWidget.
        - These widgets will work out of the box and only need to implement the required methods as described below (see the Textbox widget as an example).
    - A QWidget
        - These widgets will need more customization but allow more flexibility (see the Table widget as an example).

- After extending one of these classes, you are only required to implement 3 methods.
    - **@staticmethod new(clickPos: QPoint) -> InstaceOfWidget** - This method will be called by the notebook when adding your custom widget into the program. It will recieve a QPoint that holds the coordinates that the user would like to add this widget. This method should handle any logic that should run when the widget is initialized for the first time (see the Image widget as the most in depth example). This method should then return an instance of your custom widget, likely by calling the constructor.

    - **__getstate__() -> any** - This method is used by Pickle to persist your widget to the disk when the notebook is saved, it is also used by the clipboard and undo functionality to handle faithful replication. Generally, this method should return a dict with any important information about the state. Any part of the state you would like to be saved (such as stylesheet, geometry, content, etc) should be saved to this dict (see the Table widget for the most in depth example).

    - **__setstate__(data) -> None** - This method is used by Pickle to reinstantiate your widget when the notebook is loaded from the disk, as with __getstate__ it is used by the clipboard and undo functionality. This method will receive the exact object that you returned in your __getstate__ function, it should use this object to call the constructor of your class, and bring back any state (see any widget).

    - Note: More methods or functionality may be required for your widget to function as you like, but these three are the only ones that the notebook specifically has to have.

- Once these three methods are implemented, you should be able to place your python file in the \PluginWidgets directory, then when the application is started, you can right click on an empty part of the editor, choose "Add Custom Widget" from the menu, and select the name of your widget from the next menu that appears. If everything is implemented correctly, your widget will appear where you originally right clicked.

### Optional Widget Methods
There are a few more methods that a widget can choose to implement for additional functionality, but it is not required. The program will check if the widget implements these before trying to call them.
- **newGeometryEvent(newGeometry: QRect) -> None** - This method is called on the widget when the geometry (x, y, width, height) of the container that wraps the widget is changed. This can be used for things such as scaling an image to maintain aspect ratio when the container is resized (see Image widget).
- **customMenuItems() -> List[QAction and/or QActionWidget]** - This method is used to add additional items to the menu that appears when a user right clicks on the container wrapping a widget, which usually displays options for copy, cut, delete. Any QAction that is in the list will be placed at the bottom of the menu, and any QActionWidgets will be placed at the top (see Textbox widget for QActionWidget example, and Table widget for QAction example).
- **checkEmpty() -> boolean** - This method is called when the user's mouse leaves the container wrapping the widget to determine if the widget is considered "empty", and should be deleted. If true is returned, the widget will be deleted when the user's mouse leaves the container wrapping the widget, if false is returned, it will not. If the method is not implemented, it will not delete the widget (see Textbox widget for example).

## The Program Itsself

The most largest and most important parts of the program are described by the class diagram below.

![Class Diagram](https://github.com/rockCityMath/OpenNote/blob/docs/docs/OpenNote%20Class%20Diagram.png)

- **Editor** - Stores a NotebookModel which contains all models for the active notebook. Stores all views that the user interacts with to make changes to the models.
- **NotebookModel** - Stores information about the notebook such as the path, title and a list of PageModels.
- **PageModel** - Stores the page’s title, list of sections, uuid, and parentUuid (used to determine its place in the hierarchy).
- **SectionModel** - Stores the section’s title and it’s widgets. Widgets are stored as DraggableContainers during runtime, and their real classes during save.
- **SectionView** - The view that allows users to interact with the current page’s section models. Including adding, removing, and renaming sections.
- **EditorFrameView** - The view that displays all the DraggableContainers in the active section and allows the user to interact with them through features such as dragging, multiselecting, and clipboard.
- **PageView** - The view that allows users to interact with the current notebook’s pages. Including adding, renaming, and deleting pages.
- **NotebookTitleView** - The view that displays the current notebook’s title and allows the user to change it.
- **DraggableContainer** - Very important class. This wraps the widgets that the user will interact with and allows them to be moved and resized, pass events to the child, and allows the editor frame and its features to agnostically interact with any widget regardless of what it actually is.
- **Widget** - The object/item/widget that the user interacts with such as a text box or image. Each widget implements a set/getstate and static new() method to allow it to be used with the program. Each widget handles all of its own events and functionality.


## The ViewModel Architecture
It was our first time trying to implement this architecture, so definitely don't take it's implementation in this program as the fully correct way, but I'll attempt to describe the way we did it.
- **Models** - Located in the \Models directory, these classes contain the actual underlying data that is displayed on the screen. If you're familiar with web development, I think of the view as the "frontend" and controller/logic layers of the backend, and the model as the "respository" layer and database of the backend.

- **Views** - Located in the \Views directory, these classes handle the visual display and user interaction with the underlying Models. When the user interacts with the view, the view handles updating the UI and the underlying data model to reflect this interaction.
    - The views handle updating the underlying data model by storing a reference to the model that they are currently displaying, and then performing the updates the user makes in the UI on these references (which updates the actual Model that the reference refers to).
    - For example: PageView has self.pageModels, which is a reference to all of the PageModels in the current notebook, so when a user does something such as rename a page in the UI, the View will rename the page in its Model as well.
    - Note: I'm really not sure if that reference based approach is very good, I would read the PYQT docs on the ViewModel architecture and look into that more before setting that in stone any more than it already is in the program.


## The Save/Load Flows
One of the more complex parts of the program not exactly relating to its strucutre is the way that saving and loading from the disk works. Since the program uses Pickle for saving/loading, and PYQT objects cannot be pickled (serialized), everything that should be saved/loaded has to end up in an object that Pickle can serialize. The serializable objects in this program are the models.

### Saving
When saving, the program itsself just calls pickle.dump() on the notebook model. The serializing of the notebook and everything in it takes place with the __getstate__() functions specified on any object that is not naturally serializable by pickle. The way I think of this is that the objects nested in the notebook are serialized from the bottom up (refer to the "stores" relationships on the class diagram (not the one between Editor and NotebookModel though, the Editor is not saved))
- First, widgets have to be serialized. Widgets all implement their own serialization through the __getstate__ function.

- Then, SectionModels have to be serialized. Since the actual widgets themselves are now serialized, the SectionModel only needs to store that widget (after getting it from the DraggableContainer). The section title is naturally picklable.

- Then, the PageModels have to be serialized. Since any SectionModels on the PageModel are now serialized, the PageModel is now naturally serializable.

- Finally, the NotebookModel has to be serialized. Since everything on the NotebookModel is now serialized, the NotebookModel is now naturally serializable.

- At this point, the whole notebook is serialized and ready to be stored on the disk by the pickle.dump() function.

### Loading
When loading, the program itsself just calls the pickle.load() function on the file. The reinstantiation of the models is handled through the __setstate__() functions implemented on them. Don't quote me, but I believe that thinking of loading in the same "bottom up" way as saving makes sense with the way deserialization works in Pickle.
- First, the widgets need to be reinstantiated/deserialized, they do this with the __setstate__() methods that they implement.

- Then, the sections need to be reinstantiated, they do this with the __setstate__() method that they implement, but the widgets on them also need to be put back into DraggableContainers. This is done by emitting a widgetShouldLoad signal which the EditorFrameView will listen for and when it recieves it, it will wrap the widget in a DraggableContainer and add that DraggableContainer the view so that it can be interacted with, it will also add this DraggableContainer to the section that emitted the event where it will be stored during runtime.

- Then, the remaining models naturally reinstantiate themselves with their respective __setstate__() methods.


