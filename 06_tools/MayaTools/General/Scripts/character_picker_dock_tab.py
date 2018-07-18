import maya.cmds as cmds
from functools import partial

class CharacterPicker():
    def __init__(self):
        # class var
        self.widgets = {}

        # get namespace
        namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)

        self.namespaces = []

        for name in namespaces:
            if cmds.objExists(name + ":pelvis"):
                self.namespaces.append(name)

        print self.namespaces

        # call on the build UI method
        self.buildUI()

    def buildUI(self):
        if cmds.dockControl("characterPicker_dockControl", exists=True):
            cmds.deleteUI("characterPicker_dockControl")

        self.widgets["window"] = cmds.window(title="Character Picker", w=400, h=600, mnb=False, mxb=False)
        self.widgets["mainLayout"] = cmds.columnLayout(w=400, h=600)
        self.widgets["tabLayout"] = cmds.tabLayout()

        for name in self.namespaces:
            self.widgets[(name + "_formLayout")] = cmds.formLayout(w=400, h=600, parent=self.widgets["tabLayout"])

            namespace = name + ":"

            # create the buttons
            self.widgets[name + "_headButton"] = cmds.button(label="", w=40, h=40, bgc=[0, 0.593, 1])
            cmds.button(self.widgets[name + "_headButton"], edit=True, c=partial(self.selectControls, [namespace + "head"], [(self.widgets[name + "_headButton"], [0, 0.593, 1])]))

            self.widgets[name + "_spine03Button"] = cmds.button(label="", w=100, h=40, bgc=[0.824, 0.522, 0.275])
            cmds.button(self.widgets[name + "_spine03Button"], edit=True, c=partial(self.selectControls, [namespace + "spine_03"], [(self.widgets[name + "_spine03Button"], [0.824, 0.522, 0.275])]))

            self.widgets[name + "_spine02Button"] = cmds.button(label="", w=100, h=40, bgc=[0.824, 0.522, 0.275])
            cmds.button(self.widgets[name + "_spine02Button"], edit=True, c=partial(self.selectControls, [namespace + "spine_02"], [(self.widgets[name + "_spine02Button"], [0.824, 0.522, 0.275])]))

            self.widgets[name + "_spine01Button"] = cmds.button(label="", w=100, h=40, bgc=[0.824, 0.522, 0.275])
            cmds.button(self.widgets[name + "_spine01Button"], edit=True, c=partial(self.selectControls, [namespace + "spine_01"], [(self.widgets[name + "_spine01Button"], [0.824, 0.522, 0.275])]))

            self.widgets[name + "_selectAllSpineButton"] = cmds.button(label="", w=30, h=30, bgc=[0, 1, 0])
            cmds.button(self.widgets[name + "_selectAllSpineButton"], edit=True, c=partial(self.selectControls,
            [(namespace + "spine_01"), (namespace + "spine_02"), (namespace + "spine_03")],
            [(self.widgets[name + "_spine01Button"], [0.824, 0.522, 0.275]),
             (self.widgets[name + "_spine02Button"], [0.824, 0.522, 0.275]),
             (self.widgets[name + "_spine03Button"], [0.824, 0.522, 0.275])]))

            # place the buttons
            cmds.formLayout(self.widgets[name + "_formLayout"], edit=True, af=[(self.widgets[name + "_headButton"], "left", 175), (self.widgets[name + "_headButton"], "top", 100)])
            cmds.formLayout(self.widgets[name + "_formLayout"], edit=True, af=[(self.widgets[name + "_spine03Button"], "left", 145), (self.widgets[name + "_spine03Button"], "top", 150)])
            cmds.formLayout(self.widgets[name + "_formLayout"], edit=True, af=[(self.widgets[name + "_spine02Button"], "left", 145), (self.widgets[name + "_spine02Button"], "top", 200)])
            cmds.formLayout(self.widgets[name + "_formLayout"], edit=True, af=[(self.widgets[name + "_spine01Button"], "left", 145), (self.widgets[name + "_spine01Button"], "top", 250)])
            cmds.formLayout(self.widgets[name + "_formLayout"], edit=True, af=[(self.widgets[name + "_selectAllSpineButton"], "left", 250), (self.widgets[name + "_selectAllSpineButton"], "top", 205)])

            cmds.tabLayout(self.widgets["tabLayout"], edit=True, tabLabel=((self.widgets[(name + "_formLayout")], name)))

        # cmds.showWindow(self.widgets["window"])
        cmds.dockControl(label="Character Picker", area="right", allowedArea="right", content=self.widgets["window"])

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
