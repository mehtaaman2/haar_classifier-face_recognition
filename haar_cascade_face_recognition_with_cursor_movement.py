import cv2
import win32api
from win32api import GetSystemMetrics
import win32gui

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

#Get system resolution
systemWidth = GetSystemMetrics(0)
systemHeight = GetSystemMetrics(1)

#Get Camera Window Metrics
windowWidth = frame.shape[1]
windowHeight = frame.shape[0]

print systemWidth,"*",systemHeight
print windowWidth,"*",windowHeight  

while rval:
    rval, frame = vc.read()
    key = cv2.waitKey(60); #Video Frame rate
    
    #Apply face and eye cascade
    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
    grayScaleImage = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayScaleImage, 1.3, 5)
    print faces
    if len(faces) == 0 :
        print "no faces detected"
    else:
        #face's approximate midpoint
        x = (faces[0][0]*2 + faces[0][2])/2.0 
        y = (faces[0][1]*2 + faces[0][3])/2.0
        #Scale the windows width to the screen width and maintain direction 
        #of face movement as the cameras's feed is laterally inverted 
        curX = systemWidth - int((x/windowWidth)*systemWidth)
        curY = int((y/windowHeight)*systemHeight)
        print x ,"  : " , y
        print curX ,"  : " , curY
        #Set cussor position
        win32api.SetCursorPos((curX,curY))
    #Displaying detected face and eye rectangles in the frame
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = grayScaleImage[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow("preview", frame)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()