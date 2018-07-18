import maya.cmds as cmds
import maya.mel as mel

def customMayaMenu():
    gMainWindow = mel.eval("$temp1 = $gMainWindow")
    customMenu = cmds.menu(parent=gMainWindow, label="Custom Tools")

    riggingTools = cmds.menuItem(parent=customMenu, label="Rigging Tools", subMenu=True)
    cmds.menuItem(parent=riggingTools, label="Batcher", c=batcher)
    cmds.menuItem(parent=riggingTools, label="Character Picker", c=characterPicker)
    cmds.menuItem(parent=riggingTools, label="Paint Skin Weights", c=paintSkinWeights)

    animationTools = cmds.menuItem(parent=customMenu, label="Animation Tools", subMenu=True)
    cmds.menuItem(parent=animationTools, label="Custom Transform")
    cmds.menuItem(parent=animationTools, label="Animation Tool")

def batcher(*args):
    import icon_interfaces as inter
    inter.UI()

def characterPicker(*args):
    import character_picker_dock2 as cp
    UI = cp.CharacterPicker()

def paintSkinWeights(*args):
    mel.eval("ArtPaintSkinWeightsToolOptions;")

customMayaMenu()
