from PySide2 import QtWidgets, QtGui, QtCore
import maya.OpenMayaUI as mui
import shiboken2

def window():
    return shiboken2.wrapInstance(
        long(mui.MQtUtil.mainWindow()),
        QtWidgets.QWidget
    )

class MainWindow(object):
    def __init__(self):
        self.win = QtWidgets.QDialog(
            parent = window(),
            windowTitle = "Test",
            objectName = "Test"
        )

    def show(self):
        self.win.show()

main = MainWindow()
main.show()