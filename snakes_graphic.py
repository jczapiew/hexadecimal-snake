# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'snakes_GUI.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Snakes(object):
    def setupUi(self, Snakes):
        if not Snakes.objectName():
            Snakes.setObjectName(u"Snakes")
        Snakes.resize(821, 546)
        self.centralwidget = QWidget(Snakes)
        self.centralwidget.setObjectName(u"centralwidget")
        self.exitButton = QPushButton(self.centralwidget)
        self.exitButton.setObjectName(u"exitButton")
        self.exitButton.setGeometry(QRect(750, 10, 61, 51))
        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setGeometry(QRect(660, 80, 71, 41))
        self.onePlayer = QPushButton(self.centralwidget)
        self.onePlayer.setObjectName(u"onePlayer")
        self.onePlayer.setGeometry(QRect(650, 20, 41, 21))
        self.playersLabel = QLabel(self.centralwidget)
        self.playersLabel.setObjectName(u"playersLabel")
        self.playersLabel.setGeometry(QRect(650, 0, 101, 21))
        self.twoPlayers = QPushButton(self.centralwidget)
        self.twoPlayers.setObjectName(u"twoPlayers")
        self.twoPlayers.setGeometry(QRect(700, 20, 41, 21))
        self.resetButton = QPushButton(self.centralwidget)
        self.resetButton.setObjectName(u"resetButton")
        self.resetButton.setGeometry(QRect(740, 80, 71, 41))
        self.pauseButton = QPushButton(self.centralwidget)
        self.pauseButton.setObjectName(u"pauseButton")
        self.pauseButton.setGeometry(QRect(660, 130, 71, 41))
        self.playerOnePoints = QTextEdit(self.centralwidget)
        self.playerOnePoints.setObjectName(u"playerOnePoints")
        self.playerOnePoints.setGeometry(QRect(660, 270, 51, 31))
        self.pointsLabel = QLabel(self.centralwidget)
        self.pointsLabel.setObjectName(u"pointsLabel")
        self.pointsLabel.setGeometry(QRect(710, 230, 31, 21))
        self.playerOnePointsLabel = QLabel(self.centralwidget)
        self.playerOnePointsLabel.setObjectName(u"playerOnePointsLabel")
        self.playerOnePointsLabel.setGeometry(QRect(670, 250, 39, 13))
        self.playerTwoPointsLabel = QLabel(self.centralwidget)
        self.playerTwoPointsLabel.setObjectName(u"playerTwoPointsLabel")
        self.playerTwoPointsLabel.setGeometry(QRect(730, 250, 39, 13))
        self.playerTwoPoints = QTextEdit(self.centralwidget)
        self.playerTwoPoints.setObjectName(u"playerTwoPoints")
        self.playerTwoPoints.setGeometry(QRect(730, 270, 51, 31))
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(660, 310, 141, 131))
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(0, 0, 641, 501))
        self.button_multiplayer = QPushButton(self.centralwidget)
        self.button_multiplayer.setObjectName(u"button_multiplayer")
        self.button_multiplayer.setGeometry(QRect(670, 480, 121, 23))
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(650, 450, 111, 20))
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(760, 450, 41, 20))
        self.replayButton = QPushButton(self.centralwidget)
        self.replayButton.setObjectName(u"replayButton")
        self.replayButton.setGeometry(QRect(740, 130, 71, 41))
        self.savejsonButton = QPushButton(self.centralwidget)
        self.savejsonButton.setObjectName(u"savejsonButton")
        self.savejsonButton.setGeometry(QRect(660, 180, 71, 41))
        self.readjsonButton = QPushButton(self.centralwidget)
        self.readjsonButton.setObjectName(u"readjsonButton")
        self.readjsonButton.setGeometry(QRect(740, 180, 71, 41))
        self.botButton = QPushButton(self.centralwidget)
        self.botButton.setObjectName(u"botButton")
        self.botButton.setGeometry(QRect(660, 50, 75, 23))
        Snakes.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Snakes)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 821, 21))
        Snakes.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Snakes)
        self.statusbar.setObjectName(u"statusbar")
        Snakes.setStatusBar(self.statusbar)

        self.retranslateUi(Snakes)

        QMetaObject.connectSlotsByName(Snakes)
    # setupUi

    def retranslateUi(self, Snakes):
        Snakes.setWindowTitle(QCoreApplication.translate("Snakes", u"MainWindow", None))
        self.exitButton.setText(QCoreApplication.translate("Snakes", u"Exit", None))
        self.startButton.setText(QCoreApplication.translate("Snakes", u"Start", None))
        self.onePlayer.setText(QCoreApplication.translate("Snakes", u"1", None))
        self.playersLabel.setText(QCoreApplication.translate("Snakes", u"Number of players:", None))
        self.twoPlayers.setText(QCoreApplication.translate("Snakes", u"2", None))
        self.resetButton.setText(QCoreApplication.translate("Snakes", u"Reset", None))
        self.pauseButton.setText(QCoreApplication.translate("Snakes", u"Pause", None))
        self.pointsLabel.setText(QCoreApplication.translate("Snakes", u"Points", None))
        self.playerOnePointsLabel.setText(QCoreApplication.translate("Snakes", u"Player 1", None))
        self.playerTwoPointsLabel.setText(QCoreApplication.translate("Snakes", u"Player 2", None))
        self.button_multiplayer.setText(QCoreApplication.translate("Snakes", u"Multiplayer", None))
        self.replayButton.setText(QCoreApplication.translate("Snakes", u"Replay", None))
        self.savejsonButton.setText(QCoreApplication.translate("Snakes", u"Save json", None))
        self.readjsonButton.setText(QCoreApplication.translate("Snakes", u"Read json", None))
        self.botButton.setText(QCoreApplication.translate("Snakes", u"vs. AI", None))
    # retranslateUi

