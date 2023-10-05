import kivy
# import lovecal
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.camera import Camera
import cv2
import os
import telepot
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import numpy as np

# configPath=os.path.join("model_data","ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
# modelPath=os.path.join("model_data","frozen_inference_graph.pb")
# # modelPath=os.path.join("model_data","pspnet50+99.pth")
# classesPath=os.path.join("model_data","coco.names")
class KivyCamera(Image):
    def __init__(self, capture,modelPath,configPath,classesPath, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.configPath=configPath
        self.modelPath=modelPath
        self.classesPath=classesPath
        self.net=cv2.dnn.DetectionModel(self.modelPath,self.configPath)
        self.net.setInputSize(320,320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5,127.5,127.5))
        self.net.setInputSwapRB(True)
        self.readClasses()
        Clock.schedule_interval(self.update, 1.0 / fps)
    def readClasses(self):
        with open(self.classesPath,'r') as f:
            self.classesList=f.read().splitlines()
        self.classesList.insert(0,'__Background__')
        self.colorList=np.random.uniform(low=0,high=255,size=(len(self.classesList),3))#1

    def update(self, dt):
        ret, frame = self.capture.read()

        if ret:
            # currentTime=time.time()#6
            # fps=1/(currentTime-startTime)#6
            # startTime=currentTime
            classLabelIDs,confidences,bboxs=self.net.detect(frame,confThreshold=0.5)
            bboxs=list(bboxs)
            confidences=list(np.array(confidences).reshape(1,-1)[0])
            confidences=list(map(float,confidences))
            # bboxsIdx=cv2.dnn.NMSBoxes(bboxs,confidences,score_threshold=0.5,nms_threshold=0.2)
            bboxsIdx=cv2.dnn.NMSBoxes(bboxs,confidences,score_threshold=0.5,nms_threshold=0.8)#5

            if len(bboxsIdx)!=0:
                for i in range(0,len(bboxsIdx)):
                    bbox=bboxs[np.squeeze(bboxsIdx[i])]
                    classConfidence=confidences[np.squeeze(bboxsIdx[i])]
                    classLabelID=np.squeeze(classLabelIDs[np.squeeze(bboxsIdx[i])])
                    classLabel=self.classesList[classLabelID]
                    classColor=[int(c) for c in self.colorList[classLabelID]]#1
                    # displayText="{}:{:.4f}".format(classLabel,classConfidence)#2
                    displayText="{}:{:.2f}".format(classLabel,classConfidence)#2
                    x,y,w,h=bbox
                    x1=(x+w)/2
                    y1=(y+h)/2
                    b=(0,0)[0]<x1<(800,500)[0] and (0,0)[1]<y1<(800,500)[1]
                    if b:
                        token = "6275415240:AAF3yDdT45-VIn8GdBrQUHH0XmtMXo0MC28"
                        receiver_id=5877612764
                        bot = telepot.Bot(token)
                        a=cv2.imwrite("a.jpg",frame)
                        bot.sendPhoto(receiver_id,photo=open("a.jpg", "rb"),caption="Có xâm nhập, nguy hiêm!")
                    cv2.rectangle(frame,(x,y),(x+w,y+h),color=classColor,thickness=1)
                    cv2.rectangle(frame,(0,0),(800,500),(0,255,0),2)
                    cv2.putText(frame,displayText,(x,y-10),cv2.FONT_HERSHEY_PLAIN,1,classColor,2)#2
                    # lineWidth=30#3
                    lineWidth=min(int(w*0.3),int(h*0.3))#4
                    cv2.line(frame,(x,y),(x+lineWidth,y),classColor,thickness=5)#3
                    cv2.line(frame,(x,y),(x,y+lineWidth),classColor,thickness=5)#3

                    cv2.line(frame,(x+w,y),(x+w-lineWidth,y),classColor,thickness=5)#3
                    cv2.line(frame,(x+w,y),(x+w,y+lineWidth),classColor,thickness=5)#3

                    cv2.line(frame,(x,y+h),(x+lineWidth,y+h),classColor,thickness=5)#3
                    cv2.line(frame,(x,y+h),(x,y+h-lineWidth),classColor,thickness=5)#3

                    cv2.line(frame,(x+w,y+h),(x+w-lineWidth,y+h),classColor,thickness=5)#3
                    cv2.line(frame,(x+w,y+h),(x+w,y+h-lineWidth),classColor,thickness=5)#3
            # cv2.putText(frame,"FPS:"+str(int(fps)),(20,70),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)#6
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

class MainApp(App):
    configPath=os.path.join("model_data","ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath=os.path.join("model_data","frozen_inference_graph.pb")
    # modelPath=os.path.join("model_data","pspnet50+99.pth")
    classesPath=os.path.join("model_data","coco.names")
    def build(self):
        self.icon = 'images/appicon.png'
        self.capture = cv2.VideoCapture("rtsp://admin:admin1234@ngduchanh2.ddns.net:554/cam/realmonitor?channel=1&subtype=0")
        # self.capture = cv2.VideoCapture("rtsp://admin:admin1234@192.168.1.15:554/cam/realmonitor?channel=1&subtype=0")
        self.camera = KivyCamera(capture=self.capture,modelPath=self.modelPath,configPath=self.configPath,classesPath=self.classesPath,fps=30)
        return self.camera

if __name__== "__main__":
    MainApp().run()
