from PySide2.QtGui import *
import maya.OpenMayaUI as mui
import shiboken2
import maya.cmds as mc

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(pointer), QWidget)

def createLocator():
    mc.spaceLocator()

objectName = "pyMyWin"

# check for existing window
if mc.window(objectName, exists=True):
    mc.deleteUI(objectName, wnd=True)

# create a window
parent = getMayaWindow()
window = QMainWindow(parent)
window.setObjectName(objectName)

# create a font
font = QFont()
font.setPointSize(12)
font.setBold(True)

# create a widget
widget = QWidget()
window.setCentralWidget(widget)

# create a layout
layout = QVBoxLayout(widget)

# create button
button = QPushButton("Create Locator")
layout.addWidget(button)
button.setFont(font)
# button.setMinimumSize(200, 40)
# button.setMaximumSize(200, 40)
button.clicked.connect(createLocator)

# create close button
closeButton = QPushButton("Close")
layout.addWidget(closeButton)
closeButton.setFont(font)
closeButton.clicked.connect(window.close)

# show the button
window.show()
