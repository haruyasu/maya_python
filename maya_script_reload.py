import pymel.core as pm
import sys

path = "F:/maya_python/04_pyside2/04_table_view"
if not path in sys.path:
	sys.path.append(path)

import table_view
reload(table_view)

############
import pymel.core as pm
import sys

path = "D:/github/maya_python/06_tools"
if not path in sys.path:
	sys.path.append(path)

import preset_ui
reload(preset_ui)
preset_ui.PresetUI()