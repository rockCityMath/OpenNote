# OpenNote
**Open Source OneNote Alternative**

OpenNote aims to provide much of the functionality of Microsoft's OneNote software but take an open source and extensible approach to development. The project is built using Python and PYQT and allows users to take notes by creating notebooks where they can place text, images, and other items on a page. The program hopes to support plugins in the future.

## Development Setup
- Install Python
- Install PySide6 (pip install pyside6)
- Install [QT Designer](https://build-system.fman.io/qt-designer-download) (questionable link)

> Open main.ui in QT Designer to develop UI
> 
> Open modules/app_functions to develop most functionality
> 
> Run program with `python main.py`
> 
> Build program with `python setup.py build` (have cx-freeze installed)

## Development Instructions
- Assign yourself a ticket on Trello and move it to in progress
- Check out a branch off of main and name it [type]/[ticket-summary] (feature/create-notebook) (bugfix/remove-text)
- Develop
- Submit a PR against main branch (name it the same as the branch)
- Move the ticket into code review  
  
**\* If you are checking a PR, please check the code AND checkout the branch and run it to make sure the features work**  
**\* If you merge the PR, please move the ticket into done**   
**\* Please limit your PRs to the scope of the ticket to avoid conflicts**  


## Project Files And Folders
> **main.py**: Application initialization file.
> 
> **main.ui**: Qt Designer project.
> 
> **resouces.qrc**: Qt Designer resoucers, Use version 6 >
> 
> **setup.py**: Build script (install cx-freeze)
> 
> **themes/**: Themes (.qss).
> 
> **modules/**: Module for running PyDracula GUI.
> 
> **modules/app_funtions.py**: Application's functions.
> 
> **modules/app_settings.py**: Global variables to configure user interface.
> 
> **modules/resources_rc.py**: "resource.qrc" file compiled for python using the command: ```pyside6-rcc resources.qrc -o resources_rc.py```.
> 
> **modules/ui_functions.py**: Functions related to the user interface / GUI.
> 
> **images/**: Images and icons here, convert to Python (resources_re.py) ```pyside6-rcc resources.qrc -o resources_rc.py```.
  
  
This project's UI is based on [PyDracula](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6) 



