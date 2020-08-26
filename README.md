## 组成

1. **训练模型**
2. **实时识别视频中人脸表情**

## 数据集

Kaggle数据集：[FER-2013](https://www.kaggle.com/msambare/fer2013)

大小为53.89MB，包括7种表情

训练集数量：28709

测试集数量：7178

50轮训练后准确率：约86%

## GUI

使用Tkinter进行GUI实现，[`camera.py`](camera.py)实现了在Tkinter中实时显示摄像头的功能，[`gui.py`](gui.py)在此基础上加上了人脸检测（openCV）和表情检测（数据集上训练所得模型）

## 使用说明

更改[`gui.py`](gui.py)中的77行参数，将`/Users/kimon/opt/anaconda3/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml`更改为opencv-python库在系统中实际的路径，之后直接运行[`gui.py`](gui.py)即可