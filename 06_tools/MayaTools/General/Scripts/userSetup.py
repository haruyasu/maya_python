# Documents/maya/scripts
# if you create a new scene, it happens.
import maya.cmds as cmds
import os, sys

# def test():
#     cmds.warning("This is a test")
#
# scriptJobNum = cmds.scriptJob(event=["NewSceneOpened", test])

def mayaToolsInstall_UI():
    if cmds.window("mayaToolsInstall_UI", exists=True):
        cmds.deleteUI("mayaToolsInstall_UI")

    window = cmds.window("mayaToolsInstall_UI", title="Maya Tools Install", w=300, h=110, titleBarMenu=False, sizeable=False)

    mainLayout = cmds.columnLayout(w=300, h=110)
    formLayout = cmds.formLayout(w=300, h=110)

    text = cmds.text(label="ERROR: Could not find Maya Tools directory. \nPlease locate using the \"Browse\" button.", w=300)
    cancelButton = cmds.button(label="Cancel", w=140, h=50, c=mayaToolsInstall_Cancel)
    browseButton = cmds.button(label="Browse", w=140, h=50, c=mayaToolsInstall_Browse)
    cmds.formLayout(formLayout, edit=True, af=[(text, "left", 10), (text, "top", 10)])
    cmds.formLayout(formLayout, edit=True, af=[(cancelButton, "left", 5), (cancelButton, "top", 50)])
    cmds.formLayout(formLayout, edit=True, af=[(browseButton, "right", 5), (browseButton, "top", 50)])

    cmds.showWindow(window)
    cmds.window(window, edit=True, w=300, h=110)

def mayaToolsInstall_Browse(*args):
    mayaToolsDir = cmds.fileDialog2(dialogStyle=2, fileMode=3)[0]

    # confirm that this is in fact the maya tools directory
    if mayaToolsDir.rpartition("/")[2] != "MayaTools":
        cmds.warning("Selected directory is not the MayaTools directory. Please try again.")
    else:
        cmds.deleteUI("mayaToolsInstall_UI")

        # create the text file that contains the maya tools directory path
        path = cmds.internalVar(upd=True) + "MayaTools.txt"

        f = open(path, "w")
        f.write(mayaToolsDir)
        f.close()

        # run setup
        import mayaSetup
        mayaSetup.setupTools()

def mayaToolsInstall_Cancel(*args):
    cmds.deleteUI("mayaToolsInstall_UI")

def mayaTools():
    path = cmds.internalVar(upd=True) + "mayaTools.txt"
    if os.path.exists(path):
        f = open(path, "r")
        mayaToolsDir = f.readline()

        path = mayaToolsDir + "/General/Scripts"

        if os.path.exists(path):
            if not path in sys.path:
                sys.path.append(path)
        # run setup
        import mayaSetup
        mayaSetup.setupTools()
    else:
        mayaToolsInstall_UI()

scriptJobNum = cmds.scriptJob(event=["NewSceneOpened", mayaTools])
