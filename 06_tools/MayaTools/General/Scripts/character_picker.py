import maya.cmds as cmds
from functools import partial

class CharacterPicker():
    def __init__(self):
        # class var
        self.widgets = {}

        # call on the build UI method
        self.buildUI()

    def buildUI(self):
        if cmds.window("characterPicker_UI", exists=True):
            cmds.deleteUI("characterPicker_UI")

        self.widgets["window"] = cmds.window("characterPicker_UI", title="Character Picker", w=400, h=600, mnb=False, mxb=False)
        self.widgets["mainLayout"] = cmds.columnLayout(w=400, h=600)
        self.widgets["formLayout"] = cmds.formLayout(w=400, h=600)

        # create the buttons
        self.widgets["headButton"] = cmds.button(label="", w=40, h=40, bgc=[0, 0.593, 1])
        cmds.button(self.widgets["headButton"], edit=True, c=partial(self.selectControls, ["head"], [(self.widgets["headButton"], [0, 0.593, 1])]))

        self.widgets["spine03Button"] = cmds.button(label="", w=100, h=40, bgc=[0.824, 0.522, 0.275])
        cmds.button(self.widgets["spine03Button"], edit=True, c=partial(self.selectControls, ["spine_03"], [(self.widgets["spine03Button"], [0.824, 0.522, 0.275])]))

        self.widgets["spine02Button"] = cmds.button(label="", w=100, h=40, bgc=[0.824, 0.522, 0.275])
        cmds.button(self.widgets["spine02Button"], edit=True, c=partial(self.selectControls, ["spine_02"], [(self.widgets["spine02Button"], [0.824, 0.522, 0.275])]))

        self.widgets["spine01Button"] = cmds.button(label="", w=100, h=40, bgc=[0.824, 0.522, 0.275])
        cmds.button(self.widgets["spine01Button"], edit=True, c=partial(self.selectControls, ["spine_01"], [(self.widgets["spine01Button"], [0.824, 0.522, 0.275])]))

        self.widgets["selectAllSpineButton"] = cmds.button(label="", w=30, h=30, bgc=[0, 1, 0])
        cmds.button(self.widgets["selectAllSpineButton"], edit=True, c=partial(self.selectControls, ["spine_01", "spine_02", "spine_03"], [(self.widgets["spine01Button"], [0.824, 0.522, 0.275]), (self.widgets["spine02Button"], [0.824, 0.522, 0.275]), (self.widgets["spine03Button"], [0.824, 0.522, 0.275])]))


        # place the buttons
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["headButton"], "left", 175), (self.widgets["headButton"], "top", 100)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["spine03Button"], "left", 145), (self.widgets["spine03Button"], "top", 150)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["spine02Button"], "left", 145), (self.widgets["spine02Button"], "top", 200)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["spine01Button"], "left", 145), (self.widgets["spine01Button"], "top", 250)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["selectAllSpineButton"], "left", 250), (self.widgets["selectAllSpineButton"], "top", 205)])

        cmds.showWindow(self.widgets["window"])

    def selectControls(self, controls, buttonInfo, *args):
        # buttonInfo = [[buttonName, buttonBGC]]
        # if yo have shift held down
        mods = cmds.getModifiers()

        if (mods & 1) > 0:
            for i in range(len(controls)):
                cmds.select(controls[i], tgl=True)

                buttonName = buttonInfo[i][0]
                buttonBGC = buttonInfo[i][1]

                cmds.button(buttonName, edit=True, bgc=[1.0, 1.0, 1.0])
                ++i

                # call our scriptJob
                self.createSelectionScriptJob(controls[i], buttonName, buttonBGC)

        # if you have no modifier:
        else:
            cmds.select(clear=True)
            for i in range(len(controls)):
                cmds.select(controls[i], add=True)

                buttonName = buttonInfo[i][0]
                buttonBGC = buttonInfo[i][1]

                cmds.button(buttonName, edit=True, bgc=[1.0, 1.0, 1.0])
                ++i

                # call our scriptJob
                self.createSelectionScriptJob(controls[i], buttonName, buttonBGC)

    def createSelectionScriptJob(self, control, buttonName, buttonBGC):
        scriptJobNum = cmds.scriptJob(event=["SelectionChanged", partial(self.deselectButton, control, buttonName, buttonBGC)], runOnce=True, parent=self.widgets["window"])

    def deselectButton(self, control, buttonName, buttonBGC):
        selection = cmds.ls(sl=True)

        if control not in selection:
            cmds.button(buttonName, edit=True, bgc=buttonBGC)
        else:
            self.createSelectionScriptJob(control, buttonName, buttonBGC)
