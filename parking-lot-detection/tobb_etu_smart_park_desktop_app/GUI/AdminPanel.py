import sys
from tobb_etu_smart_park_desktop_app.GUI import videoEditor
from PyQt5 import QtCore, QtGui, QtWidgets
from tobb_etu_smart_park_desktop_app.GUI import PyQt5_stylesheets
from tobb_etu_smart_park_desktop_app.GUI.videoEditor import ShowVideo, ImageViewer
from PyQt5.QtGui import QIcon
import numpy
import sys

class Ui_MainWindow():
    def setupUi(self, MainWindow):
        self.mainW = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1068, 824)

        self.selectedParkingLots = []
        self.occupancyDetectionStarted = False
        self.slotDetectionStarted = False

        self.manager = None

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.East)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")

        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setObjectName("groupBox")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")


        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 705, 500))
        self.page.setObjectName("page")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.page)
        self.gridLayout_4.setObjectName("gridLayout_4")


        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabWidget_2.setGeometry(QtCore.QRect(0, 0, 705, 500))
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.VideoPlayer = QtWidgets.QGridLayout(self.tab_3)
        self.VideoPlayer.setObjectName("Video Player")

        self.tabWidget_2.addTab(self.tab_3, "")

        self.tabWidget_2.currentChanged.connect(self.tabChange)  # changed!

        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget.setObjectName("tableWidget")

        self.tableWidget.itemSelectionChanged.connect(self.selectionChange)

        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(150)



        """ Rows """
        """
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)

        """

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)

        self.gridLayout_7.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_5, "Parking Slot Table")

        self.gridLayout.addWidget(self.tabWidget_2, 0, 0, 1, 1)
        self.dateEdit = QtWidgets.QDateEdit(self.tab)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")


        self.verticalLayout_5.addWidget(self.tabWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.detectOccupancy = QtWidgets.QPushButton(self.centralwidget)
        self.detectOccupancy.setObjectName("detectOccupancy")
        self.horizontalLayout.addWidget(self.detectOccupancy)
        self.detectOccupancy.clicked.connect(self.startOccupancyDetection)

        self.detectSlot = QtWidgets.QPushButton(self.centralwidget)
        self.detectSlot.setObjectName("detectSlot")
        self.horizontalLayout.addWidget(self.detectSlot)
        self.detectSlot.clicked.connect(self.startSlotDetection)



        self.bt_menu_button_popup = QtWidgets.QToolButton(self.centralwidget)
        self.bt_menu_button_popup.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.bt_menu_button_popup.setObjectName("bt_menu_button_popup")
        self.horizontalLayout.addWidget(self.bt_menu_button_popup)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)


        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)



        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1068, 23))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")

        self.fileMenu = self.menuMenu.addMenu('&File')



        self.openAction = QtWidgets.QAction('&Open Video')
        self.openAction.triggered.connect(self.openVideo)
        self.fileMenu.addAction(self.openAction)


        MainWindow.setMenuBar(self.menubar)


        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.up_button_action = QtWidgets.QAction(QIcon('./buttonIcons/up.jpg'), "Up", MainWindow)
        self.up_button_action.setStatusTip("Up")
        self.up_button_action.triggered.connect(self.upSelectedParkingLots)
        #self.up_button_action.setCheckable(True)
        self.toolBar.addAction(self.up_button_action)

        self.down_button_action = QtWidgets.QAction(QIcon('./buttonIcons/down.jpg'), "Down", MainWindow)
        self.down_button_action.setStatusTip("Down")
        self.down_button_action.triggered.connect(self.downSelectedParkingLots)
        #self.down_button_action.setCheckable(True)
        self.toolBar.addAction(self.down_button_action)

        self.left_button_action = QtWidgets.QAction(QIcon('./buttonIcons/left.jpg'), "Left", MainWindow)
        self.left_button_action.setStatusTip("Left")
        self.left_button_action.triggered.connect(self.leftSelectedParkingLots)
        #self.left_button_action.setCheckable(True)
        self.toolBar.addAction(self.left_button_action)

        self.right_button_action = QtWidgets.QAction(QIcon('./buttonIcons/right.jpg'), "Right", MainWindow)
        self.right_button_action.setStatusTip("Right")
        self.right_button_action.triggered.connect(self.rightSelectedParkingLots)
        #self.right_button_action.setCheckable(True)
        self.toolBar.addAction(self.right_button_action)

        self.selectAll_button_action = QtWidgets.QAction(QIcon('./buttonIcons/selectAll.jpg'), "Select All", MainWindow)
        self.selectAll_button_action.setStatusTip("Select All")
        self.selectAll_button_action.triggered.connect(self.selectAll)
        self.toolBar.addAction(self.selectAll_button_action)

        self.deSelectAll_button_action = QtWidgets.QAction(QIcon('./buttonIcons/deSelectAll.jpg'), "Deselect All", MainWindow)
        self.deSelectAll_button_action.setStatusTip("Deselect All")
        self.deSelectAll_button_action.triggered.connect(self.deSelectAll)
        self.toolBar.addAction(self.deSelectAll_button_action)

        self.saveToServer = QtWidgets.QAction(QIcon('./buttonIcons/save.jpg'), "Save", MainWindow)
        self.saveToServer.setStatusTip("Save")
        self.saveToServer.triggered.connect(self.sendServer)
        self.toolBar.addAction(self.saveToServer)

        self.deleteParkingSlot = QtWidgets.QAction(QIcon('./buttonIcons/delete.jpg'), "Delete", MainWindow)
        self.deleteParkingSlot.setStatusTip("Delete")
        self.deleteParkingSlot.triggered.connect(self.deleteSelectedSlots)
        self.toolBar.addAction(self.deleteParkingSlot)


        #self.dockWidget2 = QtWidgets.QDockWidget(MainWindow)
        #self.dockWidget2.setObjectName("dockWidget2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout_3.setObjectName("gridLayout_3")



        #self.dockWidget2.setWidget(self.dockWidgetContents_2)
        #MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget2)
        self.actionSub_menu = QtWidgets.QAction(MainWindow)
        self.actionSub_menu.setObjectName("actionSub_menu")


        #self.menuSubmenu_2.addAction(self.actionSub_menu)
        #self.menuMenu.addAction(self.menuSubmenu_2.menuAction())
        self.menubar.addAction(self.menuMenu.menuAction())

        #self.toolBar.addAction(self.actionSub_menu)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def upSelectedParkingLots(self):
        for parking_lot in self.selectedParkingLots:
            x1 = parking_lot.points[0][0][0]
            y1 = parking_lot.points[0][0][1]

            x2 = parking_lot.points[1][0][0]
            y2 = parking_lot.points[1][0][1]

            x3 = parking_lot.points[2][0][0]
            y3 = parking_lot.points[2][0][1]

            x4 = parking_lot.points[3][0][0]
            y4 = parking_lot.points[3][0][1]

            pts = numpy.array([list( (x1,y1 - 1) ), list((x2,y2 - 1)), list((x3,y3 - 1)), list((x4,y4 - 1))], numpy.int32)
            parking_lot.points = pts.reshape((-1, 1, 2))


    def downSelectedParkingLots(self):
        for parking_lot in self.selectedParkingLots:
            x1 = parking_lot.points[0][0][0]
            y1 = parking_lot.points[0][0][1]

            x2 = parking_lot.points[1][0][0]
            y2 = parking_lot.points[1][0][1]

            x3 = parking_lot.points[2][0][0]
            y3 = parking_lot.points[2][0][1]

            x4 = parking_lot.points[3][0][0]
            y4 = parking_lot.points[3][0][1]

            pts = numpy.array([list( (x1,y1 + 1) ), list((x2,y2 + 1)), list((x3,y3 + 1)), list((x4,y4 + 1))], numpy.int32)
            parking_lot.points = pts.reshape((-1, 1, 2))


    def leftSelectedParkingLots(self):
        for parking_lot in self.selectedParkingLots:
            x1 = parking_lot.points[0][0][0]
            y1 = parking_lot.points[0][0][1]

            x2 = parking_lot.points[1][0][0]
            y2 = parking_lot.points[1][0][1]

            x3 = parking_lot.points[2][0][0]
            y3 = parking_lot.points[2][0][1]

            x4 = parking_lot.points[3][0][0]
            y4 = parking_lot.points[3][0][1]

            pts = numpy.array([list((x1- 1, y1)), list((x2- 1, y2 )), list((x3- 1, y3 )), list((x4- 1, y4 ))],
                              numpy.int32)
            parking_lot.points = pts.reshape((-1, 1, 2))


    def rightSelectedParkingLots(self):
        for parking_lot in self.selectedParkingLots:
            x1 = parking_lot.points[0][0][0]
            y1 = parking_lot.points[0][0][1]

            x2 = parking_lot.points[1][0][0]
            y2 = parking_lot.points[1][0][1]

            x3 = parking_lot.points[2][0][0]
            y3 = parking_lot.points[2][0][1]

            x4 = parking_lot.points[3][0][0]
            y4 = parking_lot.points[3][0][1]

            pts = numpy.array([list((x1 + 1, y1)), list((x2 + 1, y2)), list((x3 + 1, y3)), list((x4 + 1, y4))],
                              numpy.int32)
            parking_lot.points = pts.reshape((-1, 1, 2))

    def getFirstPoint(self, points):
        x1 = points[0][0][0]
        y1 = points[0][0][1]
        first = "[" + str(x1) + "," + str(y1) + "]"
        return first

    def getSecondPoint(self, points):
        x2 = points[1][0][0]
        y2 = points[1][0][1]
        second = "[" + str(x2) + "," + str(y2) + "]"
        return second

    def getThirdPoint(self, points):
        x3 = points[2][0][0]
        y3 = points[2][0][1]
        third = "[" + str(x3) + "," + str(y3) + "]"
        return third

    def getFourthPoint(self, points):
        x4 = points[3][0][0]
        y4 = points[3][0][1]
        fourth = "[" + str(x4) + "," + str(y4) + "]"
        return fourth

    def deleteSelectedSlots(self):
        API = self.manager.API
        parkingZone = self.manager.parkZoneName
        for parking_lot in self.selectedParkingLots:
            if (parking_lot.from_server == True):
                print("serverdan sil")
                API.deleteParkingLotByID(parking_lot.parkingLotID)
                # parking_lot.deleted = True
                self.manager.parking_lots.remove(parking_lot)
                # self.parkingLots.remove(parking_lot)

    def sendServer(self):
        API = self.manager.API
        parkingZone = self.manager.parkZoneName
        for parking_lot in self.selectedParkingLots:
            if (parking_lot.from_server == True):
                first = self.getFirstPoint(parking_lot.points)
                second = self.getSecondPoint(parking_lot.points)
                third = self.getThirdPoint(parking_lot.points)
                fourth = self.getFourthPoint(parking_lot.points)
                API.updateParkingLotByID(parking_lot.parkingLotID, "Available", parking_lot.updatedParkingLotID
                                         , parking_lot.parkingZone, first, second, third, fourth)
            else:
                first = self.getFirstPoint(parking_lot.points)
                second = self.getSecondPoint(parking_lot.points)
                third = self.getThirdPoint(parking_lot.points)
                fourth = self.getFourthPoint(parking_lot.points)
                API.createParkingLot("Available", parking_lot.parkingLotID, parkingZone, first, second, third, fourth)
                parking_lot.from_server = True

    def selectAll(self):
        print("Select All")
        self.selectedParkingLots = self.manager.parking_lots
        self.highLightAllSelecteds()


    def deSelectAll(self):
        print("Select All")
        self.selectedParkingLots = []
        self.highLightAllSelecteds()
        selectedRows = self.tableWidget.selectedItems()
        self.unSelectParkingLots(selectedRows)

    def startOccupancyDetection(self):
        if self.occupancyDetectionStarted == False:
            self.manager.occupancyDetectionStarted = True
            self.occupancyDetectionStarted = True
            self.detectOccupancy.setText("Stop Detection")
        else:
            self.manager.occupancyDetectionStarted = False
            self.occupancyDetectionStarted = False
            self.detectOccupancy.setText("Start Detection")

    def startSlotDetection(self):

        import sys
        sys.path.append('C:/tensorflow1/models; C:/tensorflow1/models/research;C:/tensorflow1/models/research/slim')

        if self.slotDetectionStarted == False:
            self.manager.slotDetectionStarted = True
            self.slotDetectionStarted = True
            self.detectSlot.setText("Stop ParkingSlot Detection")
        else:
            self.manager.slotDetectionStarted = False
            self.slotDetectionStarted = False
            self.detectSlot.setText("Show ParkingSlot Detection")

    def highlightParkingLot(self, parkingLotID):
        for parking_lot in self.manager.parking_lots:
            if (parking_lot.parkingLotID == parkingLotID):
                parking_lot.highlight()

    def unSelectParkingLots(self, selectedRows):
        i = 1
        tempSelecteds = []
        for parking_lot in self.manager.parking_lots:
            isSelected = False
            for row in selectedRows:
                if (i % 5 == 1):
                    if (parking_lot.parkingLotID == row.text()):
                        isSelected =True
                        tempSelecteds.append(parking_lot)

                i = i + 1
            if (isSelected == False):
                parking_lot.releaseHighlight()
        self.selectedParkingLots = tempSelecteds

    def highLightAllSelecteds(self):
        for parking_lot in self.selectedParkingLots:
            parking_lot.highlight()


    def selectionChange(self):
        selectedRows = self.tableWidget.selectedItems()
        i = 1
        self.unSelectParkingLots(selectedRows)
        for row in selectedRows:
            if (i % 5 == 1):
                self.highlightParkingLot(str(row.text()))
            i = i + 1

    def tabChange(self, i):
        if (i == 1):
            self.parkingLots = self.manager.parking_lots
            i = 0

            for j in range(50):
                self.tableWidget.setItem(j, 0, QtWidgets.QTableWidgetItem(""))
                self.tableWidget.setItem(j, 1, QtWidgets.QTableWidgetItem(""))
                self.tableWidget.setItem(j, 2, QtWidgets.QTableWidgetItem(""))
                self.tableWidget.setItem(j, 3, QtWidgets.QTableWidgetItem(""))
                self.tableWidget.setItem(j, 4, QtWidgets.QTableWidgetItem(""))
                j = j + 1

            for parking_lot in self.manager.parking_lots:
                x1 = parking_lot.points[0][0][0]
                y1 = parking_lot.points[0][0][1]

                x2 = parking_lot.points[1][0][0]
                y2 = parking_lot.points[1][0][1]

                x3 = parking_lot.points[2][0][0]
                y3 = parking_lot.points[2][0][1]

                x4 = parking_lot.points[3][0][0]
                y4 = parking_lot.points[3][0][1]

                firstPoint = str(" ( " + str(x1) + " , " + str(y1) + " ) ")
                secondPoint = str(" ( " + str(x2) + " , " + str(y2) + " ) ")
                thirdPoint = str(" ( " + str(x3) + " , " + str(y3) + " ) ")
                fourthPoint = str(" ( " + str(x4) + " , " + str(y4) + " ) ")

                self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(parking_lot.parkingLotID))
                self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(firstPoint))
                self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(secondPoint))
                self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(thirdPoint))
                self.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(fourthPoint))
                i = i + 1

    def openVideo(self):
        print("Menu")


    def notifyFunction(self):
        print("Bana dokundu")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("MainWindow", "Live Stream"))

        """ Rows """
        """
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Row"))

        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Row"))

        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Row"))

        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "New Row"))
        """

        """ Columns """

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Parking Lot ID"))

        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Point 1"))

        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Point 2"))

        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Point 3"))

        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Point 4"))



        self.detectOccupancy.setText(_translate("MainWindow", "Start Detection"))
        self.detectSlot.setText(_translate("MainWindow", "Detection of Parking Slot"))

        #self.menuMenu.setTitle(_translate("MainWindow", "&Menu"))
        #self.menuSubmenu_2.setTitle(_translate("MainWindow", "&Submenu 2"))


        #self.dockWidget2.setWindowTitle(_translate("MainWindow", "Parking Slots"))
        #self.actionSub_menu.setToolTip(_translate("MainWindow", "submenu"))




def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()


    ui = Ui_MainWindow()
    ui.setupUi(window)

    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)
    videoViewer = ImageViewer()

    vid.VideoSignal.connect(videoViewer.setImage)
    startVideoButton = QtWidgets.QPushButton('Open Camera')
    startVideoButton.clicked.connect(vid.startVideo)

    ui.VideoPlayer.addWidget(videoViewer)
    ui.VideoPlayer.addWidget(startVideoButton)
    ui.manager = vid

    videoViewer.triggerFunction = ui.notifyFunction
    window.setWindowTitle("Tobb ETU Smart Car Park Admin Panel")


    app.setStyleSheet(PyQt5_stylesheets.load_stylesheet_pyqt5(style="style_Dark"))

    if "--travis" in sys.argv:
        QtCore.QTimer.singleShot(2000, app.exit)

    window.showMaximized()
    app.exec_()


if __name__ == "__main__":
    main()


