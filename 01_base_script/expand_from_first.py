import maya.cmds as mc

selectionList = mc.ls(orderedSelection=True, type="transform")

if len(selectionList) >= 2:
    targetName = selectionList[0]
    selectionList.remove(targetName)
    locatorGroupName = mc.group(empty=True, name="expansion_locator_grp#")
    maxExpansion = 100
    newAttributeName = "expansion"

    if not mc.objExists("%s.%s" % (targetName, newAttributeName)):
        mc.select(targetName)
        mc.addAttr(longName=newAttributeName,
                    shortName="exp",
                    attributeType="double",
                    min=0, max=maxExpansion,
                    defaultValue=maxExpansion,
                    keyable=True)

        for objectName in selectionList:
            coords = mc.getAttr("%s.translate" % objectName)[0]
            locatorName = mc.spaceLocator(position=coords,
                                            name="%s_loc#" % objectName)[0]
            mc.xform(locatorName, centerPivots=True)
            mc.parent(locatorName, locatorGroupName)
            pointConstraintName = mc.pointConstraint([targetName, locatorName],
                                                        objectName,
                                                        name="%s_pointConstraint#" % objectName)[0]
            mc.expression(alwaysEvaluate=True,
                            name="%s_attractWeight" % objectName,
                            object=pointConstraintName,
                            string="%sW0=%s-%s.%s" % (targetName, maxExpansion, targetName, newAttributeName))
            mc.connectAttr("%s.%s" % (targetName, newAttributeName),
                            "%s.%sW1" % (pointConstraintName, locatorName))

        mc.xform(locatorGroupName, centerPivots=True)
else:
    print "Please select two or more objects."
