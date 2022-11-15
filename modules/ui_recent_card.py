# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'recentCard.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
    QWidget)

class Ui_Recentcard(object):
    def setupUi(self, Recentcard):
        if not Recentcard.objectName():
            Recentcard.setObjectName(u"Recentcard")
        Recentcard.resize(150, 100)
        Recentcard.setWindowOpacity(100.000000000000000)
        Recentcard.setLayoutDirection(Qt.LeftToRight)
        Recentcard.setAutoFillBackground(False)
        Recentcard.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.title = QLabel(Recentcard)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(0, 0, 151, 101))
        self.title.setFocusPolicy(Qt.ClickFocus)
        self.title.setStyleSheet(u"color: rgb(72, 72, 72);\n"
"selection-background-color: rgb(181, 247, 255);")
        self.title.setFrameShape(QFrame.NoFrame)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setWordWrap(False)

        self.retranslateUi(Recentcard)

        QMetaObject.connectSlotsByName(Recentcard)
    # setupUi

    def retranslateUi(self, Recentcard):
        Recentcard.setWindowTitle(QCoreApplication.translate("Recentcard", u"Form", None))
        self.title.setText(QCoreApplication.translate("Recentcard", u"TextLabel", None))
    # retranslateUi

