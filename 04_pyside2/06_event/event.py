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

class SetEventWindow(QMainWindow):
    def __init__(self):
        super(SetEventWindow, self).__init__(parent)

    def closeEvent(self, event):
        print "coloseWindow"

    def resizeEvent(self, event):
        ex = ui
        print "resize width:%s height:%s" % (ex.width(), ex.height())

    def hideEvent(self, event):
        print "hide"

    def enterEvent(self, event):
        print "enter"

    def leaveEvent(self, event):
        print "leave"

    def showEvent(self, event):
        print "show"

class drapEventWindow(SetEventWindow):
    def __init__(self):
        super(drapEventWindow, self).__init__()

    def dragEnterEvent(self, event):
        event.accept()
        print('dragEnterEvent')

    def dragLeaveEvent(self, event):
        event.accept()
        print('dragLeaveEvent')

    def dragMoveEvent(self, event):
        event.accept()
        print('dragMoveEvent')

    def dropEvent(self, event):
        event.accept()
        print('dropEvent')

class keyEventWindow(drapEventWindow):
    def __init__(self):
        super(keyEventWindow, self).__init__()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            print "keyPressEvent"
        event.accept()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Q:
            print "keyReleaseEvent"
        event.accept()

class mouseEventWindow(keyEventWindow):
    def __init__(self):
        super(mouseEventWindow, self).__init__()

    def mouseDoubleClickEvent(self, event):
        print "mouseDoubleClick"

    def mouseMoveEvent(self, event):
        print "mouseMove"

    def mousePressEvent(self, event):
        print "mousePress"

    def mouseReleaseEvent(self, event):
        print "mouseRelease"

    def moveEvent(self, event):
        ex = ui
        print "move x:%s y:%s" % (ex.pos().x(), ex.pos().y())

class MyLineEdit(QLineEdit):
    def __init__(self):
        super(MyLineEdit, self).__init__()

    def focusInEvent(self, event):
        self.selectAll()
        print "focusInEvent"

    def focusNextPrevChild(self, event):
        self.selectAll()
        print "focusNextPrevChild"

    def focusOutEvent(self, event):
        self.selectAll()
        print "focusOutEvent"

class Gui(QWidget):
    def __init__(self):
        super(Gui, self).__init__()
        self.btn = QPushButton("resize", self)
        self.btn.setMinimumWidth(50)
        self.line1 = MyLineEdit()
        self.line2 = MyLineEdit()

        layout = QVBoxLayout(self)
        layout.addWidget(self.btn)
        layout.addWidget(self.line1)
        layout.addWidget(self.line2)

        self.btn.clicked.connect(self.resizeWindow)

    def resizeWindow(self):
        ex = ui
        width = ex.width()
        geo = self.geometry()
        if width == 200:
            ui.resize(600, 300)
        else:
            ui.resize(200, 300)

class Example(mouseEventWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.setCentralWidget(Gui())
        self.setWindowTitle('Example')
        self.resize(200, 300)
        self.move(400, 400)
        self.setAcceptDrops(True)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        self.frameGeometry().moveCenter(QDesktopWidget().availableGeometry().center())
        self.x = 0
        self.y = 5

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(Qt.red)
        self.x += 1
        if self.x > 120:
            self.x = 0
        elif self.x % 20 == 0:
            print "paintEvent x:%s" % self.x
        painter.drawRect(self.x, self.y, 10, 10)

def main():
    global ui
    app = QApplication.instance()
    ui = Example()
    ui.show()
    sys.exit()
    app.exec_()

main()