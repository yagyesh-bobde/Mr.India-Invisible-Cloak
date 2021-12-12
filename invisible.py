import cv2
import handTrackingModule as htm
import time

cam = cv2.VideoCapture(0)

########
widthimg = 1280
heightimg = 1280
#######
cam.set(3,widthimg)
cam.set(4,heightimg)
#########
########
ctime = 0
ptime = 0
#####
detector = htm.handDetector()
########

options = ['Face', 'Hands', 'UpperB' , 'LowerB','Stop']
big_box_height = 85
hi_box = 30
hf_box = 75
box_width = 150
start_points = []
end_points =[]
point = 0
end_point = 0
for i in range(5) :
    if i == 0 :
        point = 10
        end_point = point + box_width
    else:
        point = end_points[i-1] + 20
        end_point = point + box_width

    start_points.append(point)
    end_points.append(end_point)
#########



def add_options(img , widthimg, heightimg) :
    cv2.rectangle(img,(0,0),(widthimg,big_box_height),(255,255,255) , cv2.FILLED)
    cv2.putText(img,"Make Invisible: ",(5,15),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),2)
    for i in range(len(options)) :
        if i==len(options)-1 :
            point = widthimg-160
            cv2.rectangle(img, (point, hi_box), (point+150, hf_box), (200, 200, 200), cv2.FILLED)
            cv2.putText(img, options[i], (point + 25, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 50, 250), 2)
        else:
            cv2.rectangle(img,(start_points[i],hi_box),(end_points[i],hf_box),(200,200,200),cv2.FILLED)
            cv2.putText(img,options[i],(start_points[i]+25,60),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,150,250),2)

   #cv2.rectangle(img,(start_points[1],hi_box),(end_points[1],hf_box),(200,200,200),cv2.FILLED)
    #cv2.putText(img, 'Face', (45, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 0, 0), 2)

while True:
    res, frame = cam.read()
    frame = cv2.flip(frame, 1)
    img = detector.findHands(frame)
    add_options(frame, widthimg, heightimg)
    lmslist = detector.findPosition(img)
    #print(lmslist)
    # --FpS--
    ctime = time.time()
    fps = 1 // (ctime - ptime)
    ptime = ctime
    cv2.putText(frame, str(int(fps)), (frame.shape[1] - 100, frame.shape[0] - 25), cv2.FONT_HERSHEY_TRIPLEX, 2,
                (0, 255, 0), 2)

    cv2.imshow('Hand Tracker', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

