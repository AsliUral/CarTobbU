from PIL import Image, ImageTk
import tkinter as tk
import argparse
import datetime
import cv2
import os


class Application:
    def __init__(self, output_path = "./"):
        self.vs = cv2.VideoCapture("../parking_lot_manage_mark/video/parking_lot_1.mp4")
        self.output_path = output_path
        self.current_image = None

        self.root = tk.Tk()
        self.root.title("Tobb ETU Smart Car Park")

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