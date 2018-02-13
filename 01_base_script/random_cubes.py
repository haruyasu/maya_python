import maya.cmds as mc
import random

random.seed(1234)

result = mc.polyCube(w=1, h=1, d=1, name="myCube#")

transformName = result[0]

instanceGroupName = mc.group(empty=True, name=transformName + "_instance_grp#")

for i in range(0, 50):
    instanceResult = mc.instance(transformName, name=transformName + "_instance#")
    mc.parent(instanceResult, instanceGroupName)

    x = random.uniform(-10, 10)
    y = random.uniform(0, 20)
    z = random.uniform(-10, 10)

    mc.move(x, y, z, instanceResult)

    xRot = random.uniform(0, 360)
    yRot = random.uniform(0, 360)
    zRot = random.uniform(0, 360)

    mc.rotate(xRot, yRot, zRot, instanceResult)

    scalingFactor = random.uniform(0.3, 1.5)
    mc.scale(scalingFactor, scalingFactor, scalingFactor, instanceResult)

mc.hide(transformName)
mc.xform(instanceGroupName, centerPivots=True)
