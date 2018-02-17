import maya.cmds as mc
import functools

def createUI(pWindowTitle, pApplyCallback):
    windowID = "myWindowID"

    if mc.window(windowID, exists=True):
        mc.deleteUI(windowID)

    mc.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True)
    mc.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 75), (2, 60), (3, 60)], columnOffset=[(1, "right", 3)])
    mc.text(label="Time Range:")
    startTimeField = mc.intField(value=mc.playbackOptions(q=True, minTime=True))
    endTimeField = mc.intField(value=mc.playbackOptions(q=True, maxTime=True))
    mc.text("Attribute:")
    targetAttributeField = mc.textField(text="rotateY")
    mc.separator(h=10, style="none")
    mc.separator(h=10, style="none")
    mc.separator(h=10, style="none")
    mc.separator(h=10, style="none")
    mc.separator(h=10, style="none")
    mc.button(label="Apply", command=functools.partial(pApplyCallback, startTimeField, endTimeField, targetAttributeField))

    def cancelCallback(*pArgs):
        if mc.window(windowID, exists=True):
            mc.deleteUI(windowID)

    mc.button(label="Cancel", command=cancelCallback)
    mc.showWindow()

def keyFullRotation(pObjectName, pStartTime, pEndTime, pTargetAttribute):
    mc.cutKey(pObjectName, time=(pStartTime, pEndTime), attribute=pTargetAttribute)
    mc.setKeyframe(pObjectName, time=pStartTime, attribute=pTargetAttribute, value=0)
    mc.setKeyframe(pObjectName, time=pEndTime, attribute=pTargetAttribute, value=360)
    mc.selectKey(pObjectName, time=(pStartTime, pEndTime), attribute=pTargetAttribute, keyframe=True)
    mc.keyTangent(inTangentType="linear", outTangentType="linear")

def applyCallback(pStartTimeField, pEndTimeField, pTargetAttributeField, *pArgs):
    startTime = mc.intField(pStartTimeField, query=True, value=True)
    endTime = mc.intField(pEndTimeField, query=True, value=True)
    targetAttribute = mc.textField(pTargetAttributeField, query=True, text=True)

    print "Start Time: %s" % startTime
    print "End Time: %s" % endTime
    print "Attribute: %s" % targetAttribute

    selectionList = mc.ls(selection=True, type="transform")

    for objectName in selectionList:
        keyFullRotation(objectName, startTime, endTime, targetAttribute)

createUI("My Title", applyCallback)
