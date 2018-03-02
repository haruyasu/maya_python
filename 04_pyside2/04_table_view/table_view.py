import os
import maya.cmds as cmds
import maya.OpenMayaUI as om
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from shiboken2 import wrapInstance

ICON_DIR = "F:/maya_python/04_pyside2/04_table_view/icon"

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

class FileTableModel(QAbstractTableModel):
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
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
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
        if role == Qt.DisplayRole:
            return item.columns[index.column()].value
        elif role == Qt.TextAlignmentRole:
            return int(Qt.AlignLeft | Qt.AlignVCenter)
        return None

class SwatchDisplayPortDelegate(QItemDelegate):
    def __init__(self, parent, items, proxy_model):
        super(SwatchDisplayPortDelegate, self).__init__(parent)
        self.items = items
        self.proxy_model = proxy_model

    def paint(self, painter, option, index):
        item = self.items[self.proxy_model.mapToSource(index).row()]

        if not self.parent().indexWidget(index) and item.node:
            self.parent().setIndexWidget(index, _create_swatch_display_port_widget(item.node, self.parent()))

    def sizeHint(self, option, index):
        return QSize(64, 64)

def _create_swatch_display_port_widget(file_node, parent):
    tmp = cmds.window()
    cmds.columnLayout()
    sw = cmds.swatchDisplayPort(h=64, w=64, sn=file_node)
    ptr = om.MQtUtil.findControl(sw)
    sw_widget = wrapInstance(long(ptr), QWidget)
    sw_widget.setParent(parent)
    sw_widget.resize(64, 64)
    cmds.deleteUI(tmp)
    return sw_widget

class MenuButton(QPushButton):
    def __init__(self, icon_name, stacked_layout, index, parent=None):
        super(MenuButton, self).__init__(parent=parent)
        self.index = index
        self.setCheckable(True)
        self.setChecked(False)
        self.setFixedWidth(50)
        self.setFixedHeight(50)
        pix_map = QPixmap(os.path.join(ICON_DIR, "menu_{0}.png".format(icon_name)))
        icon = QIcon(pix_map)
        self.setIcon(icon)
        self.setIconSize(QSize(30, 30))
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

class QHLine(QFrame):
    def __init__(self):
        u"""initialize"""
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class Gui(MayaQWidgetBaseMixin, QMainWindow):
    selectedItem2 = ""

    def __init__(self, parent=None):
        super(Gui, self).__init__(parent=parent)
        self.setWindowTitle("TableView")
        self.setObjectName("TableViewWindow")
        self.setProperty("saveWindowPref", True)
        self.setStyleSheet("QFrame#header {background-color:#222}")
        self.table_view = QTableView()
        self.model = FileTableModel(self)

        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setSourceModel(self.model)
        self.table_view.setSortingEnabled(True)
        self.table_view.setModel(self.proxy_model)

    @staticmethod
    def show_ui(*args):
        win = Gui()
        win._create_ui()

    def _create_ui(self, *args):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self._refresh)
        file_menu.addAction(exit_action)

        edit_menu = menu_bar.addMenu("Edit")
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self._refresh)
        edit_menu.addAction(refresh_action)

        root_widget = QFrame(self)
        root_layout = QGridLayout(root_widget)
        root_widget.setLayout(root_layout)
        root_layout.setContentsMargins(0, 0, 0, 0)

        header_widget = QFrame(self)
        header_widget.setObjectName("header")
        header_widget.setMinimumHeight(60)

        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(12, 6, 6, 6)
        title_image = QLabel()
        title_pix = QPixmap(os.path.join(ICON_DIR, "logo.png"))
        title_image.setPixmap(title_pix)
        title_image.setScaledContents(True)
        title_image.setFixedSize(30, 30)
        header_layout.addWidget(title_image)

        title_label = QLabel(" Maya File Manager")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        root_layout.addWidget(header_widget, 0, 0, 1, 1)

        content_layout = QHBoxLayout(self)
        content_layout.setContentsMargins(6, 6, 6, 6)

        self.content_stacked_layout = QStackedLayout(self)

        content_layout.addWidget(self._create_menu_ui())

        root_layout.addLayout(content_layout, 1, 0, 1, 1)

        self.content_stacked_layout.addWidget(self._create_home_ui())
        self.content_stacked_layout.addWidget(self._create_file_nodes_ui())
        self.content_stacked_layout.addWidget(self._create_manager_ui())

        content_layout.addLayout(self.content_stacked_layout)

        self.setCentralWidget(root_widget)
        self.resize(1020, 600)
        self.show()

    def _create_menu_ui(self):
        menu_group = QButtonGroup(self)

        menu_widget = QFrame(self)
        menu_layout = QVBoxLayout(menu_widget)

        info_button = MenuButton("home", self.content_stacked_layout, 0)
        menu_layout.addWidget(info_button)
        menu_group.addButton(info_button)
        info_button.set_active()

        nodes_button = MenuButton("filer", self.content_stacked_layout, 1)
        menu_layout.addWidget(nodes_button)
        menu_group.addButton(nodes_button)

        nodes_button = MenuButton("note", self.content_stacked_layout, 2)
        menu_layout.addWidget(nodes_button)
        menu_group.addButton(nodes_button)

        nodes_button = MenuButton("movie", self.content_stacked_layout, 1)
        menu_layout.addWidget(nodes_button)
        menu_group.addButton(nodes_button)

        menu_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        return menu_widget

    def _create_home_ui(self):
        info_widget = QFrame(self)
        info_layout = QVBoxLayout(info_widget)
        info_label = QLabel("Home")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        info_label.setFont(title_font)
        info_layout.addWidget(info_label)
        info_layout.addWidget(QHLine())

        text_label = QLabel("Select Project")

        text_font = QFont()
        text_font.setPointSize(14)
        text_font.setBold(True)
        text_label.setFont(text_font)

        info_layout.addWidget(text_label)

        text_layout = QHBoxLayout(self)
        text_label2 = QLabel("Project")
        text_label2.setFont(text_font)
        text_layout.addWidget(text_label2)

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["maya", "houdini", "nuke"])
        self.comboBox.setEditable(True)
        # self.comboBox.setInsertPolicy(QComboBox.NoInsert)
        # self.comboBox.completer().setCompletionMode(QCompleter.PopupCompletion)

        text_layout.addWidget(self.comboBox)
        info_layout.addLayout(text_layout)

        info_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        return info_widget
        # self.content_stacked_layout.addWidget(info_widget)

    def _create_file_nodes_ui(self):
        file_nodes_root = QFrame(self)
        file_nodes_layout = QVBoxLayout(file_nodes_root)

        search_layout = QHBoxLayout(self)
        search_label = QLabel("Search")
        search_layout.addWidget(search_label)
        self.search_text = QLineEdit(self)
        self.search_text.textChanged.connect(self._change_filter)
        search_layout.addWidget(self.search_text)
        file_nodes_layout.addLayout(search_layout)

        self.table_view.clicked.connect(self._select_file_node)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setItemDelegateForColumn(0, SwatchDisplayPortDelegate(self.table_view, self.model.items, self.proxy_model))
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()
        self.table_view.verticalHeader().setDefaultSectionSize(64)

        file_nodes_layout.addWidget(self.table_view)

        return file_nodes_root

    def _create_manager_ui(self):
        info_widget = QFrame(self)
        self.info_layout = QVBoxLayout(info_widget)

        category_layout = QGridLayout(self)

        text_label = QLabel("Category")
        category_layout.addWidget(text_label, 0, 0)

        comboBox = QComboBox(self)
        comboBox.addItems(["maya", "houdini", "nuke"])
        comboBox.setEditable(True)
        comboBox.setMaximumWidth(350)
        category_layout.addWidget(comboBox, 0, 1)

        lineEdit = QLineEdit()
        lineEdit.setMaximumWidth(300)
        lineEdit.setText("Search")
        category_layout.addWidget(lineEdit, 0, 2)

        category_layout.setColumnStretch(1, 1)

        self.info_layout.addLayout(category_layout)
######
        path_layout = QHBoxLayout(self)
        path_label = QLabel("Path ")
        path_layout.addWidget(path_label)
        self.path_edit = QLineEdit(self)
        self.path_edit.setText("F:/maya_python/04_pyside2/")

        self.dir_path_edit = "F:/maya_python/04_pyside2/"

        folder_name = os.listdir(self.dir_path_edit)

        path_layout.addWidget(self.path_edit)
        self.info_layout.addLayout(path_layout)
#######
        list_layout = QHBoxLayout(self)
        self.listWidget1 = QListWidget()
        self.listWidget1.addItems(folder_name)
        self.listWidget1.itemClicked.connect(self._change_path2)
        self.listWidget2 = QListWidget()
        self.listWidget3 = QListWidget()

        list_layout.addWidget(self.listWidget1)
        list_layout.addWidget(self.listWidget2)
        list_layout.addWidget(self.listWidget3)
        self.info_layout.addLayout(list_layout)

######
        self.table_layout = QHBoxLayout(self)
        self.tableWidget = QTableWidget()
        headerLabels = ["File", "Size", "Type", "UpdateDateTime"]
        self.tableWidget.setColumnCount(len(headerLabels))
        self.tableWidget.setHorizontalHeaderLabels(headerLabels)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)

        try:
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        except:
            self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Interactive)

        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        dataList = [
            ["", "", "", ""],
        ]
        self.tableWidget.setRowCount(len(dataList))

        for row, colData in enumerate(dataList):
            for col, value in enumerate(colData):
                item = QTableWidgetItem(value)
                self.tableWidget.setItem(row, col, item)

        self.table_layout.addWidget(self.tableWidget)
        self.info_layout.addLayout(self.table_layout)

#######
        button_layout = QHBoxLayout(self)
        openButton = QPushButton("Open")
        button_layout.addWidget(openButton)
        importButton = QPushButton("Import")
        button_layout.addWidget(importButton)
        refButton = QPushButton("Reference")
        button_layout.addWidget(refButton)

        self.info_layout.addLayout(button_layout)

        self.info_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        return info_widget

    def _change_path2(self):
        items = self.listWidget1.selectedItems()[0].text() + "/"
        self.selectedItem = os.path.join(self.dir_path_edit, items)
        self.path_edit.setText(self.selectedItem)

        folder_name2 = []
        for x in os.listdir(self.selectedItem):
            if os.path.isdir(self.selectedItem + x):
                folder_name2.append(x)

        self.file_name = []
        for x in os.listdir(self.selectedItem):
            if os.path.isfile(self.selectedItem + x):
                self.file_name.append(x)

        self._file_disp()

        self.listWidget2.clear()
        self.listWidget3.clear()
        self.listWidget2.addItems(folder_name2)

        self.listWidget2.itemClicked.connect(self._change_path3)

    def _change_path3(self):
        items = self.listWidget2.selectedItems()[0].text() + "/"
        self.selectedItem2 = os.path.join(self.selectedItem, items)
        self.path_edit.setText(self.selectedItem2)

        folder_name3 = []
        for x in os.listdir(self.selectedItem2):
            if os.path.isdir(self.selectedItem2 + x):
                folder_name3.append(x)


        self.file_name = []
        for x in os.listdir(self.selectedItem2):
            if os.path.isfile(self.selectedItem2 + x):
                self.file_name.append(x)

        self._file_disp()

        self.listWidget3.clear()
        self.listWidget3.addItems(folder_name3)

        self.listWidget3.itemClicked.connect(self._change_path4)

    def _change_path4(self):
        items = self.listWidget3.selectedItems()[0].text() + "/"
        selectedItem3 = os.path.join(self.selectedItem2, items)
        self.path_edit.setText(selectedItem3)

    def _file_disp(self):
        dataList = [[0 for i in range(4)] for j in range(len(self.file_name))]

        for i in range(len(self.file_name)):
            dataList[i][0] = self.file_name[i]
            dataList[i][1] = "100.04KB"
            dataList[i][2] = "MayaAscii"
            dataList[i][3] = "2017/01/04 10:00:22"

        # dataList = [
        #     ["aaa.ma", "100.04KB", "MayaAscii", "2017/01/04 10:00:22"],
        #     ["bbb.ma", "222.23KB", "MayaAscii", "2017/02/06 13:00:22"],
        # ]
        self.tableWidget.setRowCount(len(dataList))

        for row, colData in enumerate(dataList):
            for col, value in enumerate(colData):
                item = QTableWidgetItem(value)
                self.tableWidget.setItem(row, col, item)

        self.table_layout.addWidget(self.tableWidget)
        self.info_layout.addLayout(self.table_layout)


    def _exit(self, *args):
        # ToDo make close event
        self.closeEvent()

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
        reg_exp = QRegExp(self.search_text.text(), Qt.CaseSensitive, QRegExp.RegExp)
        self.proxy_model.setFilterKeyColumn(2)
        self.proxy_model.setFilterRegExp(reg_exp)

    def _select_file_node(self, index):
        index = self.proxy_model.mapToSource(index)
        if not index.isValid():
            return
        model = self.model.items[index.row()]
        cmds.select(model.node)

Gui.show_ui()
