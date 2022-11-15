# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFontComboBox, QFrame,
    QLabel, QListView, QMainWindow, QPushButton,
    QSizePolicy, QToolButton, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1250, 732)
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        self.styleSheet.setStyleSheet(u"QPushButton::hover{\n"
"background-color: #cecece;\n"
"}")
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setGeometry(QRect(0, 0, 1621, 941))
        self.bgApp.setStyleSheet(u"background-color: #c2c2c2;")
        self.bgApp.setFrameShape(QFrame.StyledPanel)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.toolbar = QFrame(self.bgApp)
        self.toolbar.setObjectName(u"toolbar")
        self.toolbar.setGeometry(QRect(0, 0, 1621, 100))
        self.toolbar.setStyleSheet(u"background-color: #f1f0ef;")
        self.toolbar.setFrameShape(QFrame.StyledPanel)
        self.toolbar.setFrameShadow(QFrame.Raised)
        self.undoBtn = QPushButton(self.toolbar)
        self.undoBtn.setObjectName(u"undoBtn")
        self.undoBtn.setGeometry(QRect(15, 52, 40, 40))
        self.undoBtn.setAutoFillBackground(False)
        self.undoBtn.setStyleSheet(u"QPushButton{\n"
"background-color: #d9d9d9; border: none;\n"
"} \n"
"QPushButton::hover{\n"
"background-color: #cecece;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/svg/images/svg/undo-svgrepo-com.svg", QSize(), QIcon.Normal, QIcon.On)
        self.undoBtn.setIcon(icon)
        self.undoBtn.setIconSize(QSize(20, 20))
        self.undoBtn.setFlat(False)
        self.fontCB = QFontComboBox(self.toolbar)
        self.fontCB.setObjectName(u"fontCB")
        self.fontCB.setGeometry(QRect(65, 52, 164, 40))
        self.fontCB.setStyleSheet(u"QComboBox {\n"
"	background-color: #d9d9d9;\n"
"    border: none;\n"
"	font-size: 20px;\n"
"	padding: 0px 3px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"	border: none;\n"
"color: black;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"	padding-right: 5px;\n"
"    image: url(:/svg/images/svg/arrow-down-icon.svg);\n"
"	width: 12px;\n"
"}\n"
"\n"
"")
        self.fontSizeCB = QComboBox(self.toolbar)
        self.fontSizeCB.setObjectName(u"fontSizeCB")
        self.fontSizeCB.setGeometry(QRect(235, 52, 78, 42))
        self.fontSizeCB.setStyleSheet(u"QComboBox {\n"
"	background-color: #d9d9d9;\n"
"    border: none;\n"
"	font-size: 20px;\n"
"	padding: 0px 3px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"	border: none;\n"
"color: black;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"	padding-right: 5px;\n"
"    image: url(:/svg/images/svg/arrow-down-icon.svg);\n"
"	width: 12px;\n"
"}\n"
"\n"
"")
        self.fontSizeCB.setEditable(True)
        self.boldBtn = QPushButton(self.toolbar)
        self.boldBtn.setObjectName(u"boldBtn")
        self.boldBtn.setGeometry(QRect(320, 52, 40, 40))
        font = QFont()
        self.boldBtn.setFont(font)
        self.boldBtn.setAutoFillBackground(False)
        self.boldBtn.setStyleSheet(u"\n"
"QPushButton{\n"
"background-color: #d9d9d9; border: none; font-size: 20px;\n"
"} \n"
"QPushButton::hover{\n"
"background-color: #cecece;\n"
"}")
        self.boldBtn.setIconSize(QSize(40, 40))
        self.boldBtn.setFlat(False)
        self.italicBtn = QPushButton(self.toolbar)
        self.italicBtn.setObjectName(u"italicBtn")
        self.italicBtn.setGeometry(QRect(370, 52, 40, 40))
        self.italicBtn.setFont(font)
        self.italicBtn.setAutoFillBackground(False)
        self.italicBtn.setStyleSheet(u"QPushButton{\n"
"background-color: #d9d9d9; border: none; font-size: 20px; \n"
"}\n"
"QPushButton::hover{\n"
"background-color: #cecece;\n"
"}")
        self.italicBtn.setIconSize(QSize(40, 40))
        self.italicBtn.setFlat(False)
        self.underlineBtn = QPushButton(self.toolbar)
        self.underlineBtn.setObjectName(u"underlineBtn")
        self.underlineBtn.setGeometry(QRect(420, 52, 40, 40))
        self.underlineBtn.setFont(font)
        self.underlineBtn.setAutoFillBackground(False)
        self.underlineBtn.setStyleSheet(u"QPushButton{\n"
"background-color: #d9d9d9; border: none; font-size: 20px;\n"
"}\n"
"QPushButton::hover{\n"
"background-color: #cecece;\n"
"}")
        self.underlineBtn.setIconSize(QSize(40, 40))
        self.underlineBtn.setFlat(False)
        self.highlightBtn = QPushButton(self.toolbar)
        self.highlightBtn.setObjectName(u"highlightBtn")
        self.highlightBtn.setGeometry(QRect(470, 52, 40, 40))
        self.highlightBtn.setFont(font)
        self.highlightBtn.setAutoFillBackground(False)
        self.highlightBtn.setStyleSheet(u"QPushButton{\n"
"background-color: #d9d9d9; border: none; font-size: 20px; color: rgb(255, 255, 0);\n"
"}\n"
"QPushButton::hover{\n"
"background-color: #cecece;\n"
"}")
        self.highlightBtn.setIconSize(QSize(40, 40))
        self.highlightBtn.setFlat(False)
        self.fontColorCB = QComboBox(self.toolbar)
        self.fontColorCB.setObjectName(u"fontColorCB")
        self.fontColorCB.setGeometry(QRect(520, 52, 78, 42))
        self.fontColorCB.setStyleSheet(u"QComboBox {\n"
"	background-color: #d9d9d9;\n"
"    border: none;\n"
"	font-size: 20px;\n"
"	padding: 0px 3px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"	border: none;\n"
"color: black;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"	padding-right: 5px;\n"
"    image: url(:/svg/images/svg/arrow-down-icon.svg);\n"
"	width: 12px;\n"
"}\n"
"\n"
"")
        self.fontColorCB.setEditable(True)
        self.fileBtn = QToolButton(self.toolbar)
        self.fileBtn.setObjectName(u"fileBtn")
        self.fileBtn.setGeometry(QRect(16, 10, 40, 30))
        self.fileBtn.setStyleSheet(u"QToolButton{\n"
"background-color: #f1f0ef; border: none; font-size: 22px;\n"
"}\n"
"\n"
"QToolButton::hover{\n"
"background-color: #d9d9d9;\n"
"}")
        self.homeBtn = QToolButton(self.toolbar)
        self.homeBtn.setObjectName(u"homeBtn")
        self.homeBtn.setGeometry(QRect(65, 10, 60, 30))
        self.homeBtn.setStyleSheet(u"QToolButton{\n"
"background-color: #f1f0ef; border: none; font-size: 22px;\n"
"}\n"
"\n"
"QToolButton::hover{\n"
"background-color: #d9d9d9;\n"
"}")
        self.viewBtn = QToolButton(self.toolbar)
        self.viewBtn.setObjectName(u"viewBtn")
        self.viewBtn.setGeometry(QRect(130, 10, 60, 30))
        self.viewBtn.setStyleSheet(u"QToolButton{\n"
"background-color: #f1f0ef; border: none; font-size: 22px;\n"
"}\n"
"\n"
"QToolButton::hover{\n"
"background-color: #d9d9d9;\n"
"}")
        self.helpBtn = QToolButton(self.toolbar)
        self.helpBtn.setObjectName(u"helpBtn")
        self.helpBtn.setGeometry(QRect(195, 10, 61, 30))
        self.helpBtn.setStyleSheet(u"QToolButton{\n"
"background-color: #f1f0ef; border: none; font-size: 22px;\n"
"}\n"
"\n"
"QToolButton::hover{\n"
"background-color: #d9d9d9;\n"
"}")
        self.saveBtn = QToolButton(self.toolbar)
        self.saveBtn.setObjectName(u"saveBtn")
        self.saveBtn.setGeometry(QRect(260, 10, 61, 30))
        self.saveBtn.setStyleSheet(u"QToolButton{\n"
"background-color: #f1f0ef; border: none; font-size: 22px;\n"
"}\n"
"\n"
"QToolButton::hover{\n"
"background-color: #d9d9d9;\n"
"}")
        self.sections = QFrame(self.bgApp)
        self.sections.setObjectName(u"sections")
        self.sections.setGeometry(QRect(0, 100, 1621, 40))
        self.sections.setStyleSheet(u"background-color: #afafaf;")
        self.sections.setFrameShape(QFrame.StyledPanel)
        self.sections.setFrameShadow(QFrame.Raised)
        self.pages = QFrame(self.bgApp)
        self.pages.setObjectName(u"pages")
        self.pages.setGeometry(QRect(0, 100, 240, 791))
        self.pages.setStyleSheet(u"background-color: #ffffff;")
        self.pages.setFrameShape(QFrame.StyledPanel)
        self.pages.setFrameShadow(QFrame.Raised)
        self.notebooks = QFrame(self.pages)
        self.notebooks.setObjectName(u"notebooks")
        self.notebooks.setGeometry(QRect(0, 0, 245, 40))
        self.notebooks.setStyleSheet(u"background-color: #d9d9d9;")
        self.notebooks.setFrameShape(QFrame.StyledPanel)
        self.notebooks.setFrameShadow(QFrame.Raised)
        self.notebookCB = QComboBox(self.notebooks)
        self.notebookCB.setObjectName(u"notebookCB")
        self.notebookCB.setGeometry(QRect(0, 0, 240, 40))
        self.notebookCB.setStyleSheet(u"QComboBox {\n"
"	background-color: #d9d9d9;\n"
"    border: none;\n"
"	font-size: 20px;\n"
"	padding: 0px 3px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"	border: none;\n"
"color: black;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"	padding-right: 5px;\n"
"    image: url(:/svg/images/svg/arrow-down-icon.svg);\n"
"	width: 12px;\n"
"}\n"
"\n"
"")
        self.notebookCB.setEditable(True)
        self.addPage = QFrame(self.pages)
        self.addPage.setObjectName(u"addPage")
        self.addPage.setGeometry(QRect(0, 600, 240, 35))
        self.addPage.setStyleSheet(u"background-color: #d9d9d9;")
        self.addPage.setFrameShape(QFrame.StyledPanel)
        self.addPage.setFrameShadow(QFrame.Raised)
        self.addPageBtn = QPushButton(self.addPage)
        self.addPageBtn.setObjectName(u"addPageBtn")
        self.addPageBtn.setGeometry(QRect(0, 0, 240, 35))
        self.addPageBtn.setStyleSheet(u"QPushButton {\n"
"background-color: #d9d9d9;\n"
"border: none;\n"
"font-size: 20px;\n"
"padding-bottom: 5px;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"background-color: #cecece;\n"
"}")
        self.pagesTitle = QLabel(self.pages)
        self.pagesTitle.setObjectName(u"pagesTitle")
        self.pagesTitle.setGeometry(QRect(8, 49, 111, 32))
        self.pagesTitle.setFont(font)
        self.pagesTitle.setStyleSheet(u"color: #000000; font-size: 24px;")
        self.pagesList = QListView(self.pages)
        self.pagesList.setObjectName(u"pagesList")
        self.pagesList.setGeometry(QRect(10, 90, 211, 501))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(12)
        font1.setBold(False)
        self.pagesList.setFont(font1)
        self.pagesList.setFrameShape(QFrame.NoFrame)
        self.pagesList.setLineWidth(0)
        self.workspace = QWidget(self.bgApp)
        self.workspace.setObjectName(u"workspace")
        self.workspace.setGeometry(QRect(240, 140, 1261, 631))
        self.activePage = QLabel(self.workspace)
        self.activePage.setObjectName(u"activePage")
        self.activePage.setGeometry(QRect(70, 20, 311, 71))
        font2 = QFont()
        font2.setPointSize(28)
        self.activePage.setFont(font2)
        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.undoBtn.setText("")
        self.fontSizeCB.setCurrentText(QCoreApplication.translate("MainWindow", u"12", None))
        self.boldBtn.setText(QCoreApplication.translate("MainWindow", u"B", None))
        self.italicBtn.setText(QCoreApplication.translate("MainWindow", u"I", None))
        self.underlineBtn.setText(QCoreApplication.translate("MainWindow", u"U", None))
        self.highlightBtn.setText(QCoreApplication.translate("MainWindow", u"HI", None))
        self.fontColorCB.setCurrentText(QCoreApplication.translate("MainWindow", u"Red", None))
        self.fileBtn.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.homeBtn.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.viewBtn.setText(QCoreApplication.translate("MainWindow", u"View", None))
        self.helpBtn.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.saveBtn.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.notebookCB.setCurrentText(QCoreApplication.translate("MainWindow", u"My Notebook", None))
        self.addPageBtn.setText(QCoreApplication.translate("MainWindow", u"+ Create New Page", None))
        self.pagesTitle.setText(QCoreApplication.translate("MainWindow", u"Pages", None))
        self.activePage.setText(QCoreApplication.translate("MainWindow", u"ActivePage", None))
    # retranslateUi

