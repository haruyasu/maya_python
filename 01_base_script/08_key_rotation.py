import maya.cmds as mc

def keyFullRotation(pObjectName, pStartTime, pEndTime, pTargetAttribute):
    mc.cutKey(pObjectName, time=(pStartTime, pEndTime), attribute=pTargetAttribute)
    mc.setKeyframe(pObjectName, time=pStartTime, attribute=pTargetAttribute, value=0)
    mc.setKeyframe(pObjectName, time=pEndTime, attribute=pTargetAttribute, value=360)
    mc.selectKey(pObjectName, time=(pStartTime, pEndTime), attribute=pTargetAttribute, keyframe=True)
    mc.keyTangent(inTangentType="linear", outTangentType="linear")

selectionList = mc.ls(selection=True, type="transform")

if len(selectionList) >= 1:
    startTime = mc.playbackOptions(query=True, minTime=True)
    endTime = mc.playbackOptions(query=True, maxTime=True)

    for objectName in selectionList:
        keyFullRotation(objectName, startTime, endTime, "rotateY")
else:
    print "Please select at least one object"
