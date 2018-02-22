# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import os, glob, collections
from itertools import chain

def getScriptList():
    scripts = collections.OrderedDict()

    scriptPath = "F:\maya_python"

    files = os.listdir(scriptPath)
    files.sort()

    extList = ["py", "mel"]

    for f in files:
        if f == 'lib': continue
        path = os.path.join(scriptPath, f)
        if os.path.isdir(path):
            scripts[f] = list(chain.from_iterable([glob.glob(os.path.join(path, '*.' + ext)) for ext in extList]))

    return scripts

def loadScript(category, fullpath):
    path = os.path.basename(os.path.dirname(__file__)) + '/' + category + '/' + os.path.basename(fullpath)
    mel.eval('source "' + path + '";')

def getIcon(path, ext):
    iconPath = path.replace(ext, '.png')
    iconPath = iconPath.replace(os.sep, '/')

    if os.path.exists(iconPath):
        return iconPath
    else:
        return False

def getAnnotation(path, ext):
    textPath = path.replace(ext, '.txt')

    if os.path.exists(textPath):
        with open(textPath) as f:
            lines = f.readlines()
            return lines[0]
    else:
        return False

def main():
    menuName = "Script"

    pkyTools = getScriptList()

    if cmds.menu(menuName, ex=True):
        cmds.deleteUI(menuName)

    cmds.menu(menuName, label=menuName, parent='MayaWindow', tearOff=True)

    for category in pkyTools:
        cmds.menuItem(label=category, tearOff=True, subMenu=True)

        for scriptPath in pkyTools[category]:
            scriptName = os.path.splitext(os.path.basename(scriptPath))[0]
            if scriptName == '__init__': continue

            ext = os.path.splitext(scriptPath)[1]

            icon = getIcon(scriptPath, ext)
            icon = '-i "%s"' % icon if icon else ''

            ann = getAnnotation(scriptPath, ext)
            ann = '-ann "%s"' % ann.rstrip() if ann else ''

            if ext == '.py':
                pyName = '%s.%s.%s' % (menuName, category, scriptName)
                pyCmd = 'python(\\"import %s; %s.main();\\")' % (pyName, pyName)
                cmd = 'menuItem -l "%s" %s %s -c "%s";' % (scriptName, icon, ann, pyCmd)
            elif ext == '.mel':
                loadScript(category, scriptPath)
                cmd = 'menuItem -l "%s" %s %s -c "%s";' % (scriptName, icon, ann, scriptName)

            mel.eval(cmd)

        cmds.setParent('..', menu=True)

main()