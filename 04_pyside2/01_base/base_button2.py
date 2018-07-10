try:
  from PySide2.QtCore import *
  from PySide2.QtGui import *
  from PySide2.QtWidgets import *
  from PySide2 import __version__
  from shiboken2 import wrapInstance
except ImportError:
  from PySide.QtCore import *
  from PySide.QtGui import *
  from PySide import __version__
  from shiboken import wrapInstance
import maya.OpenMayaUI as mui
import maya.cmds as mc

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return wrapInstance(long(pointer), QWidget)

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
