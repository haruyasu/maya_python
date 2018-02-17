import maya.cmds as mc

selCVs = mc.ls(sl=True, fl=True)

selSize_CV = len(selCVs)

for cvs in range(0, selSize_CV, 1):
    findCV_X = mc.getAttr(selCVs[cvs] + ".xValue")
    findCV_Y = mc.getAttr(selCVs[cvs] + ".yValue")
    findCV_Z = mc.getAttr(selCVs[cvs] + ".zValue")
    mc.select(cl=True)
    mkJnt = mc.polyCube()
    mc.setAttr(mkJnt[0] + ".tx", findCV_X)
    mc.setAttr(mkJnt[0] + ".tx", findCV_Y)
    mc.setAttr(mkJnt[0] + ".tx", findCV_Z)
