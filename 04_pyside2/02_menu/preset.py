from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import maya.cmds as mc
import maya.mel as mel
import os
import glob
import re
from functools import partial

import pymel.core as pm
import maya.OpenMayaUI as mui
import shiboken2

class QPresetMenuButton(QPushButton):
    (
     REPLACE,
     REPLACE_ALL,
     BLEND90,
     BLEND75,
     BLEND50,
     BLEND25,
     BLEND10
    ) = range(0,7)

    _parent = None

    def __init__(self, parent=None, text='Preset'):
        super(QPresetMenuButton,self).__init__(parent)

        self._parent = parent
        if text:
            self.setText(text)

        self.clicked.connect(self.contextMenu)

    def contextMenu(self):
        def addAction(self, menu, name, func):
            action = QAction(name,self)
            action.triggered.connect(partial(func,menu.num))
            menu.addAction(action)

        items = (('Replace', self.replace),
                 ('Replace All Selected', self.replaceAll),
                 ('Blend 90%', partial(self.blend, self.BLEND90)),
                 ('Blend 75%', partial(self.blend, self.BLEND75)),
                 ('Blend 50%', partial(self.blend, self.BLEND50)),
                 ('Blend 25%', partial(self.blend, self.BLEND25)),
                 ('Blend 10%', partial(self.blend, self.BLEND10)))

        node = mc.ls(sl=True)
        if node:
            paths, _type = self.getPresetPaths(node[0])
            presets = self.getPresetNames(paths)
            self.paths = paths

            menu = QMenu(self)
            action = QAction('%s : %s'%(_type,node[0]),self)
            menu.addAction(action)

            num = 0
            for preset in presets:
                submenu = menu.addMenu(preset)
                submenu.num = num
                num += 1
                for name, func in items:
                    addAction(self, submenu, name, func)

            point = QCursor.pos()
            menu.exec_(point)

    def replace(self, num):
        print '# Replace'
        nodes = mc.ls(sl=True)
        if nodes:
            applyPreset(nodes[0], self.paths[num], REPLACE)

    def replaceAll(self, num):
        print '# Replace All Selected'
        nodes = mc.ls(sl=True)
        if nodes:
            mc.undoInfo(ock=True)
            for node in nodes:
                applyPreset(node, self.paths[num], REPLACE_ALL)
            mc.undoInfo(cck=True)

    def blend(self, value, num):
        val = {BLEND90:'90',BLEND75:'75',BLEND50:'50',BLEND25:'25',BLEND10:'10'}[value]
        print '# Blend %s%%'%val
        nodes = mc.ls(sl=True)
        if nodes:
            applyPreset(nodes[0], self.paths[num], value)

    def getPresetPaths(self,node):
        paths = []
        _type = mc.nodeType(node)

        env = os.environ['MAYA_LOCATION']
        ppath = env + '/presets/attrPresets/' + _type
        paths.extend(glob.glob(ppath+'/*.mel'))

        env = os.environ['MAYA_PRESET_PATH']
        envs = env.split(';')
        for env in envs:
            ppath = env + '/attrPresets/' + _type
            paths.extend(glob.glob(ppath+'/*.mel'))

        env = mc.internalVar(userPrefDir=True)
        env = env.replace('/prefs','/presets/attrPresets')
        ppath = env + _type
        paths.extend(glob.glob(ppath+'/*.mel'))

        paths = [i.replace('\\','/') for i in paths]

        return paths, _type

    def applyPreset(self, node, path, mode):
        cmd = ' "%s" "" "" "%s" '%(node,path)
        if mode == REPLACE:
            mel.eval('applyPresetToNode' + cmd + '1')
        elif mode ==  REPLACE_ALL:
            mel.eval('applyPresetToSelectedNodes' + cmd + '1')
        elif mode == BLEND90:
            mel.eval('applyPresetToNode' + cmd + '.9')
        elif mode == BLEND75:
            mel.eval('applyPresetToNode' + cmd + '.75')
        elif mode == BLEND50:
            mel.eval('applyPresetToNode' + cmd + '.51')
        elif mode == BLEND25:
            mel.eval('applyPresetToNode' + cmd + '.25')
        elif mode == BLEND10:
            mel.eval('applyPresetToNode' + cmd + '.1')
        else:
            raise ValueError

    def getPresetNames(self, paths):
        names = []
        for i in paths:
            root,ext = os.path.splitext(i)
            names.append(os.path.basename(root))
        return names

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

button3 = QPresetMenuButton()
layout.addWidget(button3)
button3.setFont(font)
button3.setMinimumSize(200, 40)
button3.setMaximumSize(200, 40)
button3.setStyleSheet("background-color: rgb(128, 128, 128); color: rgb(0, 0, 0)")

closeButton = QPushButton("Close")
layout.addWidget(closeButton)
closeButton.setFont(font)
closeButton.clicked.connect(window.close)

window.show()
