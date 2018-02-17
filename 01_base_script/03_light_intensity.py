import maya.cmds as mc

def scale_light_intensity(percentage=1.0):
    all_lights = mc.ls(type="light") or []

    for light in all_lights:
        current_intensity = mc.getAttr("{0}.intensity".format(light))
        new_intensity = current_intensity * percentage
        mc.setAttr("{0}.intensity".format(light), new_intensity)
        print "Changed the intensity of light {0} from {1:.3f} to {2:.3f}".format(light, current_intensity, new_intensity)

scale_light_intensity(1.2)
