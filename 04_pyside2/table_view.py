import os
import maya.cmds as cmds
import maya.OpenMayaUI as om
from PySide2 import QtCore, QtGui, QtWidgets
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from shiboken2 import wrapInstance

ICON_DIR = "F:/maya_python/04_pyside2/icon"

class Column(object):
    def __init__(self, index, value):
        self.index = index
        self.value = value

class Columns(object):
    def __init__(self):
        self._columns = None

    @property
    def columns(self):
        if self._columns is None:
            self._columns = self._get_columns()
        return self._columns

    def _get_columns(self):
        tmp_columns = []
        for k, v in self.__dict__.items():
            if type(v) == Column:
                tmp_columns.append(v)
        return sorted(tmp_columns, key=lambda x: x.index)

class FileInfo(Columns):
    header = ["Thumb", "Name", "Path"]
    row_count = len(header)

    def __init__(self, node):
        super(FileInfo, self).__init__()
        self.node = node
        self.thumbnail = Column(0, "")
        self.name = Column(1, node)
        self.file_type = Column(2, cmds.getAttr(node + ".fileTextureName").replace("a11889", "tm8r"))

class FileTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super(FileTableModel, self).__init__(parent)
        self.items = []
        self.refresh()

    def refresh(self, refresh_items=True):
        if refresh_items:
            file_nodes = cmds.ls(type="file")
            self.set_items(file_nodes)

        self.layoutAboutToBeChanged.emit()
        self.modelAboutToBeReset.emit()
        self.modelReset.emit()
        self.layoutChanged.emit()

    def set_items(self, nodes):
        self.items = []
        for node in nodes:
            self.items.append(FileInfo(node))

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return FileInfo.header[col]
        return None

    def rowCount(self, parent):
        return len(self.items)

    def columnCount(self, parent):
        return FileInfo.row_count

    def data(self, index, role):
        if not index.isValid():
            return None

        item = self.items[index.row()]
        if role == QtCore.Qt.DisplayRole:
            return item.columns[index.column()].value
        elif role == QtCore.Qt.TextAlignmentRole:
            return int(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        return None

class SwatchDisplayPortDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent, items, proxy_model):
        super(SwatchDisplayPortDelegate, self).__init__(parent)
        self.items = items
        self.proxy_model = proxy_model

    def paint(self, painter, option, index):
        item = self.items[self.proxy_model.mapToSource(index).row()]
        if not self.parent().indexWidget(index) and item.node:
            self.parent().setIndexWidget(
                index,
                _create_swatch_display_port_widget(item.node, self.parent())
            )

    def sizeHint(self, option, index):
        return QtCore.QSize(64, 64)

def _create_swatch_display_port_widget(file_node, parent):
    tmp = cmds.window()
    cmds.columnLayout()
    sw = cmds.swatchDisplayPort(h=64, w=64, sn=file_node)
    ptr = om.MQtUtil.findControl(sw)
    sw_widget = wrapInstance(long(ptr), QtWidgets.QWidget)
    sw_widget.setParent(parent)
    sw_widget.resize(64, 64)
    cmds.deleteUI(tmp)
    return sw_widget

class MenuButton(QtWidgets.QPushButton):
    def __init__(self, icon_name, stacked_layout, index, parent=None):
        super(MenuButton, self).__init__(parent=parent)
        self.index = index
        self.setCheckable(True)
        self.setChecked(False)
        self.setFixedWidth(50)
        self.setFixedHeight(50)
        pix_map = QtGui.QPixmap(os.path.join(ICON_DIR, "menu_{0}.png".format(icon_name)))
        icon = QtGui.QIcon(pix_map)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(30, 30))
        self.stacked_layout = stacked_layout
        self.setStyleSheet("""
                            MenuButton {background-color:#666;}
                            MenuButton:checked {background-color:#4f4f4f;}
                            """)
        self.checkStateSet()

    def mouseReleaseEvent(self, event):
        super(MenuButton, self).mouseReleaseEvent(event)
        if not self.isChecked() or not self.stacked_layout:
            return
        self.set_active()

    def set_active(self):
        self.setChecked(True)
        self.stacked_layout.setCurrentIndex(self.index)

class QHLine(QtWidgets.QFrame):
    def __init__(self):
        u"""initialize"""
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

class TableViewExampleWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    _UI_WINDOW_NAME = "TableView"
    _UI_ID = "TableViewWindow"

    def __init__(self, parent=None):
        super(TableViewExampleWindow, self).__init__(parent=parent)
        self.setWindowTitle(self._UI_WINDOW_NAME)
        self.setObjectName(self._UI_ID)
        self.setProperty("saveWindowPref", True)
        self.setStyleSheet("QFrame#header {background-color:#222}")
        self.table_view = QtWidgets.QTableView()
        self.model = FileTableModel(self)

        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxy_model.setSourceModel(self.model)
        self.table_view.setSortingEnabled(True)
        self.table_view.setModel(self.proxy_model)

    @staticmethod
    def show_ui(*args):
        win = TableViewExampleWindow()
        win._create_ui()

    def _create_ui(self, *args):
        menu_bar = self.menuBar()
        edit_menu = menu_bar.addMenu("Edit")
        refresh_action = QtWidgets.QAction("Refresh", self)
        refresh_action.triggered.connect(self._refresh)
        edit_menu.addAction(refresh_action)

        root_widget = QtWidgets.QFrame(self)
        root_layout = QtWidgets.QGridLayout(root_widget)
        root_widget.setLayout(root_layout)
        root_layout.setContentsMargins(0, 0, 0, 0)

        header_widget = QtWidgets.QFrame(self)
        header_widget.setObjectName("header")
        header_widget.setMinimumHeight(60)

        header_layout = QtWidgets.QHBoxLayout(header_widget)
        header_layout.setContentsMargins(12, 6, 6, 6)
        title_image = QtWidgets.QLabel()
        title_pix = QtGui.QPixmap(os.path.join(ICON_DIR, "logo.png"))
        title_image.setPixmap(title_pix)
        title_image.setScaledContents(True)
        title_image.setFixedSize(30, 30)
        header_layout.addWidget(title_image)

        title_label = QtWidgets.QLabel(" TableView")
        title_font = QtGui.QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        root_layout.addWidget(header_widget, 0, 0, 1, 1)

        content_layout = QtWidgets.QHBoxLayout(self)
        content_layout.setContentsMargins(6, 6, 6, 6)

        self.content_stacked_layout = QtWidgets.QStackedLayout(self)

        content_layout.addWidget(self._create_menu_ui())

        root_layout.addLayout(content_layout, 1, 0, 1, 1)

        self.content_stacked_layout.addWidget(self._create_home_ui())
        self.content_stacked_layout.addWidget(self._create_file_nodes_ui())

        content_layout.addLayout(self.content_stacked_layout)

        self.setCentralWidget(root_widget)
        self.resize(1020, 600)
        self.show()

    def _create_menu_ui(self):
        menu_group = QtWidgets.QButtonGroup(self)

        menu_widget = QtWidgets.QFrame(self)
        menu_layout = QtWidgets.QVBoxLayout(menu_widget)

        info_button = MenuButton("home", self.content_stacked_layout, 0)
        menu_layout.addWidget(info_button)
        menu_group.addButton(info_button)
        info_button.set_active()

        nodes_button = MenuButton("filer", self.content_stacked_layout, 1)
        menu_layout.addWidget(nodes_button)
        menu_group.addButton(nodes_button)

        menu_layout.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        return menu_widget

    def _create_home_ui(self):
        info_widget = QtWidgets.QFrame(self)
        info_layout = QtWidgets.QVBoxLayout(info_widget)
        info_label = QtWidgets.QLabel("Home")
        title_font = QtGui.QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        info_label.setFont(title_font)
        info_layout.addWidget(info_label)
        info_layout.addWidget(QHLine())
        info_layout.addWidget(QtWidgets.QLabel("Sample"))

        info_layout.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        return info_widget
        self.content_stacked_layout.addWidget(info_widget)

    def _create_file_nodes_ui(self):
        file_nodes_root = QtWidgets.QFrame(self)
        file_nodes_layout = QtWidgets.QVBoxLayout(file_nodes_root)

        search_layout = QtWidgets.QHBoxLayout(self)
        search_label = QtWidgets.QLabel("Search")
        search_layout.addWidget(search_label)
        self.search_text = QtWidgets.QLineEdit(self)
        self.search_text.textChanged.connect(self._change_filter)
        search_layout.addWidget(self.search_text)
        file_nodes_layout.addLayout(search_layout)

        self.table_view.clicked.connect(self._select_file_node)
        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_view.setItemDelegateForColumn(0, SwatchDisplayPortDelegate(self.table_view, self.model.items, self.proxy_model))
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()
        self.table_view.verticalHeader().setDefaultSectionSize(64)

        file_nodes_layout.addWidget(self.table_view)
        return file_nodes_root

    def _refresh(self, *args):
        self.table_view.clearSelection()
        self.table_view.clearFocus()
        self.model.refresh(refresh_items=True)
        self.table_view.setItemDelegateForColumn(0, SwatchDisplayPortDelegate(self.table_view, self.model.items, self.proxy_model))
        self.table_view.setVisible(False)
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()
        self.table_view.verticalHeader().setDefaultSectionSize(64)
        self.table_view.setVisible(True)

    def _change_filter(self, *args):
        reg_exp = QtCore.QRegExp(self.search_text.text(),
                                 QtCore.Qt.CaseSensitive,
                                 QtCore.QRegExp.RegExp)
        self.proxy_model.setFilterKeyColumn(2)
        self.proxy_model.setFilterRegExp(reg_exp)

    def _select_file_node(self, index):
        index = self.proxy_model.mapToSource(index)
        if not index.isValid():
            return
        model = self.model.items[index.row()]
        cmds.select(model.node)

TableViewExampleWindow.show_ui()
