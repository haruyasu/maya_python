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

def createConstraintLayout(attribute, parentLayout, checked):
    # create add the horizontal layout
    layout = QHBoxLayout()
    parentLayout.addLayout(layout)

    # create label
    label = QLabel(attribute)
    layout.addWidget(label)

    # create font and assign
    font = QFont()
    font.setPointSize(10)
    font.setBold(True)
    label.setFont(font)

    # add spacer
    spacer = QSpacerItem(30, 0)
    layout.addSpacerItem(spacer)

    # loop through attribute and create a checkbox for each one
    for attr in ["X", "Y", "Z"]:
        checkbox = QCheckBox(attr)
        objectName = attribute.partition(":")[0] + attr + "_cmCheckBox"
        checkbox.setObjectName(objectName)
        checkbox.setChecked(checked)
        layout.addWidget(checkbox)
        checkbox.setMinimumWidth(30)
        checkbox.setMaximumWidth(30)

    # create spacer and maintain offsets checkbox
    spacer = QSpacerItem(50, 0)
    layout.addSpacerItem(spacer)

    offsetCheckbox = QCheckBox("Maintain Offsets")
    objectName = attribute.partition(":")[0] + "_cmCheckBox_offset"
    offsetCheckbox.setObjectName(objectName)
    layout.addWidget(offsetCheckbox)

def createConstrain():
    # get selection
    selection = cmds.ls(sl=True)
    if len(selection) > 0:
        constraintObj = selection[0]
        targetObj = selection[1]

    # get checkbox values
    for attribute in ["Translate", "Rotate", "Scale"]:
        skipList = []
        for attr in ["X", "Y", "Z"]:
            if cmds.control(attribute + attr + "_cmCheckBox", exists=True):
                ptr = mui.MQtUtil.findControl(attribute + attr + "_cmCheckBox")
                checkBox = wrapInstance(long(ptr), QCheckBox)
                value = checkBox.isChecked()
                if not value:
                    skipList.append(attr.lower())

        maintainOffset = False
        # maintain offsets
        if cmds.control(attribute + "_cmCheckBox_offset", exists=True):
            ptr = mui.MQtUtil.findControl(attribute + "_cmCheckBox_offset")
            checkBox = wrapInstance(long(ptr), QCheckBox)
            maintainOffset = checkBox.isChecked()


        # create constraint
        if len(skipList) != 3:
            if attribute == "Translate":
                cmds.pointConstraint(constraintObj, targetObj, skip=skipList, mo=maintainOffset)
            if attribute == "Rotate":
                cmds.orientConstraint(constraintObj, targetObj, skip=skipList, mo=maintainOffset)
            if attribute == "Scale":
                cmds.scaleConstraint(constraintObj, targetObj, skip=skipList, mo=maintainOffset)

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
    window.setMinimumSize(400, 125)
    window.setMaximumSize(400, 125)

    # create the main widget
    mainWidget = QWidget()
    window.setCentralWidget(mainWidget)

    # create our main vertical layout
    verticalLayout = QVBoxLayout(mainWidget)

    # loop throught the attributes, create layout
    for attribute in ["Translate:", "Rotate:", "Scale:"]:
        if attribute == "Scale:":
            createConstraintLayout(attribute, verticalLayout, False)
        else:
            createConstraintLayout(attribute, verticalLayout, True)

    # create the "create" button
    button = QPushButton("Create Constraint")
    verticalLayout.addWidget(button)
    button.clicked.connect(createConstrain)

    # show the window
    window.show()

constraintMaster_UI()
