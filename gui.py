import tkinter
import cv2
import time
import numpy as np 
from PIL import Image, ImageTk
from tensorflow import keras


emotion_dict = {0: "   Angry   ", 1: "Disgusted", 2: "  Fearful  ", 3: "   Happy   ", 4: "  Neutral  ", 5: "    Sad    ", 6: "Surprised"}
emotion_model = keras.models.load_model('model.h5')
show_text=[0]


class MyVideoCapture:
    """docstring for MyVideoCapture"""
    def __init__(self, video_source=0, rate=1):
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


    def box(self):
        bounding_box = cv2.CascadeClassifier('/Users/kimon/opt/anaconda3/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml')
        if bounding_box.empty():
            print('File not exists!')
        _, frame = self.get_frame()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        num_faces = bounding_box.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame1, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)
            prediction = emotion_model.predict(cropped_img)
            
            maxindex = int(np.argmax(prediction))
            cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            show_text[0]=maxindex


    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


class App:
    def __init__(self, window, window_title, rate=1):
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


        # 时延
        self.delay = 50
        self.update()

        self.window.mainloop()


    def snapshot(self):
        flag, frame = self.vid.get_frame()

        if flag:
            cv2.imwrite('snapshot-' + time.strftime("%d-%m-%Y-%H-%M-%S") + '.jpg',
                cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 1))



    def update(self):
        flag, frame = self.vid.get_frame()
        frame = cv2.flip(frame, 1)
        bounding_box = cv2.CascadeClassifier('/Users/kimon/opt/anaconda3/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml')
        if bounding_box.empty():
            print('File not exists!')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        num_faces = bounding_box.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)
            prediction = emotion_model.predict(cropped_img)
            
            maxindex = int(np.argmax(prediction))
            cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            show_text[0]=maxindex

        if flag:
            # cv2.flip(frame, 1)实现水平翻转，即自拍镜像
            # self.pic = ImageTk.PhotoImage(image=Image.fromarray(cv2.flip(frame, 1)))
            self.pic = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.pic, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)


App(tkinter.Tk(), "Face Expression Recognition")