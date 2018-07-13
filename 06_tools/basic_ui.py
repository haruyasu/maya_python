import maya.cmds as cmds

class BasicUI():
    def __init__(self):
        self.windowName = "exampleWindow"
        self.windowHeight = 400
        self.windowWidth = 400
        self.createUI(self.windowName, self.windowHeight, self.windowWidth, True, False)

    def createUI(self, windowName, windowHeight, windowWidth, dock, scroll):
        if dock == True:
            if cmds.dockControl(windowName + "_dock", exists=True):
                cmds.deleteUI(windowName + "_dock")
        else:
            if cmds.window(windowName, exists=True):
                cmds.deleteUI(windowName)

        self.window = cmds.window(windowName, title=windowName, w=windowWidth, h=windowHeight, mnb=False, mxb=False)

        self.mainLayout = cmds.columnLayout(w=windowWidth, h=windowHeight)


        # unique UI stuff
        self.createCustom()

        if dock == True:
            cmds.dockControl(windowName + "_dock", label=windowName + "_dock", area="left", content=self.window)
        else:
            cmds.showWindow(self.window)

    def createCustom(self):
        print "create Custom"

class TestUI(BasicUI):
    def __init__(self):
        self.windowName = "TestWindow"
        self.windowHeight = 800
        self.windowWidth = 300

        self.createUI(self.windowName, self.windowHeight, self.windowWidth, True, False)

    def createCustom(self):
        cmds.rowColumnLayout(nc=2, cw=[(1, 150), (2, 150)], parent=self.mainLayout)
        cmds.button(label="Test")
        cmds.button(label="Test2")

BasicUI()
TestUI()
