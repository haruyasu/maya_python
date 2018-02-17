import maya.cmds as mc

if mc.window(ram, exists = True):
    mc.deleteUI(ram)

ram = mc.window("RenamerWin", t = "Cube", w=300, h=300, sizeable=False, mnb=False)
mc.columnLayout(adj=True)
# imagePath = mc.internalVar(upd=True) + "img/xxxx.jpg"
# mc.image(w=300, h=100, image=imagePath)
mc.separator(h=10)
mc.text("Welcome to the Tool RENAMER")
mc.separator(h=10)

cubW = mc.intSliderGrp(l="Width", min=0, max=10, field=True)
cubH = mc.intSliderGrp(l="Height", min=0, max=10, field=True)
cubD = mc.intSliderGrp(l="Depth", min=0, max=10, field=True)

mc.button(l="Create a Cube", c="myCube()")
mc.separator(h=10)

cubName = mc.textFieldGrp(l="Renamer", editable=True)
mc.button(l="Rename the Cube", c="myCubeRenamer()")
mc.showWindow(ram)

def myCube():
    myCubeWidth = mc.intSliderGrp(cubW, q=True, value=True)
    myCubeHeight = mc.intSliderGrp(cubH, q=True, value=True)
    myCubeDepth = mc.intSliderGrp(cubD, q=True, value=True)
    finalCube = mc.polyCube(w=myCubeWidth, h=myCubeHeight, d=myCubeDepth, n="Cube")
    mc.move(0, myCubeHeight / 2.0, 0, finalCube, r=True)

def myCubeRenamer():
    finalName = mc.textFieldGrp(cubName, q=True, text=True)
    mc.rename(finalName)
