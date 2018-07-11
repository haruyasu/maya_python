import maya.cmds as cmds

widgets = {}

def UI():
    if cmds.window("tabTest", exists=True):
        cmds.deleteUI("tabTest")

    widgets["window"] = cmds.window("tabTest", title="Character Tabs Test", w=400, h=600, mxb=False, mnb=False)
    mainLayout = cmds.columnLayout(w=400, h=600)
    widgets["tabLayout"] = cmds.tabLayout(imw=5, imh=5)

    # find all the character namaspaces in the scene, create UI for each
    findNamaSpaces()

    cmds.showWindow(widgets["window"])

def findNamaSpaces():
    cmds.namespace(setNamespace=":")
    namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)

    for namespace in namespaces:
        if cmds.objExists(namespace + ":*"):
            # create a tab
            widgets[(namespace + "_tab")] = cmds.columnLayout(w=400, h=600, parent=widgets["tabLayout"])

            # create attr field grps for translate rotate and scale
            cmds.separator(h=10, style="none")
            widgets[(namespace + "_attrFG_T")] = cmds.attrFieldGrp(attribute=(namespace + ":null.translate"))
            widgets[(namespace + "_attrFG_R")] = cmds.attrFieldGrp(attribute=(namespace + ":null.rotate"))
            widgets[(namespace + "_attrFG_S")] = cmds.attrFieldGrp(attribute=(namespace + ":null.scale"))

            cmds.separator(h=10, style="none")

            widgets[(namespace + "_attrEOM_Vis")] = cmds.attrEnumOptionMenu(label="Test", attribute=(namespace + ":null.Test"))

            # edit the tab name
            cmds.tabLayout(widgets["tabLayout"], edit=True, tabLabel=(widgets[(namespace + "_tab")], namespace))

UI()
