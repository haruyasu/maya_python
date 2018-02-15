import maya.cmds as mc
import maya.mel as mel
import pymel.core as pm

from PySide2.QtGui import *
from PySide2.QtWidgets import *
from functools import partial

import maya.OpenMayaUI as mui
import shiboken2

class className():
    def __init__(self):
        self.varA = 1
        self.varB = 2
        self.varC = 0

    def defA(self):
        self.varC += self.varA + self.varB

    def defB(self, userName):
        if self.varC == None:
            return

        print("Hi " + userName + ", Thank you!!")
        print("varC is equal to " + str(self.varC))

cn = className()

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(pointer), QWidget)

objectName = "pyMyWin"

if mc.window("pyMyWin", exists=True):
    mc.deleteUI("pyMyWin", wnd=True)

parent = getMayaWindow()
window = QMainWindow(parent)
window.setObjectName(objectName)

font = QFont()
font.setPointSize(12)
font.setBold(True)

widget = QWidget()
window.setCentralWidget(widget)

layout = QVBoxLayout(widget)

button = QPushButton("A + B")
layout.addWidget(button)
button.setFont(font)
button.setMinimumSize(200, 40)
button.setMaximumSize(200, 40)
button.setStyleSheet("background-color: rgb(128, 128, 128); color: rgb(0, 0, 0)")
button.clicked.connect(partial(cn.defA))

button2 = QPushButton("Print C")
layout.addWidget(button2)
button2.setFont(font)
button2.setMinimumSize(200, 40)
button2.setMaximumSize(200, 40)
button2.setStyleSheet("background-color: rgb(128, 128, 128); color: rgb(0, 0, 0)")
button2.clicked.connect(partial(cn.defB, "Haru"))

closeButton = QPushButton("Close")
layout.addWidget(closeButton)
closeButton.setFont(font)
closeButton.clicked.connect(window.close)

window.show()
