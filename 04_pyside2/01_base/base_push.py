from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

try:
  from PySide2.QtCore import *
  from PySide2.QtGui import *
  from PySide2.QtWidgets import *
  from PySide2 import __version__
  from shiboken2 import wrapInstance
except ImportError:
  from PySide.QtCore import *
  from PySide.QtGui import *
  from PySide import __version__
  from shiboken import wrapInstance

class MyButton(MayaQWidgetBaseMixin, QPushButton):
    def __init__(self, parent=None):
        super(MyButton, self).__init__(parent=parent)
        self.setText('Push Me')

# Create an instance of the button and display it.
#
button = MyButton()
button.show()

# A valid Maya control name has been automatically assigned
# to the button.
#
buttonName = button.objectName()
print('# ' + buttonName)
# MyButton_368fe1d8-5bc3-4942-a1bf-597d1b5d3b83

# Losing our only reference to the button does not cause it to be
# destroyed.
#
myButton = None

# We can use the button's name to find it as a Maya control.
#
from maya.OpenMayaUI import MQtUtil
from shiboken2 import wrapInstance

ptr = MQtUtil.findControl(buttonName)
foundControl = wrapInstance(long(ptr), QPushButton)

# Print out the button's text.
#
print('# ' + foundControl.text())
# Push Me
