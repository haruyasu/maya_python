from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        openAct = QAction(self.style().standardIcon(QStyle.SP_DialogOpenButton), 'Open', self)
        openAct.triggered.connect(self.open)

        saveAct = QAction(self.style().standardIcon(QStyle.SP_DialogSaveButton), 'Save', self)
        saveAct.triggered.connect(self.save)

        menuBar = self.menuBar()
        menu = menuBar.addMenu('File')
        menu.addAction(openAct)
        menu.addAction(saveAct)

        toolBar = self.addToolBar('File')
        toolBar.addAction(openAct)
        toolBar.addAction(saveAct)

        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Menu")
        self.show()

    def open(self):
        print 'Open'

    def save(self):
        print 'Save'

MainWindow()
