# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'client_form.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.resize(268, 527)
        self.actionserver_ip = QAction(mainWindow)
        self.actionserver_ip.setObjectName(u"actionserver_ip")
        self.action_name_set = QAction(mainWindow)
        self.action_name_set.setObjectName(u"action_name_set")
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_ip_set = QLineEdit(self.centralwidget)
        self.lineEdit_ip_set.setObjectName(u"lineEdit_ip_set")

        self.horizontalLayout_2.addWidget(self.lineEdit_ip_set)

        self.btn_ip_set = QPushButton(self.centralwidget)
        self.btn_ip_set.setObjectName(u"btn_ip_set")

        self.horizontalLayout_2.addWidget(self.btn_ip_set)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_message = QLineEdit(self.centralwidget)
        self.lineEdit_message.setObjectName(u"lineEdit_message")

        self.horizontalLayout.addWidget(self.lineEdit_message)

        self.btn_message = QPushButton(self.centralwidget)
        self.btn_message.setObjectName(u"btn_message")

        self.horizontalLayout.addWidget(self.btn_message)


        self.verticalLayout.addLayout(self.horizontalLayout)

        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 268, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mainWindow)
        self.statusbar.setObjectName(u"statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.action_name_set)

        self.retranslateUi(mainWindow)

        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QCoreApplication.translate("mainWindow", u"ddatG-Client", None))
        self.actionserver_ip.setText(QCoreApplication.translate("mainWindow", u"server - ip", None))
        self.action_name_set.setText(QCoreApplication.translate("mainWindow", u"\ub2c9\ub124\uc784 \uc124\uc815", None))
        self.label.setText(QCoreApplication.translate("mainWindow", u"\ud604\uc7ac \uc11c\ubc84 : ", None))
        self.btn_ip_set.setText(QCoreApplication.translate("mainWindow", u"\uc811\uc18d", None))
        self.btn_message.setText(QCoreApplication.translate("mainWindow", u"\uc804\uc1a1", None))
        self.menu.setTitle(QCoreApplication.translate("mainWindow", u"\uc124\uc815", None))
    # retranslateUi

