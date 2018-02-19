from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from maya import cmds
from maya import OpenMayaUI
import shiboken2 as shiboken

class Commands(object):
    def __init__(self):
        self.cmdsDict = {"sphere": self._polySphere,
                         "cube": self._polyCube,
                         "plane": self._polyPlane,
                         "cylinder": self._polyCylinder}

    def _polySphere(self):
        cmds.polySphere()

    def _polyCube(self):
        cmds.polyCube()

    def _polyPlane(self):
        cmds.polyPlane()

    def _polyCylinder(self):
        cmds.polyCylinder()

class Gui(QWidget):
    def __init__(self, parent=None):
        super(Gui, self).__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.Tool)

        self.lineEdit = QLineEdit()
        self.lineEdit.returnPressed.connect(self.execute)

        layout = QBoxLayout(QBoxLayout.TopToBottom)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)
        self.setupCompleter()

    def setupCompleter(self):
        items = {"Sphere", "Cube", "Plane", "Cylinder"}
        completer = QCompleter(items)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEdit.setCompleter(completer)

    def execute(self):
        key = self.lineEdit.text()
        cm = Commands()
        cm.cmdsDict[key.lower()]()
        self.close()

def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(ptr), QWidget)

def main():
    window = Gui(getMayaWindow())
    window.show()

if __name__ == '__main__':
    main()