import pymel.core as pm

def createPolySphere(x_slider, y_slider, z_slider):
    def cmd(*args):
        sphere = pm.polySphere(r=1, sx=20, sy=20, ax=(0, 1, 0), cuv=2, ch=1)[0]
        x_value = x_slider.getValue()
        y_value = y_slider.getValue()
        z_value = z_slider.getValue()
        sphere.setTranslation((x_value, y_value, z_value))
    return cmd

with pm.window(title="Polygon Sphere GUI", widthHeight=(200, 55)) as polysphere_gui:
    def closeWin(*args):
        polysphere_gui.delete()

    with pm.columnLayout():
        x_slider = pm.floatSliderGrp(label="Move X", field=True, minValue=-10.0, maxValue=10.0, value=0.0)
        y_slider = pm.floatSliderGrp(label="Move Y", field=True, minValue=-10.0, maxValue=10.0, value=0.0)
        z_slider = pm.floatSliderGrp(label="Move Z", field=True, minValue=-10.0, maxValue=10.0, value=0.0)

        pm.button(label="Create Polygon Sphere", command=createPolySphere(x_slider, y_slider, z_slider))
        pm.button(label="Close", command=closeWin)
    
