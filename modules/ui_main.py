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
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1250, 732)
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        self.styleSheet.setStyleSheet(u"")
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setGeometry(QRect(0, 0, 1621, 941))
        self.bgApp.setStyleSheet(u"background-color: #c2c2c2;")
        self.bgApp.setFrameShape(QFrame.StyledPanel)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.toolbar = QFrame(self.bgApp)
        self.toolbar.setObjectName(u"toolbar")
        self.toolbar.setGeometry(QRect(0, 50, 1621, 100))
        self.toolbar.setStyleSheet(u"background-color: #f1f0ef;")
        self.toolbar.setFrameShape(QFrame.StyledPanel)
        self.toolbar.setFrameShadow(QFrame.Raised)
        self.undoBtn = QPushButton(self.toolbar)
        self.undoBtn.setObjectName(u"undoBtn")
        self.undoBtn.setGeometry(QRect(15, 52, 40, 40))
        self.undoBtn.setAutoFillBackground(False)
        self.undoBtn.setStyleSheet(u"background-color: #d9d9d9; border: none;")
        icon = QIcon()
        icon.addFile(u":/svg/images/svg/undo-svgrepo-com.svg", QSize(), QIcon.Normal, QIcon.On)
        self.undoBtn.setIcon(icon)
        self.undoBtn.setIconSize(QSize(20, 20))
        self.undoBtn.setFlat(False)
        self.fontComboBox = QFontComboBox(self.toolbar)
        self.fontComboBox.setObjectName(u"fontComboBox")
        self.fontComboBox.setGeometry(QRect(65, 52, 164, 40))
        self.fontComboBox.setStyleSheet(u"QComboBox {\n"
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
        self.fontSizeComboBox = QComboBox(self.toolbar)
        self.fontSizeComboBox.setObjectName(u"fontSizeComboBox")
        self.fontSizeComboBox.setGeometry(QRect(235, 52, 78, 42))
        self.fontSizeComboBox.setStyleSheet(u"QComboBox {\n"
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
        self.fontSizeComboBox.setEditable(True)
        self.boldBtn = QPushButton(self.toolbar)
        self.boldBtn.setObjectName(u"boldBtn")
        self.boldBtn.setGeometry(QRect(320, 52, 40, 40))
        font = QFont()
        font.setBold(True)
        self.boldBtn.setFont(font)
        self.boldBtn.setAutoFillBackground(False)
        self.boldBtn.setStyleSheet(u"background-color: #d9d9d9; border: none; font-size: 20px;")
        self.boldBtn.setIconSize(QSize(40, 40))
        self.boldBtn.setFlat(False)
        self.italicBtn = QPushButton(self.toolbar)
        self.italicBtn.setObjectName(u"italicBtn")
        self.italicBtn.setGeometry(QRect(370, 52, 40, 40))
        font1 = QFont()
        font1.setItalic(True)
        self.italicBtn.setFont(font1)
        self.italicBtn.setAutoFillBackground(False)
        self.italicBtn.setStyleSheet(u"background-color: #d9d9d9; border: none; font-size: 20px;")
        self.italicBtn.setIconSize(QSize(40, 40))
        self.italicBtn.setFlat(False)
        self.underlineBtn = QPushButton(self.toolbar)
        self.underlineBtn.setObjectName(u"underlineBtn")
        self.underlineBtn.setGeometry(QRect(420, 52, 40, 40))
        font2 = QFont()
        font2.setUnderline(True)
        self.underlineBtn.setFont(font2)
        self.underlineBtn.setAutoFillBackground(False)
        self.underlineBtn.setStyleSheet(u"background-color: #d9d9d9; border: none; font-size: 20px;")
        self.underlineBtn.setIconSize(QSize(40, 40))
        self.underlineBtn.setFlat(False)
        self.highlightBtn = QPushButton(self.toolbar)
        self.highlightBtn.setObjectName(u"highlightBtn")
        self.highlightBtn.setGeometry(QRect(470, 52, 40, 40))
        font3 = QFont()
        font3.setUnderline(False)
        self.highlightBtn.setFont(font3)
        self.highlightBtn.setAutoFillBackground(False)
        self.highlightBtn.setStyleSheet(u"background-color: #d9d9d9; border: none; font-size: 20px; color: rgb(255, 255, 0);")
        self.highlightBtn.setIconSize(QSize(40, 40))
        self.highlightBtn.setFlat(False)
        self.fontColorComboBox = QComboBox(self.toolbar)
        self.fontColorComboBox.setObjectName(u"fontColorComboBox")
        self.fontColorComboBox.setGeometry(QRect(520, 52, 78, 42))
        self.fontColorComboBox.setStyleSheet(u"QComboBox {\n"
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
        self.fontColorComboBox.setEditable(True)
        self.titlebar = QFrame(self.bgApp)
        self.titlebar.setObjectName(u"titlebar")
        self.titlebar.setGeometry(QRect(-10, 0, 1931, 50))
        self.titlebar.setStyleSheet(u"background-color: #7c66ff;")
        self.titlebar.setFrameShape(QFrame.StyledPanel)
        self.titlebar.setFrameShadow(QFrame.Raised)
        self.appTItle = QLabel(self.titlebar)
        self.appTItle.setObjectName(u"appTItle")
        self.appTItle.setGeometry(QRect(16, 8, 106, 30))
        self.appTItle.setFont(font)
        self.appTItle.setStyleSheet(u"color: #ffffff; font-size: 22px;")
        self.notebookTitle = QLabel(self.titlebar)
        self.notebookTitle.setObjectName(u"notebookTitle")
        self.notebookTitle.setGeometry(QRect(610, 8, 135, 30))
        font4 = QFont()
        self.notebookTitle.setFont(font4)
        self.notebookTitle.setStyleSheet(u"color: #ffffff; font-size: 22px;")
        self.rightButtons = QFrame(self.titlebar)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setGeometry(QRect(1130, 0, 127, 50))
        self.rightButtons.setStyleSheet(u"")
        self.rightButtons.setFrameShape(QFrame.StyledPanel)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setGeometry(QRect(33, 11, 28, 28))
        self.minimizeAppBtn.setStyleSheet(u"QPushButton{\n"
"	border: none;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"	background-color: rgb(106, 88, 221);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Normal, QIcon.On)
        self.minimizeAppBtn.setIcon(icon1)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))
        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setGeometry(QRect(70, 11, 28, 28))
        self.maximizeRestoreAppBtn.setStyleSheet(u"QPushButton{\n"
"	border: none;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"	background-color: rgb(106, 88, 221);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Normal, QIcon.On)
        self.maximizeRestoreAppBtn.setIcon(icon2)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))
        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setGeometry(QRect(99, 11, 28, 28))
        self.closeAppBtn.setStyleSheet(u"QPushButton{\n"
"	border: none;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"	background-color: rgb(106, 88, 221);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Normal, QIcon.On)
        self.closeAppBtn.setIcon(icon3)
        self.closeAppBtn.setIconSize(QSize(20, 20))
        self.sections = QFrame(self.bgApp)
        self.sections.setObjectName(u"sections")
        self.sections.setGeometry(QRect(0, 150, 1621, 40))
        self.sections.setStyleSheet(u"background-color: #afafaf;")
        self.sections.setFrameShape(QFrame.StyledPanel)
        self.sections.setFrameShadow(QFrame.Raised)
        self.pages = QFrame(self.bgApp)
        self.pages.setObjectName(u"pages")
        self.pages.setGeometry(QRect(0, 150, 240, 791))
        self.pages.setStyleSheet(u"background-color: #ffffff;")
        self.pages.setFrameShape(QFrame.StyledPanel)
        self.pages.setFrameShadow(QFrame.Raised)
        self.notebooks = QFrame(self.pages)
        self.notebooks.setObjectName(u"notebooks")
        self.notebooks.setGeometry(QRect(0, 0, 245, 40))
        self.notebooks.setStyleSheet(u"background-color: #d9d9d9;")
        self.notebooks.setFrameShape(QFrame.StyledPanel)
        self.notebooks.setFrameShadow(QFrame.Raised)
        self.addPage = QFrame(self.pages)
        self.addPage.setObjectName(u"addPage")
        self.addPage.setGeometry(QRect(0, 550, 240, 35))
        self.addPage.setStyleSheet(u"background-color: #d9d9d9;")
        self.addPage.setFrameShape(QFrame.StyledPanel)
        self.addPage.setFrameShadow(QFrame.Raised)
        self.pagesTitle = QLabel(self.pages)
        self.pagesTitle.setObjectName(u"pagesTitle")
        self.pagesTitle.setGeometry(QRect(8, 49, 62, 32))
        self.pagesTitle.setFont(font4)
        self.pagesTitle.setStyleSheet(u"color: #000000; font-size: 24px;")
        self.workspace = QFrame(self.bgApp)
        self.workspace.setObjectName(u"workspace")
        self.workspace.setGeometry(QRect(240, 190, 1261, 631))
        self.workspace.setFrameShape(QFrame.StyledPanel)
        self.workspace.setFrameShadow(QFrame.Raised)
        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.undoBtn.setText("")
        self.fontSizeComboBox.setCurrentText(QCoreApplication.translate("MainWindow", u"12", None))
        self.boldBtn.setText(QCoreApplication.translate("MainWindow", u"B", None))
        self.italicBtn.setText(QCoreApplication.translate("MainWindow", u"I", None))
        self.underlineBtn.setText(QCoreApplication.translate("MainWindow", u"U", None))
        self.highlightBtn.setText(QCoreApplication.translate("MainWindow", u"HI", None))
        self.fontColorComboBox.setCurrentText(QCoreApplication.translate("MainWindow", u"Red", None))
        self.appTItle.setText(QCoreApplication.translate("MainWindow", u"OpenNote", None))
        self.notebookTitle.setText(QCoreApplication.translate("MainWindow", u"My Notebook", None))
        self.minimizeAppBtn.setText("")
        self.maximizeRestoreAppBtn.setText("")
        self.closeAppBtn.setText("")
        self.pagesTitle.setText(QCoreApplication.translate("MainWindow", u"Pages", None))
    # retranslateUi

