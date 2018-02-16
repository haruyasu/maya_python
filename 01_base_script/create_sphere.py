import maya.cmds as mc

x_slider = ""
y_slider = ""
z_slider = ""

def createPolySphere(*args):
    mc.polySphere(r=1, sx=20, ax=(0, 1, 0), cuv=2, ch=1)
    x_value = mc.floatSliderGrp(x_slider_name, q=True, value=True)
    y_value = mc.floatSliderGrp(y_slider_name, q=True, value=True)
    z_value = mc.floatSliderGrp(z_slider_name, q=True, value=True)
    mc.move(x_value, y_value, z_value, r=True)

window = mc.window(title="Polygon Sphere GUI", widthHeight=(200, 55))
mc.columnLayout(adjustableColumn=True)

x_slider_name = mc.floatSliderGrp(label="Move X", field=True, minValue=-10.0, maxValue=10.0, value=0.0)
y_slider_name = mc.floatSliderGrp(label="Move Y", field=True, minValue=-10.0, maxValue=10.0, value=0.0)
z_slider_name = mc.floatSliderGrp(label="Move Z", field=True, minValue=-10.0, maxValue=10.0, value=0.0)
mc.button(label="Create Polygon Sphere", command=createPolySphere)
mc.button(label="Close", command=('mc.deleteUI(\"' + window + '\", window=True)'))
mc.setParent('..')
mc.showWindow(window)
