import re
import os
import sys

import maya.cmds as cmds
import pymel.core as pm
from maya import OpenMayaUI

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import shiboken2 as shiboken

ptr = OpenMayaUI.MQtUtil.mainWindow()
parent = shiboken.wrapInstance(long(ptr), QWidget)

class setMainWindow(QMainWindow):
    def __init__(self):
        super(setMainWindow, self).__init__(parent)

    def mouseReleaseEvent(self, pos):
        self.mc_x = pos.x()
        self.mc_y = pos.y()

    def mousePressEvent(self, pos):
        self.mc_x = pos.x()
        self.mc_y = pos.y()

    def mouseMoveEvent(self, pos):
        winX = pos.globalX() - self.mc_x
        winY = pos.globalY() - self.mc_y
        self.move(winX, winY)


class Gui(setMainWindow):
    def __init__(self):
        super(Gui, self).__init__()
        self.initUI()
        self.setButton()
        self.paletteUI()

    def initUI(self):
        self.setWindowOpacity(0.85)
        self.setGeometry(300, 300, 200, 150)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

    def setButton(self):
        btn = QPushButton("Close", self)
        btn.move(50, 50)
        btn.clicked.connect(self.close)

    def paletteUI(self):
        setColors = ['#54354e', '#6a86c7']

        Palette = QPalette()
        gradient = QLinearGradient(QRectF(self.rect()).topLeft(), QRectF(self.rect()).topRight())
        gradient.setColorAt(0.0, setColors[0])
        gradient.setColorAt(1.0, setColors[1])
        Palette.setBrush(QPalette.Background, QBrush(gradient))
        self.setPalette(Palette)

        path = QPainterPath()
        path.addRoundedRect(self.rect(), 10, 10)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)


def main():
    global ui
    app = QApplication.instance()
    ui = Gui()
    ui.show()
    sys.exit()
    app.exec_()

main()