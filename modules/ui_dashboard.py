# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QScrollArea,
    QSizePolicy, QWidget)

class Ui_Dashboard(object):
    def setupUi(self, Dashboard):
        if not Dashboard.objectName():
            Dashboard.setObjectName(u"Dashboard")
        Dashboard.resize(842, 600)
        Dashboard.setStyleSheet(u"")
        self.centralwidget = QWidget(Dashboard)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 851, 51))
        self.frame.setStyleSheet(u"background-color: rgb(200, 100, 217);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.title = QLabel(self.frame)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(370, 20, 111, 21))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        self.title.setFont(font)
        self.title.setStyleSheet(u"font: 24pt \"Arial\";\n"
"")
        self.addNotebookButton = QPushButton(self.frame)
        self.addNotebookButton.setObjectName(u"addNotebookButton")
        self.addNotebookButton.setGeometry(QRect(580, 10, 91, 32))
        self.openNotebookButton = QPushButton(self.frame)
        self.openNotebookButton.setObjectName(u"openNotebookButton")
        self.openNotebookButton.setGeometry(QRect(700, 10, 100, 32))
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(0, 100, 841, 461))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 839, 459))
        self.gridLayoutWidget = QWidget(self.scrollAreaWidgetContents)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(-1, -1, 841, 461))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 60, 71, 31))
        self.label.setStyleSheet(u"font: 18pt \"Arial\";")
        self.name = QLineEdit(self.centralwidget)
        self.name.setObjectName(u"name")
        self.name.setGeometry(QRect(240, 70, 241, 21))
        self.name.setStyleSheet(u"border-color: rgb(52, 52, 52);")
        self.location = QLineEdit(self.centralwidget)
        self.location.setObjectName(u"location")
        self.location.setGeometry(QRect(520, 70, 291, 21))
        self.location.setStyleSheet(u"border-color: rgb(76, 76, 76);")
        Dashboard.setCentralWidget(self.centralwidget)

        self.retranslateUi(Dashboard)

        QMetaObject.connectSlotsByName(Dashboard)
    # setupUi

    def retranslateUi(self, Dashboard):
        Dashboard.setWindowTitle(QCoreApplication.translate("Dashboard", u"MainWindow", None))
        self.title.setText(QCoreApplication.translate("Dashboard", u"OpenNote", None))
        self.addNotebookButton.setText(QCoreApplication.translate("Dashboard", u"Create", None))
        self.openNotebookButton.setText(QCoreApplication.translate("Dashboard", u"Load", None))
        self.label.setText(QCoreApplication.translate("Dashboard", u"Recent", None))
        self.name.setPlaceholderText(QCoreApplication.translate("Dashboard", u"name", None))
        self.location.setPlaceholderText(QCoreApplication.translate("Dashboard", u"location", None))
    # retranslateUi

