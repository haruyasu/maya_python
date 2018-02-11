import maya.cmds as mc

string = objAligner

if mc.window(objAligner, ex=True):
    mc.deleteUI(objAligner, window=True)

objAligner = mc.window(title="Object Aligment Tool", s=False, wh=(300, 100))
mc.columnLayout(adj=True)
mc.text(l="Instructions: select source, then target")
mc.button(l="Go Aligner Go!", w=300, h=100, c="aligner()")
mc.showWindow(objAligner)

def aligner():
    prtCns = mc.parentConstraint()
    mc.delete(prtCns)
