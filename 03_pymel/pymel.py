import pymel.core as pm
import maya.cmds as cmds

def toggleRenderLayer(*arg):
    renderLayerName = pm.textScrollList("renderLayer", query=True, selectItem=True)
    val = cmds.getAttr("%s.renderable" % renderLayerName[0])
    if val:
        cmds.setAttr("%s.renderable" % renderLayerName[0], 0)
    else:
        cmds.setAttr("%s.renderable" % renderLayerName[0], 1)

pm.window(title="Demo", width=200)
pm.columnLayout(adjustableColumn=True)

renderLayerList = cmds.ls(type="renderLayer")
pm.textScrollList("renderLayer", append=renderLayerList)
pm.button(label="On / Off Render Layer", command=toggleRenderLayer)
pm.showWindow()
