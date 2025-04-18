# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfaceUaeubW.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.Widgets import (QCustomSlideMenu, QCustomStackedWidget)
from Qss.icons import _icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1113, 690)
        font = QFont()
        font.setBold(True)
        MainWindow.setFont(font)
        MainWindow.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        MainWindow.setStyleSheet(u"*{\n"
"	border:none;\n"
"	background-color:transparent;\n"
"	background:transparent;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #fff;\n"
"}\n"
"#centralwidget, #homeBtn, #mainBodyContent, QLineEdit{\n"
"	background-color:#1b1b27\n"
"}\n"
"#header, #mainBody{\n"
"	background-color:#27263c;\n"
"}\n"
"#pushButton_2{\n"
"	border: 1px solid #cc5bce;\n"
"    border-radius: 19px;   /* Half of height to make it circular */\n"
"    min-width: 38px;       /* Width = 2 \u00d7 border-radius */\n"
"    min-height: 38px;      /* Height = 2 \u00d7 border-radius */\n"
"    padding: 0;            /* Remove default padding */\n"
"    margin: 0;\n"
"    qproperty-iconSize: 38px;  /* Force icon size via CSS */\n"
"	text-align:center;\n"
"}\n"
"QPushButton{\n"
"	text-align:left;\n"
"	padding: 5px 10px;\n"
"	border-top-left-radius: 10px;\n"
"	border-bottom-left-radius: 10px;\n"
"}\n"
"#homeBtn{\n"
"	border-left: 3px solid #cc5bce;\n"
"	font-weight: bold;\n"
"}\n"
"QLineEdit{\n"
"	padding: 5px 10px;\n"
"	border-radius: 5px;\n"
"}\n"
""
                        "\n"
"#addUserBtn{\n"
"	background-color:  #cc5bce;\n"
"	border-radius: 10px;\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QWidget(self.centralwidget)
        self.header.setObjectName(u"header")
        self.horizontalLayout = QHBoxLayout(self.header)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.header)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.menuBtn = QPushButton(self.frame_2)
        self.menuBtn.setObjectName(u"menuBtn")
        self.menuBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/feather/icons/feather/align-justify.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menuBtn.setIcon(icon)
        self.menuBtn.setIconSize(QSize(24, 24))

        self.horizontalLayout_4.addWidget(self.menuBtn, 0, Qt.AlignmentFlag.AlignLeft)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"Bauhaus"])
        font1.setPointSize(16)
        font1.setBold(True)
        self.label.setFont(font1)

        self.horizontalLayout_4.addWidget(self.label)


        self.horizontalLayout.addWidget(self.frame_2, 0, Qt.AlignmentFlag.AlignLeft)

        self.frame = QFrame(self.header)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_4 = QPushButton(self.frame)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/feather/icons/feather/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_4.setIcon(icon1)
        self.pushButton_4.setIconSize(QSize(32, 32))

        self.horizontalLayout_3.addWidget(self.pushButton_4)

        self.pushButton_3 = QPushButton(self.frame)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/feather/icons/feather/bell.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setIconSize(QSize(32, 32))

        self.horizontalLayout_3.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/feather/icons/feather/user.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon3)
        self.pushButton_2.setIconSize(QSize(38, 38))

        self.horizontalLayout_3.addWidget(self.pushButton_2)


        self.horizontalLayout.addWidget(self.frame, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout.addWidget(self.header)

        self.mainBody = QWidget(self.centralwidget)
        self.mainBody.setObjectName(u"mainBody")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainBody.sizePolicy().hasHeightForWidth())
        self.mainBody.setSizePolicy(sizePolicy)
        self.mainBody.setMinimumSize(QSize(1113, 620))
        self.horizontalLayout_2 = QHBoxLayout(self.mainBody)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 9, 0, 0)
        self.leftMenu = QCustomSlideMenu(self.mainBody)
        self.leftMenu.setObjectName(u"leftMenu")
        self.leftMenu.setMinimumSize(QSize(200, 0))
        self.leftMenu.setMaximumSize(QSize(0, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.leftMenu)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 30)
        self.widget = QWidget(self.leftMenu)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(200, 591))
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(10, 0, 0, 0)
        self.frame_3 = QFrame(self.widget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.homeBtn = QPushButton(self.frame_3)
        self.homeBtn.setObjectName(u"homeBtn")
        self.homeBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/feather/icons/feather/home.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.homeBtn.setIcon(icon4)

        self.verticalLayout_5.addWidget(self.homeBtn)

        self.carsBtn = QPushButton(self.frame_3)
        self.carsBtn.setObjectName(u"carsBtn")
        self.carsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon5 = QIcon()
        icon5.addFile(u":/font_awesome_solid/icons/font_awesome/solid/car.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.carsBtn.setIcon(icon5)

        self.verticalLayout_5.addWidget(self.carsBtn)

        self.compareBtn = QPushButton(self.frame_3)
        self.compareBtn.setObjectName(u"compareBtn")
        self.compareBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon6 = QIcon()
        icon6.addFile(u":/font_awesome_solid/icons/font_awesome/solid/scale-unbalanced.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.compareBtn.setIcon(icon6)

        self.verticalLayout_5.addWidget(self.compareBtn)

        self.newsBtn = QPushButton(self.frame_3)
        self.newsBtn.setObjectName(u"newsBtn")
        self.newsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon7 = QIcon()
        icon7.addFile(u":/font_awesome_regular/icons/font_awesome/regular/newspaper.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.newsBtn.setIcon(icon7)

        self.verticalLayout_5.addWidget(self.newsBtn)

        self.accountBtn = QPushButton(self.frame_3)
        self.accountBtn.setObjectName(u"accountBtn")
        self.accountBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.accountBtn.setIcon(icon3)

        self.verticalLayout_5.addWidget(self.accountBtn)


        self.verticalLayout_4.addWidget(self.frame_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.frame_4 = QFrame(self.widget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_4)
        self.verticalLayout_6.setSpacing(10)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.settingsBtn = QPushButton(self.frame_4)
        self.settingsBtn.setObjectName(u"settingsBtn")
        self.settingsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon8 = QIcon()
        icon8.addFile(u":/feather/icons/feather/settings.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settingsBtn.setIcon(icon8)

        self.verticalLayout_6.addWidget(self.settingsBtn)

        self.helpBtn = QPushButton(self.frame_4)
        self.helpBtn.setObjectName(u"helpBtn")
        self.helpBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon9 = QIcon()
        icon9.addFile(u":/feather/icons/feather/help-circle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.helpBtn.setIcon(icon9)

        self.verticalLayout_6.addWidget(self.helpBtn)

        self.aboutBtn = QPushButton(self.frame_4)
        self.aboutBtn.setObjectName(u"aboutBtn")
        self.aboutBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon10 = QIcon()
        icon10.addFile(u":/feather/icons/feather/info.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.aboutBtn.setIcon(icon10)

        self.verticalLayout_6.addWidget(self.aboutBtn)


        self.verticalLayout_4.addWidget(self.frame_4)


        self.verticalLayout_3.addWidget(self.widget)


        self.horizontalLayout_2.addWidget(self.leftMenu)

        self.mainBodyContent = QWidget(self.mainBody)
        self.mainBodyContent.setObjectName(u"mainBodyContent")
        self.verticalLayout_2 = QVBoxLayout(self.mainBodyContent)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.mainPages = QCustomStackedWidget(self.mainBodyContent)
        self.mainPages.setObjectName(u"mainPages")
        self.homePage = QWidget()
        self.homePage.setObjectName(u"homePage")
        self.label_8 = QLabel(self.homePage)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(230, 270, 291, 151))
        font2 = QFont()
        font2.setPointSize(50)
        self.label_8.setFont(font2)
        self.mainPages.addWidget(self.homePage)
        self.carsPage = QWidget()
        self.carsPage.setObjectName(u"carsPage")
        self.label_5 = QLabel(self.carsPage)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(360, 370, 291, 151))
        self.label_5.setFont(font2)
        self.mainPages.addWidget(self.carsPage)
        self.comparePage = QWidget()
        self.comparePage.setObjectName(u"comparePage")
        self.label_6 = QLabel(self.comparePage)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(290, 270, 291, 151))
        self.label_6.setFont(font2)
        self.mainPages.addWidget(self.comparePage)
        self.newsPage = QWidget()
        self.newsPage.setObjectName(u"newsPage")
        self.label_9 = QLabel(self.newsPage)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(380, 250, 291, 151))
        self.label_9.setFont(font2)
        self.mainPages.addWidget(self.newsPage)
        self.accountPage = QWidget()
        self.accountPage.setObjectName(u"accountPage")
        self.label_4 = QLabel(self.accountPage)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(280, 340, 291, 151))
        self.label_4.setFont(font2)
        self.mainPages.addWidget(self.accountPage)
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName(u"settingsPage")
        self.label_10 = QLabel(self.settingsPage)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(290, 290, 291, 151))
        self.label_10.setFont(font2)
        self.mainPages.addWidget(self.settingsPage)
        self.helpPage = QWidget()
        self.helpPage.setObjectName(u"helpPage")
        self.label_7 = QLabel(self.helpPage)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(340, 270, 291, 151))
        self.label_7.setFont(font2)
        self.mainPages.addWidget(self.helpPage)
        self.aboutPage = QWidget()
        self.aboutPage.setObjectName(u"aboutPage")
        self.label_3 = QLabel(self.aboutPage)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(328, 256, 291, 151))
        self.label_3.setFont(font2)
        self.mainPages.addWidget(self.aboutPage)

        self.verticalLayout_2.addWidget(self.mainPages)


        self.horizontalLayout_2.addWidget(self.mainBodyContent)

        self.rightMenu = QWidget(self.mainBody)
        self.rightMenu.setObjectName(u"rightMenu")
        self.rightMenu.setMinimumSize(QSize(200, 0))
        self.verticalLayout_7 = QVBoxLayout(self.rightMenu)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget_2 = QWidget(self.rightMenu)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_8 = QVBoxLayout(self.widget_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(70, 70))
        self.label_2.setMaximumSize(QSize(70, 70))
        self.label_2.setPixmap(QPixmap(u":/feather/icons/feather/edit-2.png"))
        self.label_2.setScaledContents(True)

        self.verticalLayout_8.addWidget(self.label_2, 0, Qt.AlignmentFlag.AlignHCenter)

        self.frame_5 = QFrame(self.widget_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.lineEdit = QLineEdit(self.frame_5)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_9.addWidget(self.lineEdit)

        self.lineEdit_2 = QLineEdit(self.frame_5)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.verticalLayout_9.addWidget(self.lineEdit_2)

        self.lineEdit_3 = QLineEdit(self.frame_5)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.verticalLayout_9.addWidget(self.lineEdit_3)


        self.verticalLayout_8.addWidget(self.frame_5)

        self.addUserBtn = QPushButton(self.widget_2)
        self.addUserBtn.setObjectName(u"addUserBtn")
        self.addUserBtn.setFont(font)
        self.addUserBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon11 = QIcon()
        icon11.addFile(u":/material_design/icons/material_design/add.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.addUserBtn.setIcon(icon11)
        self.addUserBtn.setIconSize(QSize(24, 24))

        self.verticalLayout_8.addWidget(self.addUserBtn, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_7.addWidget(self.widget_2, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)


        self.horizontalLayout_2.addWidget(self.rightMenu)


        self.verticalLayout.addWidget(self.mainBody)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menuBtn.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Andre's Car Viewing Application", None))
        self.pushButton_4.setText("")
        self.pushButton_3.setText("")
        self.pushButton_2.setText("")
        self.homeBtn.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.carsBtn.setText(QCoreApplication.translate("MainWindow", u"Cars", None))
        self.compareBtn.setText(QCoreApplication.translate("MainWindow", u"Compare", None))
        self.newsBtn.setText(QCoreApplication.translate("MainWindow", u"News", None))
        self.accountBtn.setText(QCoreApplication.translate("MainWindow", u"My Account", None))
        self.settingsBtn.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.helpBtn.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.aboutBtn.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Cars", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Compare", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"News", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Account", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.label_2.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Email", None))
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Phone Number", None))
        self.addUserBtn.setText(QCoreApplication.translate("MainWindow", u"Add User", None))
    # retranslateUi

