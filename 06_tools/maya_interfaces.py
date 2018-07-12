import maya.cmds as cmds
import os

widgets = {}
def UI():
    if cmds.window("exampleToolbar", exists=True):
        cmds.deleteUI("exampleToolbar")

    widgets["window"] = cmds.window("exampleToolbar", w=150, h=700, mnb=False, mxb=False, title="Toolbar")
    widgets["scrollLayout"] = cmds.scrollLayout(hst=0)
    widgets["mainLayout"] = cmds.columnLayout(adj=True, parent=widgets["scrollLayout"])

    # find icons and create symbol button for each icon
    populateIcons()

    cmds.showWindow(widgets["window"])
    cmds.window(widgets["window"], edit=True, w=150, h=700, sizeable=False)

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
        widgets[(niceName + "_button")] = cmds.symbolButton(w=50, h=50, image=(IconPath + icon), parent=widgets[(category + "_mainLayout")])


UI()
