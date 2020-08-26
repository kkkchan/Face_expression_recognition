import tkinter
import cv2
import time
from PIL import Image, ImageTk


class MyVideoCapture:
    """docstring for MyVideoCapture"""
    def __init__(self, video_source=0, rate):
        self.rate = rate
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError('Unable to open video source', video_source)
        
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH) * rate)
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT) * rate)

    
    def get_frame(self):
        if self.vid.isOpened():
            flag, frame = self.vid.read()
            # print(frame.shape)
            frame = cv2.resize(frame, (int(frame.shape[1] * self.rate), int(frame.shape[0] * self.rate)))
            # print(frame.shape)
            if flag:
                return (flag, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (flag, None)


    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


class App:
    def __init__(self, window, window_title, rate=0.5):
        self.window = window
        self.window.title(window_title)
        self.vid = MyVideoCapture(rate=rate)
        self.rate = rate
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        self.btn_snapshot = tkinter.Button(window, text='截图', width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        self.btn_exit = tkinter.Button(window, text='关闭', width=50, command=self.window.destroy)
        self.btn_exit.pack(anchor=tkinter.CENTER, expand=True)


        self.delay = 10
        self.update()

        self.window.mainloop()


    def snapshot(self):
        flag, frame = self.vid.get_frame()

        if flag:
            cv2.imwrite('snapshot-' + time.strftime("%d-%m-%Y-%H-%M-%S") + '.jpg',
                cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 1))



    def update(self):
        flag, frame = self.vid.get_frame()

        if flag:
            # cv2.flip(frame, 1)实现水平翻转，即自拍镜像
            self.pic = ImageTk.PhotoImage(image=Image.fromarray(cv2.flip(frame, 1)))
            self.canvas.create_image(0, 0, image=self.pic, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")