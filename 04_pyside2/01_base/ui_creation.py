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
import maya.cmds as cmds

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return wrapInstance(long(pointer), QWidget)

def createConstraintLayout(label, parentLayout):



def constraintMaster_UI():
    objectName = "pyConstraintMasterWin"

    # check to see if the UI already exists and if so, delete
    if cmds.window(objectName, exists=True):
        cmds.deleteUI(objectName, wnd=True)

    # create the window
    parent = getMayaWindow()
    window = QMainWindow(parent)
    window.setObjectName(objectName)
    window.setWindowTitle("Constraint Master")

    # create the main widget
    mainWidget = QWidget()
    window.setCentralWidget(mainWidget)

    # create our main vertical layout
    verticalLayout = QVBoxLayout(mainWidget)

    # create the translate layout
    translateLayout = QHBoxLayout()
    verticalLayout.addLayout(translateLayout)

    # translate items: label, tx, checkbox, ty, tz, maintain offsets
    translateLabel = QLabel("Translate:")
    translateLayout.addWidget(translateLabel)
    font = QFont()
    font.setPointSize(10)
    font.setBold(True)
    translateLabel.setFont(font)

    # add spacer
    spacer = QSpacerItem(30, 0)
    translateLayout.addSpacerItem(spacer)

    txCheckBox = QCheckBox("X")
    translateLayout.addWidget(txCheckBox)
    txCheckBox.setMinimumWidth(30)
    txCheckBox.setMaximumWidth(30)
    txCheckBox.setChecked(True)

    tyCheckBox = QCheckBox("Y")
    translateLayout.addWidget(tyCheckBox)
    tyCheckBox.setMinimumWidth(30)
    tyCheckBox.setMaximumWidth(30)
    tyCheckBox.setChecked(True)

    tzCheckBox = QCheckBox("Z")
    translateLayout.addWidget(tzCheckBox)
    tzCheckBox.setMinimumWidth(30)
    tzCheckBox.setMaximumWidth(30)
    tzCheckBox.setChecked(True)

    # add spacer
    spacer = QSpacerItem(50, 0)
    translateLayout.addSpacerItem(spacer)

    offsetCheckbox = QCheckBox("Maintain Offsets")
    translateLayout.addWidget(offsetCheckbox)

    # create the rotete layout
    rotateLayout = QHBoxLayout()
    verticalLayout.addLayout(rotateLayout)

    # create the scale layout
    scaleLayout = QHBoxLayout()
    verticalLayout.addLayout(scaleLayout)

    # create the "create" button
    button = QPushButton("Create Constraint")
    verticalLayout.addWidget(button)

    # show the window
    window.show()

constraintMaster_UI()
