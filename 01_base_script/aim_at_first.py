import maya.cmds as mc

selectionList = mc.ls(orderedSelection=True)

if len(selectionList) >= 2:
    print "Selected items: %s" % selectionList
    targetName = selectionList[0]
    selectionList.remove(targetName)

    for objectName in selectionList:
        print "Constraining %s towards %s" % (objectName, targetName)
        mc.aimConstraint(targetName, objectName, aimVector=[0, 1, 0])
else:
    print "Please select two or more objects."
