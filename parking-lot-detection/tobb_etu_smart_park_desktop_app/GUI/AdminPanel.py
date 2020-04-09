import re
import sys
import time
from functools import partial

import PyQt5
from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QPushButton, QDockWidget, QWidget, QMessageBox, QFrame, \
    QProgressBar, QDialog, QMdiSubWindow
from PyQt5.QtCore import Qt, QSize, QRegExp

from tobb_etu_smart_car_park_python_api import smart_car_park_python_api
from tobb_etu_smart_park_desktop_app.GUI import VideoEditor
from PyQt5 import QtCore, QtGui, QtWidgets

from tobb_etu_smart_park_desktop_app.GUI import PyQt5_stylesheets
from tobb_etu_smart_park_desktop_app.GUI.System import System
from tobb_etu_smart_park_desktop_app.GUI.VideoEditor import ShowVideo, ImageViewer, getPoint
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QRegExpValidator
import numpy
import sys
import threading
import cv2

from tobb_etu_smart_park_desktop_app.GUI.parking_lot import ParkingLot
from tobb_etu_smart_park_desktop_app.GUI.parking_zone import ParkingZone

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QPushButton)

blur = QtWidgets.QGraphicsBlurEffect(blurRadius=5)
cameraID = "global"
parkZoneID = "global"
parkZoneName = "global"

apiKey = "ABC"
tempUi = None
globalAPI = smart_car_park_python_api.SmartCarParkAPI(cameraIP=cameraID,
                                                      parkZoneID=parkZoneID,
                                                      apiKey = apiKey,
                                                      parkZoneName = parkZoneName)
TIME_LIMIT = 100
def getParkingZone():
    zones_JSON = globalAPI.getAllParkZones()
    counter = 0
    parkzones = []
    #zones_JSON[i]["ParkZoneName"] this will change with zones_JSON[i]["CameraIP"] after server update
    for i in range(len(zones_JSON)):
        if (zones_JSON[i]["ParkZoneName"] is not None and zones_JSON[i]["ParkZoneName"] != ''):
            cameraIP = "151.654.15.76"
            if counter == 0:
                cameraIP = "151.654.15.76"
            elif counter == 1:
                cameraIP = "151.654.15.75"
            parkzones.append(ParkingZone(
                parkingZoneID=zones_JSON[i]["ParkingZoneID"],
                parkZoneName=zones_JSON[i]["ParkZoneName"],
                API=globalAPI,
                cameraIP=cameraIP + ".mp4"
            ))
            counter += 1
    return parkzones


class Ui_MainWindow():
    def setupUi(self, MainWindow):
        self.parkzones = []
        self.severParkinglots = []

        self.parkZoneButtons = []

        self.mainW = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1068, 824)

        self.selectedParkingLots = []
        self.occupancyDetectionStarted = False
        self.slotDetectionStarted = False

        self.autoIncrementVal = None
        self.slotIDLetter = None

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

        self.tableWidget.itemChanged.connect(self.tableChange)

        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(150)

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

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)

        self.gridLayout_7.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_5, "Parking Slot Table")

        self.gridLayout.addWidget(self.tabWidget_2, 0, 0, 1, 1)

        self.lotIDLetterText = QtWidgets.QLineEdit(self.tab)
        self.lotIDLetterText.setFixedWidth(175)
        self.lotIDLetterText.setPlaceholderText("LotLetter")
        self.lotIDLetterText.textChanged.connect(self.changeLetter)
        self.lotIDLetterText.setObjectName("lotIDLetterEdit")
        self.gridLayout_7.addWidget(self.lotIDLetterText, 2, 0, 1, 1)

        self.autoIncrementText = QtWidgets.QLineEdit(self.tab)
        self.autoIncrementText.setFixedWidth(175)
        self.autoIncrementText.setPlaceholderText("AutoIncrement")
        self.autoIncrementText.textChanged.connect(self.changeIncrement)
        self.autoIncrementText.setObjectName("lotIDLetterEdit2")
        self.gridLayout_7.addWidget(self.autoIncrementText, 3, 0, 1, 1)


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

        self.startSystemButton = QtWidgets.QAction(QIcon('./buttonIcons/startSystem.jpg'), "Start System", MainWindow)
        self.startSystemButton.setStatusTip("Start System")
        self.startSystemButton.triggered.connect(self.startSystem)
        self.toolBar.addAction(self.startSystemButton)


        self.docked = QtWidgets.QDockWidget(MainWindow)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.docked)
        self.dockedWidget = QtWidgets.QWidget()
        self.dockedWidget.setObjectName("dockedWidget")
        self.docked.setWidget(self.dockedWidget)
        self.dockedWidget.setLayout(QVBoxLayout())

        self.actionSub_menu = QtWidgets.QAction(MainWindow)
        self.actionSub_menu.setObjectName("actionSub_menu")



        #self.menuSubmenu_2.addAction(self.actionSub_menu)
        #self.menuMenu.addAction(self.menuSubmenu_2.menuAction())
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def findParkZone(self, parkZoneName):
        for parkzone in self.parkzones:
            if (parkZoneName == parkzone.parkZoneName):
                parkzone.isSelected = True
                self.manager.startVideo()
            else:
                parkzone.isSelected = False


    def parkZoneSelected(self):
        counter = 0
        noSelectedButton = True
        for button in self.parkZoneButtons:
            if(button.isChecked() == False):
                self.parkzones[counter].isSelected = True
                noSelectedButton = False
                self.manager.stopped = False
            else:
                self.parkzones[counter].isSelected = False
            counter = counter + 1

        if noSelectedButton == True:
            self.manager.stopped = True
            self.manager.run_video = False

        self.manager.parkzones = self.parkzones

    def changeIncrement(self, newIncrementValue):
        self.manager.autoIncrement = newIncrementValue
        print("Change incerement : " , newIncrementValue)

    def changeLetter(self, newAutoLetter):
        self.manager.autoLetter = newAutoLetter
        print("Change auto letter : ", newAutoLetter)

    def getServerParkingLots(self):
        lots_JSON = globalAPI.getAllParkingLots()
        counter = 0
        for i in range(len(lots_JSON)):
            if (lots_JSON[i]["FirstPoint"] is not None and lots_JSON[i]["FirstPoint"] != ''):
                self.severParkinglots.append(ParkingLot(
                    from_server=True,
                    parkingLotID=lots_JSON[i]["ParkingLotID"],
                    pt1=(
                    getPoint(lots_JSON[i]["FirstPoint"])[0], getPoint(lots_JSON[i]["FirstPoint"])[1]),
                    pt2=(
                    getPoint(lots_JSON[i]["SecondPoint"])[0], getPoint(lots_JSON[i]["SecondPoint"])[1]),
                    pt3=(
                    getPoint(lots_JSON[i]["ThirdPoint"])[0], getPoint(lots_JSON[i]["ThirdPoint"])[1]),
                    pt4=(
                    getPoint(lots_JSON[i]["FourthPoint"])[0], getPoint(lots_JSON[i]["FourthPoint"])[1]),
                    API=globalAPI,
                    parkingZone=lots_JSON[i]["ParkZoneName"]))

        return counter


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
                API.deleteParkingLotByID(parking_lot.parkingLotID)
                # parking_lot.deleted = True
                self.manager.parking_lots.remove(parking_lot)
                # self.parkingLots.remove(parking_lot)
            else:
                # parking_lot.deleted = True
                self.manager.parking_lots.remove(parking_lot)
                # self.parkingLots.remove(parking_lot)




    def startSystem(self):
        (yolo, classes) = self.manager.getOccupancyModelConfg()
        self.systems = []
        for zone in self.parkzones:
            self.systems.append(System(zone))
        while(True):
            counter = 0
            for system in self.systems:
                if (counter == 1 or counter == 10):
                    camera = system.camera
                    frame = system.readFrame()
                    # Noise
                    blur = cv2.GaussianBlur(frame.copy(), (5, 5), 3)
                    # Minimize data
                    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
                    pos_sec = camera.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

                    for i in range(len(system.parkingLots_ODetection)):
                        system.parkingLots_ODetection[i].check(pos_sec, gray, system.API, yolo, classes, frame)
                        system.parkingLots_ODetection[i].draw(frame)
                counter = counter + 1


    def sendServer(self):
        API = self.manager.API
        parkingZone = self.manager.parkZoneName
        for parking_lot in self.selectedParkingLots:
            if (parking_lot.from_server == True):
                first = self.getFirstPoint(parking_lot.points)
                second = self.getSecondPoint(parking_lot.points)
                third = self.getThirdPoint(parking_lot.points)
                fourth = self.getFourthPoint(parking_lot.points)
                if (parking_lot.originalID != None):
                    API.updateParkingLotByID(parking_lot.originalID, "Available", parking_lot.parkingLotID
                                         , parking_lot.parkingZone, first, second, third, fourth)
                else:
                    API.updateParkingLotByID(parking_lot.parkingLotID, "Available", parking_lot.parkingLotID
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
                if (i % 6 == 1):
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
            if (i % 6 == 1):
                self.highlightParkingLot(str(row.text()))
            i = i + 1

    def findChanged(self):
        for parking_lot in self.selectedParkingLots:
            if (parking_lot.from_server == True):
                #API.deleteParkingLotByID(parking_lot.parkingLotID)
                # parking_lot.deleted = True
                self.manager.parking_lots.remove(parking_lot)
                # self.parkingLots.remove(parking_lot)
            else:
                # parking_lot.deleted = True
                self.manager.parking_lots.remove(parking_lot)
                # self.parkingLots.remove(parking_lot)

    def tableChange(self, item):
        newValue = item.text()
        changedColumn = item.column()
        changedRow = item.row()
        if (item.isSelected() == True and newValue != "" and changedColumn == 0 and self.isduplicated(newValue) == False):
            self.manager.parking_lots[changedRow].updateID(newValue)


    def isduplicated(self, newValue):
        isduplicated = False
        number = self.getServerParkingLots()
        for lots in self.severParkinglots:
            if lots.parkingLotID == newValue:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error updating duplicate parking lot entry!")
                msg.setWindowTitle("Error Parking Lots Tab")
                msg.exec_()
                isduplicated = True
        return isduplicated

    def tabChange(self, i):
        self.autoIncrementText.setText(str(self.manager.autoIncrement))
        self.lotIDLetterText.setText(str(self.manager.autoLetter))
        if (i == 1):
            self.parkingLots = self.manager.parking_lots
            i = 0

            for j in range(50):
                self.tableWidget.setItem(j, 0, QtWidgets.QTableWidgetItem(""))
                self.tableWidget.setItem(j, 1, QtWidgets.QTableWidgetItem(""))
                self.tableWidget.setItem(j, 2, QtWidgets.QTableWidgetItem(""))
                self.tableWidget.setItem(j, 3, QtWidgets.QTableWidgetItem(""))
                self.tableWidget.setItem(j, 4, QtWidgets.QTableWidgetItem(""))
                self.tableWidget.setItem(j, 5, QtWidgets.QTableWidgetItem(""))
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
                self.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(parking_lot.parkingZone))

                i = i + 1

    def openVideo(self):
        print("Menu")

    def setChange(self,blur):
        self.mainW.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect().setEnabled(False))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("MainWindow", "Live Stream"))

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

        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Parking Zone Name"))

        self.detectOccupancy.setText(_translate("MainWindow", "Start Detection"))
        self.detectSlot.setText(_translate("MainWindow", "Detection of Parking Slot"))

        self.dockedWidget.setWindowTitle(_translate("MainWindow", "Park Zone"))


        #self.dockWidget2.setWindowTitle(_translate("MainWindow", "Park Zone"))

        #self.menuMenu.setTitle(_translate("MainWindow", "&Menu"))
        #self.menuSubmenu_2.setTitle(_translate("MainWindow", "&Submenu 2"))


        #self.dockWidget2.setWindowTitle(_translate("MainWindow", "Parking Slots"))
        #self.actionSub_menu.setToolTip(_translate("MainWindow", "submenu"))

class LoginForm(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    switch_window2 = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Login To CarTobbU')
        self.setWindowState(Qt.WindowActive)
        self.resize(500, 120)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        self.setPalette(p)
        self.center()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint  | Qt.WindowStaysOnTopHint)
        self.layout = QGridLayout()

        label_name = QLabel("Username",self)
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        self.layout.addWidget(label_name, 0, 0)
        self.layout.addWidget(self.lineEdit_username, 0, 1)

        labelPassword = QLabel("Password", self)
        labelPassword.move(60, 224)

        framePassword = QFrame(self)
        framePassword.setFrameShape(QFrame.StyledPanel)
        framePassword.move(60, 250)

        self.lineEditPassword = QLineEdit(framePassword)
        self.lineEditPassword.setFrame(False)
        self.lineEditPassword.setEchoMode(QLineEdit.Password)
        self.lineEditPassword.setTextMargins(8, 0, 4, 1)
        self.lineEditPassword.move(40, 1)
        self.lineEditPassword.setPlaceholderText('Please enter your password')


        self.layout.addWidget(labelPassword)
        self.layout.addWidget(self.lineEditPassword, 1,1)


        self.l1 = QLabel()
        self.l1.setText("Wrong password or username try again")


        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_password)
        self.layout.addWidget(button_login, 2, 0, 1, 2)
        self.layout.setRowMinimumHeight(2, 75)

        button_register = QPushButton('Register')
        button_register.clicked.connect(self.register)
        self.layout.addWidget(button_register, 3, 0, 1, 2)
        self.layout.setRowMinimumHeight(2, 75)

        button_forgot = QPushButton('Forgot my password')
        button_forgot.clicked.connect(self.forgotPassword)
        self.layout.addWidget(button_forgot, 4, 0, 1, 1)
        self.layout.setRowMinimumHeight(2, 75)

        self.setLayout(self.layout)


    def register(self):
        self.switch_window.emit()

    def forgotPassword(self):
        self.switch_window2.emit()


    def center(self):
        frameGm = self.frameGeometry()
        print(frameGm)
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(
            PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def check_password(self):
        msg = QMessageBox()
        username = self.lineEdit_username.text()
        password =  self.lineEditPassword.text()

        val = globalAPI.login(username,password)

        if val == True :
            blur = 0
            tempUi.setChange(blur=blur)
            self.close()
            self.destroy()
            #sys.exit(msg.exec_())
        else:
            self.layout.addWidget(self.l1, 3, 0, 1, 2)
            self.l1.setStyleSheet("color:red")


class ForgotPasswordForm(QtWidgets.QWidget):
        switch_window2 = QtCore.pyqtSignal()

        def __init__(self):
            super().__init__()
            QtWidgets.QWidget.__init__(self)
            self.setWindowTitle('Get New Password')
            self.setWindowState(Qt.WindowActive)
            self.resize(500, 120)
            self.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.setWindowFlags(Qt.WindowMinimizeButtonHint  | Qt.WindowStaysOnTopHint)
            self.center()
            self.layout = QGridLayout()

            label_name = QLabel("Username", self)
            self.lineEdit_username = QLineEdit()
            self.lineEdit_username.setPlaceholderText('Please enter your username')
            self.layout.addWidget(label_name, 0, 0)
            self.layout.addWidget(self.lineEdit_username, 0, 1)
            self.setLayout(self.layout)

            regexEmail = QRegExp('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
            validatorEmail = QtGui.QRegExpValidator(regexEmail, self)
            email = QLabel("Email", self)
            self.lineEdit_email = QLineEdit()
            self.lineEdit_email.setValidator(validatorEmail)
            self.lineEdit_email.setPlaceholderText('Please enter your email')
            self.layout.addWidget(email, 4, 0)
            self.layout.addWidget(self.lineEdit_email, 4, 1)

            self.empty = QLabel()
            self.empty.setText("")

            self.wrongEmail = QLabel()
            self.wrongEmail.setText("This is not a valid email address")

            self.emptyEmail = QLabel()
            self.emptyEmail.setText("Email is not be empty")

            self.l1 = QLabel()
            self.l1.setText("New password link is sent")

            button_register = QPushButton('Send Change Password Link')
            button_register.clicked.connect(self.sendPassword)
            self.layout.addWidget(button_register, 12, 0, 1, 2)
            self.layout.setRowMinimumHeight(12, 75)

            button_goToLogin = QPushButton('Go To Login')
            button_goToLogin.clicked.connect(self.ToLogin)
            self.layout.addWidget(button_goToLogin, 14, 0, 1, 2)
            self.layout.setRowMinimumHeight(12, 75)
            self.setLayout(self.layout)

        def sendPassword(self):
                email = self.lineEdit_email.text()
                #phone = self.lineEdit_phone_number.text()

                cM = self.checkMail(email)

                if (cM):
                    globalAPI.forgotPassword(email)
                    self.layout.addWidget(self.l1, 3, 0, 1, 2)
                    self.l1.setStyleSheet("color:green")

        def ToLogin(self):
            self.close()
            self.destroy()
            self.switch_window2.emit()

        def checkMail(self, email):

                regexMail = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

                if (re.search(regexMail, email)):
                    self.layout.addWidget(self.empty, 5, 0, 1, 2)
                    return True

                if (email == ""):
                    self.layout.addWidget(self.emptyEmail, 5, 0, 1, 2)
                    self.emptyEmail.setStyleSheet("color:red")
                    return False
                else:
                    self.layout.addWidget(self.wrongEmail, 5, 0, 1, 2)
                    self.wrongEmail.setStyleSheet("color:red")
                    return False

        def center(self):
                frameGm = self.frameGeometry()
                print(frameGm)
                screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(
                    PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
                centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
                frameGm.moveCenter(centerPoint)
                self.move(frameGm.topLeft())

class RegisterForm(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()

        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Create A User')
        self.setWindowState(Qt.WindowActive)
        self.resize(500, 120)
        self.center()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint  | Qt.WindowStaysOnTopHint)

        self.layout = QGridLayout()

        label_name = QLabel("Username", self)
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        self.layout.addWidget(label_name, 0, 0)
        self.layout.addWidget(self.lineEdit_username, 0, 1)

        label_name_full = QLabel("Full Name", self)
        self.lineEdit_username_full = QLineEdit()
        self.lineEdit_username_full.setPlaceholderText('Please enter your fullname')
        self.layout.addWidget(label_name_full, 2, 0)
        self.layout.addWidget(self.lineEdit_username_full, 2, 1)

        regexEmail = QRegExp('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
        validatorEmail = QtGui.QRegExpValidator(regexEmail, self)
        email = QLabel("Email", self)
        self.lineEdit_email = QLineEdit()
        self.lineEdit_email.setValidator(validatorEmail)
        self.lineEdit_email.setPlaceholderText('Please enter your email')
        self.layout.addWidget(email, 4, 0)
        self.layout.addWidget(self.lineEdit_email, 4, 1)

        self.wrongEmail = QLabel()
        self.wrongEmail.setText("This is not a valid email address")

        self.emptyEmail = QLabel()
        self.emptyEmail.setText("Email is not be empty")

        phone_number = QLabel("PhoneNumber", self)
        self.lineEdit_phone_number = QLineEdit()
        self.lineEdit_phone_number.setPlaceholderText('Please enter your phone number')
        self.layout.addWidget(phone_number, 6, 0)
        self.layout.addWidget(self.lineEdit_phone_number, 6, 1)

        labelPassword = QLabel("Password", self)
        labelPassword.move(60, 224)

        framePassword = QFrame(self)
        framePassword.setFrameShape(QFrame.StyledPanel)
        framePassword.move(60, 250)

        self.lineEditPassword = QLineEdit(framePassword)
        self.lineEditPassword.setFrame(False)
        self.lineEditPassword.setEchoMode(QLineEdit.Password)
        self.lineEditPassword.setTextMargins(8, 0, 4, 1)
        self.lineEditPassword.move(40, 1)
        self.lineEditPassword.setPlaceholderText('Please enter your password')

        self.layout.addWidget(labelPassword)
        self.layout.addWidget(self.lineEditPassword)

        self.weakPassword = QLabel()
        self.weakPassword.setText("Your password is not strong enough.")
        self.empty = QLabel()
        self.empty.setText("")

        self.solved = QLabel()
        self.solved.setText("")

        self.notSame = QLabel()
        self.notSame.setText("Your Password and Confirm Password does not match.")

        self.emptyPassword = QLabel()
        self.emptyPassword.setText("Password or Confirm Password is not be empty")

        self.notl = QLabel()
        self.notl.setText("Password must contain at least one lowercase character")
        self.notu = QLabel()
        self.notu.setText("Password must contain at least one uppercase character")
        self.notl = QLabel()
        self.notl.setText("Password must contain at least one lowercase character")
        self.notd = QLabel()
        self.notd.setText("Password must contain at least one digit character")
        self.not8 = QLabel()
        self.not8.setText("Password must contain at least 8 characters")

        self.l1 = QLabel()
        self.l1.setText("Welcome to CarTobbu, Please check email for verification!")


        labelPasswordCheck = QLabel("Enter Password Again", self)
        labelPasswordCheck.move(60, 224)

        framePasswordCheck = QFrame(self)
        framePasswordCheck.setFrameShape(QFrame.StyledPanel)
        framePasswordCheck.move(60, 250)

        self.lineEditPasswordCheck = QLineEdit(framePasswordCheck)
        self.lineEditPasswordCheck.setFrame(False)
        self.lineEditPasswordCheck.setEchoMode(QLineEdit.Password)
        self.lineEditPasswordCheck.setTextMargins(8, 0, 4, 1)
        self.lineEditPasswordCheck.move(40, 1)
        self.lineEditPasswordCheck.setPlaceholderText('Please enter your password again')

        self.layout.addWidget(labelPasswordCheck)
        self.layout.addWidget(self.lineEditPasswordCheck)

        button_register = QPushButton('Register')
        button_register.clicked.connect(self.register_function)
        self.layout.addWidget(button_register, 12, 0, 1, 2)
        self.layout.setRowMinimumHeight(12, 75)

        button_login = QPushButton('Back To Login')
        button_login.clicked.connect(self.login)
        self.layout.addWidget(button_login, 14, 0, 1, 2)
        self.layout.setRowMinimumHeight(14, 75)

        self.setLayout(self.layout)

    def checkMail(self,email):

        regexMail = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

        if (re.search(regexMail, email)):
            self.layout.addWidget(self.empty, 5, 0, 1, 2)
            return True

        if (email == ""):
            self.layout.addWidget(self.emptyEmail, 5, 0, 1, 2)
            self.emptyEmail.setStyleSheet("color:red")
            return False
        else:
            self.layout.addWidget(self.wrongEmail, 5, 0, 1, 2)
            self.wrongEmail.setStyleSheet("color:red")
            return False

    def checkPassword(self,password,checkPassword):

        regexPassword = '[A-Za-z0-9@#$%^&+=*?!]{8,}'
        charRegex = re.compile(r'(\w{8,})')  # Check if password has atleast 8 characters
        lowerRegex = re.compile(r'[a-z]+')  # Check if at least one lowercase letter
        upperRegex = re.compile(r'[A-Z]+')  # Check if atleast one upper case letter
        digitRegex = re.compile(r'[0-9]+')  # Check if at least one digit.

        if (password != checkPassword):
            self.layout.addWidget(self.notSame, 9, 0, 1, 2)
            self.notSame.setStyleSheet("color:red")
            return False
        if (password == "" or checkPassword==""):
            self.layout.addWidget(self.emptyPassword, 9, 0, 1, 2)
            self.emptyPassword.setStyleSheet("color:red")
            return False
        if charRegex.findall(
                password) == []:
            self.layout.addWidget(self.not8, 9, 0, 1, 2)
            self.not8.setStyleSheet("color:red")
            return False
        elif lowerRegex.findall(
                password) == []:
            self.layout.addWidget(self.notl, 9, 0, 1, 2)
            self.notl.setStyleSheet("color:red")
            return False
        elif upperRegex.findall(
                password) == []:
            self.layout.addWidget(self.notu, 9, 0, 1, 2)
            self.notu.setStyleSheet("color:red")
            return False

        elif digitRegex.findall(
                password) == []:
            self.layout.addWidget(self.notd, 9, 0, 1, 2)
            self.notd.setStyleSheet("color:red")
            return False

        else:
            self.layout.addWidget(self.solved, 9, 0, 1, 2)
            return True


    def login(self):
        self.close()
        self.destroy()
        self.switch_window.emit()

    def center(self):
        frameGm = self.frameGeometry()
        print(frameGm)
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(
            PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def register_function(self):

        username = self.lineEdit_username.text()
        password =  self.lineEditPassword.text()
        checkPassword = self.lineEditPasswordCheck.text()
        fullname =  self.lineEdit_username_full.text()
        email = self.lineEdit_email.text()
        phone = self.lineEdit_phone_number.text()

        cM = self.checkMail(email)
        cP = self.checkPassword(password,checkPassword)

        if(cM and cP):
            val = globalAPI.register(username,fullname,password,email,phone)

            if val == True :
                print("basarili")
                self.layout.addWidget(self.l1,  9, 0, 1, 2)
                self.l1.setStyleSheet("color:green")
                #sys.exit(msg.exec_())
            else:
                print("yanlis")
                self.layout.addWidget(self.l1,  9, 0, 1, 2)
                self.l1.setStyleSheet("color:red")



class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = LoginForm()
        self.login.switch_window.connect(self.show_main)
        self.login.switch_window2.connect(self.forgotPassword)
        self.login.show()

    def show_main(self):
        self.window = RegisterForm()
        self.window.switch_window.connect(self.show_login)
        self.login.close()
        self.window.show()

    def forgotPassword(self):
        self.window = ForgotPasswordForm()
        self.window.switch_window2.connect(self.show_login)
        self.login.close()
        self.window.show()



def main():

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    form = LoginForm()
    getattr(form, "raise")()
    form.activateWindow()

    window.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect(blur))
    #window.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect())
    ui = Ui_MainWindow()
    ui.setupUi(window)


    global tempUi
    tempUi = ui

    form.main = ui
    controller = Controller()
    controller.show_login()

    thread = QtCore.QThread()
    thread.start()
    cameraList = ["tobb_etu_main.mp4", "parking_lot_1.mp4"]
    vid = ShowVideo()
    vid.cameraList = cameraList
    vid.camera = "1"
    vid.moveToThread(thread)
    videoViewer = ImageViewer()

    vid.VideoSignal.connect(videoViewer.setImage)

    parkzones = getParkingZone()
    vid.parkzones = parkzones
    ui.parkzones = parkzones
    for parkzone in parkzones:
        parkZoneButton = QPushButton(parkzone.parkZoneName)
        parkZoneButton.setCheckable(True)
        parkZoneButton.toggle()
        parkZoneButton.clicked.connect(vid.startVideo)
        ui.parkZoneButtons.append(parkZoneButton)
        ui.dockedWidget.layout().addWidget(parkZoneButton)

    for button in ui.parkZoneButtons:
        button.clicked.connect(ui.parkZoneSelected)

    ui.VideoPlayer.addWidget(videoViewer)
    ui.manager = vid
    window.setWindowTitle("Tobb ETU Smart Car Park Admin Panel")

    app.setStyleSheet(PyQt5_stylesheets.load_stylesheet_pyqt5(style="style_Dark"))


    if "--travis" in sys.argv:
        QtCore.QTimer.singleShot(2000, app.exit)

    window.showMaximized()
    app.exec_()
    sys.exit(app.exec_())




if __name__ == "__main__":
    main()


