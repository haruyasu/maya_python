from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

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

class MyDockableButton(MayaQWidgetDockableMixin, QPushButton):
    def __init__(self, parent=None):
        super(MyDockableButton, self).__init__(parent=parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred )
        self.setText('Push Me')

# Show the button as a non-dockable floating window.
#
button = MyDockableButton()
button.show(dockable=False)

# showRepr() can be used to display the current dockable settings.
#
print('# ' + button.showRepr())
# show(dockable=False, height=23, width=70, y=610, x=197, floating=True)

# Change it to a dockable floating window.
#
button.show(dockable=True)
print('# ' + button.showRepr())
# show(dockable=True, area='none', height=23, width=70, y=610, x=197, floating=True)
