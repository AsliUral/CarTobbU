# Importing necessary libraries, mainly the OpenCV, and PyQt libraries
import cv2
import numpy as np
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
import time
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QToolBar, QToolButton, QPushButton, QListWidget, QListWidgetItem, QVBoxLayout

from tobb_etu_smart_park_desktop_app.GUI.parking_lot import ParkingLot
#from tobb_etu_smart_car_park_python_api import smart_car_park_python_api

def getPoint(point):
    if point is not None:
        point = point[1:len(point) - 1]
        point = point.split(',')
        return [int(point[0]) , int(point[1])]

def get_parking_lots(API):
    parking_lot_JSON = API.getAllParkingLotsOFParkZone()
    parkingLots = []
    counter = 1
    max = 0
    for i in range(len(parking_lot_JSON)):
        if (parking_lot_JSON[i]["FirstPoint"] is not None and parking_lot_JSON[i]["FirstPoint"] != ''):
            parkingLots.append(ParkingLot(
                                          from_server=True,
                                          parkingLotID=parking_lot_JSON[i]["ParkingLotID"],
                                          pt1=(getPoint(parking_lot_JSON[i]["FirstPoint"])[0],getPoint(parking_lot_JSON[i]["FirstPoint"])[1]),
                                          pt2=(getPoint(parking_lot_JSON[i]["SecondPoint"])[0],getPoint(parking_lot_JSON[i]["SecondPoint"])[1]),
                                          pt3=(getPoint(parking_lot_JSON[i]["ThirdPoint"])[0],getPoint(parking_lot_JSON[i]["ThirdPoint"])[1]),
                                          pt4=(getPoint(parking_lot_JSON[i]["FourthPoint"])[0],getPoint(parking_lot_JSON[i]["FourthPoint"])[1]),
                                          API=API,
                                          parkingZone=parking_lot_JSON[i]["ParkZoneName"]))
            counter += 1
            id = parking_lot_JSON[i]["ParkingLotID"]
            if (int(id[1:]) > max):
                max = int(id[1:])

    print("Return : " , parkingLots)
    return parkingLots, max + 1


cameraID = "1"
parkZoneID = "15"
apiKey = "ABC"
#API = smart_car_park_python_api.SmartCarParkAPI(cameraID, parkZoneID, apiKey)


#parking_lots, tempID  = get_parking_lots(API)

COLOR_WHITE = (255, 255, 255)

fps = 25

startDetection = False
currentlyMarked = False

pt1 = (0, 0)
pt2 = (0, 0)
pt3 = (0, 0)
pt4 = (0, 0)
topLeft_clicked = False
botRight_clicked = False
botLeft_clicked = False
topRight_clicked = False

coordinates = []
points = []


def slot_method():
    print('slot method called.')



class ShowVideo(QtCore.QObject):
    # initiating the built in camera
    camera_port = 'parking_lot_1.mp4'


    camera = cv2.VideoCapture(camera_port)
    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):
        run_video = True
        while run_video:
            ret, frame = self.camera.read()


            for point in points:
                cv2.circle(frame, point, 10, (0,255,255), -1)

            """
            for parking_lot in parking_lots:
                parking_lot.draw_parking_lot(frame)
                parking_lot.draw_contours(frame)
                parking_lot.draw_parking_lot_id(frame)

            if topLeft_clicked and botRight_clicked and topRight_clicked and botLeft_clicked and not currentlyMarked:
                parking_lot = ParkingLot(pt1, pt2, pt3, pt4, "U" + str(tempID), "Tobb ETU Main", API, from_server=False)
                parking_lots.append(parking_lot)
                parking_lot.draw_parking_lot(frame)
                tempID = tempID + 1
                currentlyMarked = True
                
            """


            color_swapped_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            height, width, _ = color_swapped_image.shape

            # width = camera.set(CAP_PROP_FRAME_WIDTH, 1600)
            # height = camera.set(CAP_PROP_FRAME_HEIGHT, 1080)
            # camera.set(CAP_PROP_FPS, 15)

            qt_image = QtGui.QImage(color_swapped_image.data,
                                    width,
                                    height,
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)


            self.VideoSignal.emit(qt_image)



            time.sleep(1 / fps)


class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.mouseReleaseEvent = self.draw_polygon




    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def draw_polygon(self, event):

        x = event.x()
        y = event.y()
        #image = cv2.circle(image, center_coordinates, radius, color, thickness)
        points.append((x, y))


        print("X : " , x , " Y : " , y)

        """
        global pt1, pt2, pt3, pt4, topLeft_clicked, botRight_clicked, topRight_clicked, botLeft_clicked
        global currentlyMarked

        if topLeft_clicked == True and botRight_clicked == True and botLeft_clicked == True and topRight_clicked == True:
            topLeft_clicked = False
            botRight_clicked = False
            botLeft_clicked = False
            topRight_clicked = False
            pt1 = (0, 0)
            pt2 = (0, 0)
            pt3 = (0, 0)
            pt4 = (0, 0)
            currentlyMarked = False

        if topLeft_clicked == False:
            pt1 = (x, y)
            topLeft_clicked = True

        elif botRight_clicked == False:
            pt2 = (x, y)
            botRight_clicked = True

        elif botLeft_clicked == False:
            pt3 = (x, y)
            botLeft_clicked = True

        elif topRight_clicked == False:
            pt4 = (x, y)
            topRight_clicked = True
        """

    def clickEvent(self, event):
        print("X : ", event.x() , " Y : " , event.y())

    def initUI(self):
        self.setWindowTitle('Test')

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Parking Lots'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def createTable(self):
        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Lot (1,1,1,1)"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Lot (1,2,3,4)"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Lot (2,1,3,5)"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("Lot (2,2,4,3)"))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Lot (3,1,5,6)"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("Lot (3,2,4,4)"))
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Lot (4,1,2,4)"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("Lot (4,2,7,8)"))
        self.tableWidget.move(0, 0)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


class App2(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Tobb Etu Car Park'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)
    image_viewer = ImageViewer()



    vid.VideoSignal.connect(image_viewer.setImage)

    # Button to start the videocapture:

    push_button1 = QtWidgets.QPushButton('Start')
    #push_button2 = QtWidgets.QPushButton('Test')
    push_button1.clicked.connect(vid.startVideo)
    vertical_layout = QtWidgets.QVBoxLayout()

    vertical_layout.addWidget(image_viewer)
    vertical_layout.addWidget(push_button1)
    #vertical_layout.addWidget(push_button2)

    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)

    # Create pyqt toolbar
    toolBar = QToolBar()
    vertical_layout.addWidget(toolBar)

    # Add buttons to toolbar
    toolButton = QToolButton()
    toolButton.setText("Dnm1")
    toolButton.setCheckable(True)
    toolButton.setAutoExclusive(True)
    toolBar.addWidget(toolButton)

    colorButton = QtWidgets.QPushButton("Dnm2")
    exitAct = QtWidgets.QAction('Dnm3')
    toolBar.addWidget(colorButton)
    toolBar.addAction(exitAct)

    menu = QtWidgets.QMenu()
    menu.addAction("red")
    menu.addAction("green")
    menu.addAction("blue")
    colorButton.setMenu(menu)

    button = QPushButton("Click")
    button.clicked.connect(slot_method)

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)

    main_window.show()
    ex = App()
    ex2 = App2()
    sys.exit(app.exec_())