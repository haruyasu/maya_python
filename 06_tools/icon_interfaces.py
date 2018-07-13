import maya.cmds as cmds
import os
from functools import partial
import maya.mel as mel

widgets = {}
def UI():
    if cmds.dockControl("toolbar_Dock", exists=True):
        cmds.deleteUI("toolbar_Dock")

    widgets["window"] = cmds.window(mnb=False, mxb=False, title="Toolbar")
    widgets["scrollLayout"] = cmds.scrollLayout(hst=0)
    widgets["mainLayout"] = cmds.columnLayout(adj=True, parent=widgets["scrollLayout"])

    # find icons and create symbol button for each icon
    populateIcons()

    # create a dock
    widgets["dock"] = cmds.dockControl("toolbar_Dock", label="Toolbar" area="left", content=widgets["window"], allowedArea="left")


def populateIcons():
    IconPath = cmds.internalVar(upd=True) + "icons/Tools/"
    icons = os.listdir(IconPath)

    categories = []
    for icon in icons:
        categoryName = icon.partition("__")[0]
        categories.append(categoryName)

    categoryNames = list(set(categories))

    for name in categoryNames:
        # create a frameLayout
        widgets[(name + "_frameLayout")] = cmds.frameLayout(label=name, collapsable=True, parent=widgets["mainLayout"])
        widgets[(name + "_mainLayout")] = cmds.rowColumnLayout(nc=3, parent=widgets[(name + "_frameLayout")])


    for icon in icons:
        niceName = icon.partition(".")[0]
        category = icon.partition("__")[0]
        command = icon.partition("__")[2].partition(".")[0]

        widgets[(niceName + "_button")] = cmds.symbolButton(w=50, h=50, image=(IconPath + icon), parent=widgets[(category + "_mainLayout")], c=partial(runMethod, command))

def runMethod(method, *args):
    try:
        exec(method + "()")
    except NameError:
        print "Function dose not exist"

def savePose():
    print "Saving Pose"

def componentEditor():
    mel.eval("componentEditor;")

def sdk():
    mel.eval("setDrivenKeyWindow \"\" {};")

def deleteHistory():
    selection = cmds.ls(sl=True)
    for each in selection:
        cmds.delete(ch=True)

UI()
