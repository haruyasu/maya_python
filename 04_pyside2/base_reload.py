import pymel.core as pm
import sys

path = "F:/maya_python/04_pyside2"
if not path in sys.path:
	sys.path.append(path)

import table_view
reload(table_view)
