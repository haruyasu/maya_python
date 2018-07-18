import maya.cmds as cmds

class PresetUI():
    def __init__(self):
        if cmds.window("presetUI", exists=True):
            cmds.deleteUI("presetUI")

        self.widgets = {}
        self.widgets["window"] = cmds.window("presetUI", title="Presets", w=450, h=250, mnb=False, mxb=False, sizeable=True)
        self.widgets["mainLayout"] = cmds.columnLayout(w=450, h=250)
        menuBarLayout = cmds.menuBarLayout()
        cmds.menu(label="File")
        cmds.menuItem(label="Save Preset", c=self.savePreset)
        cmds.menuItem(label="Load Preset", c=self.loadPreset)

        self.widgets["formLayout"] = cmds.formLayout(w=450, h=250)

        # create our controls
        self.widgets["floatField"] = cmds.floatFieldGrp(numberOfFields=3, label="Position", value1=0.0, value2=0.0, value3=0.0)
        self.widgets["floatSlider"] = cmds.floatSliderGrp(label="Example", field=True, minValue=-10, maxValue=10, fieldMinValue=-10, fieldMaxValue=10, value=0)
        self.widgets["radioButtonGrp"] = cmds.radioButtonGrp(label="Radio Buttons", labelArray3=["Yes", "No", "Maybe"], numberOfRadioButtons=3)
        self.widgets["inputTextField"] = cmds.textField(w=300, h=30, text="Input Directory", enable=False)
        self.widgets["outputTextField"] = cmds.textField(w=300, h=30, text="Output Directory", enable=False)
        self.widgets["inputButton"] = cmds.button(w=30, h=30, label="...", c=self.inputDirectory)
        self.widgets["outputButton"] = cmds.button(w=30, h=30, label="...", c=self.outputDirectory)
        self.widgets["swatch"] = cmds.canvas(rgbValue=(0, 0, 1), width=50, height=50)
        self.widgets["colorEditor"] = cmds.button(label="Color Editor", w=100, h=50, c=self.chooseColor)
        self.widgets["checkBox1"] = cmds.checkBox(label="Yes", v=0)
        self.widgets["checkBox2"] = cmds.checkBox(label="Yes", v=0)
        self.widgets["iconTextCheckBox1"] = cmds.iconTextCheckBox(style="iconOnly", image1="spotlight.png")
        self.widgets["iconTextCheckBox2"] = cmds.iconTextCheckBox(style="iconOnly", image1="sphere.png")
        self.widgets["iconTextCheckBox3"] = cmds.iconTextCheckBox(style="iconOnly", image1="cube.png")
        self.widgets["iconTextCheckBox4"] = cmds.iconTextCheckBox(style="iconOnly", image1="cone.png")
        self.widgets["iconTextCheckBox5"] = cmds.iconTextCheckBox(style="textOnly", label="Toggle", w=40, h=30)

        # place our controls
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["floatField"], "top", 10), (self.widgets["floatField"], "left", -60)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["floatSlider"], "top", 40), (self.widgets["floatSlider"], "left", -60)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["radioButtonGrp"], "top", 70), (self.widgets["radioButtonGrp"], "left", -60)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["inputTextField"], "top", 100), (self.widgets["inputTextField"], "left", 5)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["outputTextField"], "top", 130), (self.widgets["outputTextField"], "left", 5)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["inputButton"], "top", 100), (self.widgets["inputButton"], "left", 310)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["outputButton"], "top", 130), (self.widgets["outputButton"], "left", 310)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["swatch"], "top", 170), (self.widgets["swatch"], "left", 5)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["colorEditor"], "top", 170), (self.widgets["colorEditor"], "left", 60)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["checkBox1"], "top", 185), (self.widgets["checkBox1"], "left", 165)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["checkBox2"], "top", 185), (self.widgets["checkBox2"], "left", 265)])

        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["iconTextCheckBox1"], "top", 10), (self.widgets["iconTextCheckBox1"], "left", 400)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["iconTextCheckBox2"], "top", 50), (self.widgets["iconTextCheckBox2"], "left", 400)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["iconTextCheckBox3"], "top", 90), (self.widgets["iconTextCheckBox3"], "left", 400)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["iconTextCheckBox4"], "top", 130), (self.widgets["iconTextCheckBox4"], "left", 400)])
        cmds.formLayout(self.widgets["formLayout"], edit=True, af=[(self.widgets["iconTextCheckBox5"], "top", 170), (self.widgets["iconTextCheckBox5"], "left", 400)])

        cmds.showWindow(self.widgets["window"])
        cmds.window(self.widgets["window"], edit=True, w=450, h=250)

    def inputDirectory(self, *args):
        self.inputPath = cmds.fileDialog2(fileMode=3, dialogStyle=2)[0]
        cmds.textField(self.widgets["inputTextField"], edit=True, text=self.inputPath)

    def outputDirectory(self, *args):
        self.outputPath = cmds.fileDialog2(fileMode=3, dialogStyle=2)[0]
        cmds.textField(self.widgets["outputTextField"], edit=True, text=self.outputPath)

    def chooseColor(self, *args):
        self.color = cmds.colorEditor()
        colors = self.color.split("  ")
        colorR = colors[0]
        colorG = colors[1]
        colorB = colors[2].partition(" ")[0]
        cmds.canvas(self.widgets["swatch"], edit=True, rgbValue=(float(colorR), float(colorG), float(colorB)))

    def savePreset(self, *args):
        # get values from our UI controls
        floatFieldValues = cmds.floatFieldGrp(self.widgets["floatField"], q=True, v=True)
        floatSliderValue = cmds.floatSliderGrp(self.widgets["floatSlider"], q=True, v=True)
        radioButtonValue = cmds.radioButtonGrp(self.widgets["radioButtonGrp"], q=True, sl=True)
        inputField = cmds.textField(self.widgets["inputTextField"], q=True, text=True)
        outputField = cmds.textField(self.widgets["outputTextField"], q=True, text=True)
        canvasColor = cmds.canvas(self.widgets["swatch"], q=True, rgbValue=True)
        cb1Value = cmds.checkBox(self.widgets["checkBox1"], q=True, v=True)
        cb2Value = cmds.checkBox(self.widgets["checkBox2"], q=True, v=True)
        spotlightValue = cmds.iconTextCheckBox(self.widgets["iconTextCheckBox1"], q=True, v=True)
        sphereValue = cmds.iconTextCheckBox(self.widgets["iconTextCheckBox2"], q=True, v=True)
        cubeValue = cmds.iconTextCheckBox(self.widgets["iconTextCheckBox3"], q=True, v=True)
        coneValue = cmds.iconTextCheckBox(self.widgets["iconTextCheckBox4"], q=True, v=True)
        toggleValue = cmds.iconTextCheckBox(self.widgets["iconTextCheckBox5"], q=True, v=True)

        # write to file
        path = cmds.internalVar(upd=True) + "preset.txt"
        file = open(path, "w")

        # controlType, controlName, query, value
        file.write(str(["floatFieldGrp", "floatField", "v", str(floatFieldValues)]) + "\n")
        file.write(str(["floatSliderGrp", "floatSlider", "v", str(floatSliderValue)]) + "\n")
        file.write(str(["radioButtonGrp", "radioButtonGrp", "sl", str(radioButtonValue)]) + "\n")
        file.write(str(["textField", "inputTextField", "text", str(inputField)]) + "\n")
        file.write(str(["textField", "outputTextField", "text", str(outputField)]) + "\n")
        file.write(str(["canvas", "swatch", "rgbValue", str(canvasColor)]) + "\n")
        file.write(str(["checkBox", "checkBox1", "v", str(cb1Value)]) + "\n")
        file.write(str(["checkBox", "checkBox2", "v", str(cb2Value)]) + "\n")
        file.write(str(["iconTextCheckBox", "iconTextCheckBox1", "v", str(spotlightValue)]) + "\n")
        file.write(str(["iconTextCheckBox", "iconTextCheckBox2", "v", str(sphereValue)]) + "\n")
        file.write(str(["iconTextCheckBox", "iconTextCheckBox3", "v", str(cubeValue)]) + "\n")
        file.write(str(["iconTextCheckBox", "iconTextCheckBox4", "v", str(coneValue)]) + "\n")
        file.write(str(["iconTextCheckBox", "iconTextCheckBox5", "v", str(toggleValue)]))

        file.close()

    def loadPreset(self, *args):
        path = cmds.internalVar(upd=True) + "preset.txt"
        file = open(path, "r")

        for line in file:
            controlType = line.partition(",")[0]
            controlType = controlType.translate(None, "\,[]\'")

            controlName = line.partition(",")[2].partition(",")[0]
            controlName = controlName.translate(None, "\,[]\' ")

            queryType = line.partition(",")[2].partition(",")[2].partition(",")[0]
            queryType = queryType.translate(None, "\,[]\'")

            if controlType == "floatFieldGrp":
                data = line.rpartition("[")[2]
                data = data.translate(None, "\,[]\'")
                data = data.rstrip("\n")
                data = data.split(" ")
                commandString = ("cmds." + controlType + "(self.widgets[" + "\"" + controlName + "\"" + "], edit=True, " + queryType + "=[" + data[0] + " ," + data[1] + " ," + data[2] + ", 0.0])")
            elif controlType == "textField":
                data = line.rpartition(",")[2]
                data = data.translate(None, "\,[]\'")
                data = data[1:]
                data = data.rstrip("\n")
                commandString = ("cmds." + controlType + "(self.widgets[" + "\"" + controlName + "\"" + "], edit=True, " + queryType + "=\"" + str(data) + "\")")
            elif controlType == "canvas":
                data = line.rpartition("[")[2]
                data = data.translate(None, "\,[]\'")
                data = data.rstrip("\n")
                data = data.split(" ")
                commandString = ("cmds." + controlType + "(self.widgets[" + "\"" + controlName + "\"" + "], edit=True, " + queryType + "=[" + data[0] + " ," + data[1] + " ," + data[2] + "])")
            else:
                data = line.rpartition(",")[2]
                data = data.translate(None, "\,[]\' ")
                data = data.rstrip("\n")
                commandString = ("cmds." + controlType + "(self.widgets[" + "\"" + controlName + "\"" + "], edit=True, " + queryType + "=" + data + ")")



            print commandString
            exec(commandString)
