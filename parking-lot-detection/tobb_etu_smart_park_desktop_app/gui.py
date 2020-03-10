from PIL import Image, ImageTk
import tkinter as tk
import argparse
import datetime
import cv2
import os
from tobb_etu_smart_car_park_python_api import smart_car_park_python_api
import numpy
from parking_lot_manage_mark.parking_lot import ParkingLot
from tobb_etu_smart_car_park_python_api import smart_car_park_python_api
from parking_lot_manage_mark import parking_lot


def getPoint(point):
    if point is not None:
        point = point[1:len(point) - 1]
        point = point.split(',')
        return [int(point[0]), int(point[1])]


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
                pt1=(getPoint(parking_lot_JSON[i]["FirstPoint"])[0], getPoint(parking_lot_JSON[i]["FirstPoint"])[1]),
                pt2=(getPoint(parking_lot_JSON[i]["SecondPoint"])[0], getPoint(parking_lot_JSON[i]["SecondPoint"])[1]),
                pt3=(getPoint(parking_lot_JSON[i]["ThirdPoint"])[0], getPoint(parking_lot_JSON[i]["ThirdPoint"])[1]),
                pt4=(getPoint(parking_lot_JSON[i]["FourthPoint"])[0], getPoint(parking_lot_JSON[i]["FourthPoint"])[1]),
                API=API,
                parkingZone=parking_lot_JSON[i]["ParkZoneName"]))
            counter += 1
            id = parking_lot_JSON[i]["ParkingLotID"]
            if (int(id[1:]) > max):
                max = int(id[1:])

    print("Return : ", parkingLots)
    return parkingLots, max + 1


def draw_polygon(self, event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Calisti")
        if self.topLeft_clicked == True and self.botRight_clicked == True and self.botLeft_clicked == True and self.topRight_clicked == True:
            self.topLeft_clicked = False
            self.botRight_clicked = False
            self.botLeft_clicked = False
            self.topRight_clicked = False
            self.pt1 = (0, 0)
            self.pt2 = (0, 0)
            self.pt3 = (0, 0)
            self.pt4 = (0, 0)
            self.currentlyMarked = False

        if self.topLeft_clicked == False:
            self.pt1 = (x, y)
            self.topLeft_clicked = True

        elif self.botRight_clicked == False:
            self.pt2 = (x, y)
            self.botRight_clicked = True

        elif self.botLeft_clicked == False:
            self.pt3 = (x, y)
            self.botLeft_clicked = True

        elif self.topRight_clicked == False:
            self.pt4 = (x, y)
            self.topRight_clicked = True


class Application:
    def __init__(self, output_path="./"):
        self.vs = cv2.VideoCapture("../parking_lot_manage_mark/video/parking_lot_1.mp4")
        self.output_path = output_path
        self.current_image = None

        self.COLOR_WHITE = (255, 255, 255)
        cameraID = "1"
        parkZoneID = "8"
        apiKey = "ABC"
        camera = 'video/parking_lot_1.mp4'

        self.API = smart_car_park_python_api.SmartCarParkAPI(cameraID, parkZoneID, apiKey)
        self.parking_lots, self.tempID = get_parking_lots(self.API)

        self.ids = 0
        self.a = 1
        self.startDetection = False
        self.currentlyMarked = False

        self.pt1 = (0, 0)
        self.pt2 = (0, 0)
        self.pt3 = (0, 0)
        self.pt4 = (0, 0)
        self.topLeft_clicked = False
        self.botRight_clicked = False
        self.botLeft_clicked = False
        self.topRight_clicked = False

        self.root = tk.Tk()
        self.root.title("Tobb ETU Smart Car Park")

        # cv2.namedWindow('Tobb Etu Car Park')

        # cv2.setMouseCallback('Tobb Etu Car Park', self.draw_polygon)

        self.panel = tk.Label(self.root)
        self.panel.pack(padx=10, pady=10)

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file = tk.Menu(self.menu)

        self.menu.add_cascade(label="File", menu=self.file)

        edit = tk.Menu(self.menu)

        self.menu.add_cascade(label="Edit", menu=edit)

        btn = tk.Button(self.root, text="Snapshot!", command=self.take_snapshot)
        btn.pack(fill="both", expand=True, padx=10, pady=10)

        self.video_loop()

    def video_loop(self):
        ok, frame = self.vs.read()
        for parking_lot in self.parking_lots:
            parking_lot.draw_parking_lot(frame)
            parking_lot.draw_contours(frame)
            parking_lot.draw_parking_lot_id(frame)

        if self.topLeft_clicked and self.botRight_clicked and self.topRight_clicked and self.botLeft_clicked and not self.currentlyMarked:
            parking_lot = ParkingLot(self.pt1, self.pt2, self.pt3, self.pt4, "C" + str(self.tempID), "Marking Place",
                                     self.API, from_server=False)
            self.parking_lots.append(parking_lot)
            parking_lot.draw_parking_lot(frame)
            self.tempID = self.tempID + 1
            self.currentlyMarked = True

        if ok:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)

        self.root.after(30, self.video_loop)

    def take_snapshot(self):
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.join(self.output_path, filename)
        self.current_image.save(p, "JPEG")
        print("[INFO] saved {}".format(filename))

    def destructor(self):
        print("[INFO] closing...")
        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()


pba = Application()
pba.root.mainloop()
