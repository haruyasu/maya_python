import maya.cmds as mc
import maya.OpenMaya as OpenMaya
import sys
import maya.OpenMayaUI as OpenMayaUI

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    import shiboken2 as shiboken
except:
    from PySide.QtCore import *
    from PySide.QtGui import *
    import shiboken

try :
    import gui_pyside2 as qtGUI ;
    reload(qtGUI)
except:
    import gui_pyside as qtGUI ;
    reload(qtGUI)

class GUI(QMainWindow):
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    parent = shiboken.wrapInstance(long(ptr), QWidget)

    def __init__(self, parent=None):
        super(GUI, self).__init__(self.parent)

        self.ui = qtGUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Base UI")
        self.ui.pushButton.clicked.connect(self.addList)
        self.ui.pushButton_2.clicked.connect(self.printList)
        self.ui.listWidget.itemDoubleClicked.connect(self.doubleClickedList)

    def addList(self):
        getList = mc.ls(sl=True)
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(getList)

    def printList(self):
        getList = self.ui.listWidget.selectedItems()
        print [x.text() for x in getList]

    def doubleClickedList(self):
        getList = self.ui.listWidget.selectedItems()
        mc.select([x.text() for x in getList], r=True)

def main():
    global ui

    try:
        ui.close()
    except:
        pass
    app = QApplication.instance()
    ui = GUI()
    ui.show()
    app.exec_()

main()
