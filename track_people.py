import numpy as np
import cv2
import Person
import time
import imutils
import datetime

#https://www.youtube.com/watch?v=S26G0a7u9d4


cap = cv2.VideoCapture('laiptai4.mp4') #Open video file , reik nurodyti video faila ir jo path
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True) #Create the background substractor

kernelOp = np.ones((3,3),np.uint8)
kernelOp1 = np.ones((7,7),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)

kernelCl = np.ones((11,11),np.uint8)
kernelCl1 = np.ones((20,20),np.uint8)
kernelCl2 = np.ones((25,25),np.uint8)

#Variables
font = cv2.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1
areaTH = 5000
w_margin= 50
h_margin= 50
wmax= 500


import pdb; pdb.set_trace() #debuginimo pradzia

# Atvaizdavimo kintamieji
cnt_up=0
cnt_down=0
line_down_color=(255,0,0)
line_up_color=(0,0,255)
pts_L1= np.array([[0, 320],[480, 320]])
pts_L2= np.array([[0, 400],[480, 400]])


counter=0



while(cap.isOpened()):
    ret, frame = cap.read() #read a frame

    frame = imutils.resize(frame, width=min(640, frame.shape[1]))
    
    fgmask = fgbg.apply(frame) #Use the substractor
    try:
        ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        #Opening (erode->dilate) para quitar ruido.
        mask0 =  cv2.morphologyEx(imBin ,  cv2.MORPH_OPEN, kernelOp2)
        #mask1 =  cv2.morphologyEx(imBin , cv2.MORPH_OPEN, kernelOp1)
        #mask2 =  cv2.morphologyEx(imBin,  cv2.MORPH_OPEN, kernelOp1)
        #Closing (dilate -> erode) para juntar regiones blancas.
        #mask3 =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE,  kernelCl)
        #mask4 =  cv2.morphologyEx(mask1 , cv2.MORPH_CLOSE, kernelCl1)
        mask =  cv2.morphologyEx(mask0 , cv2.MORPH_CLOSE, kernelCl2)
    except:
        #if there are no more frames to show...
        print('EOF')
        break

    maskOriginal=mask

    _, contours0, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
########jeigu conturas per didelis perpjaunu pusiau
    mask2_flag=0
    for cnt in contours0:
        area = cv2.contourArea(cnt)
        if area > areaTH:    
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)
            if w > wmax:
                mask2 = cv2.line( mask, ((x+w/2), 0), ((x+w/2),640),(0,0,0), 10)
                mask2_flag=1

    if mask2_flag==0:
        mask2=mask

    cv2.imshow('Mask su linija',mask2)
    cv2.imshow('mask to open',mask0)
    cv2.imshow('Mask pradinis tik veliau',maskOriginal)
    cv2.imshow('pradinis substraction',imBin)



    _, contours0, hierarchy = cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)        
    for cnt in contours0:
        cv2.drawContours(frame, cnt, -1, (0,255,0), 3, 8)
        area = cv2.contourArea(cnt)

            #################
            #   Tikrina ar objektas vis dar kadre, jei ne istrina    
            #################     
        for i in persons:   
            i.updateDingimas(i.getDingimas()+1) #skaiciuoja kiek kadru neatsinaujino kiekvienas objektas
            if i.getDingimas() > 25:
                persons.remove(i)
        
        if area > areaTH:
            #################
            #   Objekto sekimas    
            #################            
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)

            print('x{} y{} w{} h{}'.format( x, y, w, h))

            
            new = True                 
            for i in persons:
                if abs(x-i.getX()) <= w_margin and abs(y-i.getY()) <= h_margin:
                    new = False
                    i.updateCoords(cx,cy)  
                    i.updateDingimas(0) # nuresetina dingima
                    break
            if new == True:
                p = Person.MyPerson(pid,cx,cy, max_p_age)
                persons.append(p)
                pid += 1    
 
            cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)            
            cv2.drawContours(frame, cnt, -1, (0,255,0), 3)
            cv2.imshow('img',img)

    #########################
    # Trajektoriju atvaizdavimas  
    #########################
    for i in persons:
        if len(i.getTracks()) >= 2:
            pts = np.array(i.getTracks(), np.int32)
            pts = pts.reshape((-1,1,2))
            frame = cv2.polylines(frame,[pts],False,i.getRGB())
#        if i.getId() == 9:
#            print str(i.getX()), ',', str(i.getY())
         #################
         #   nustato ar kirto linija    #
         #################
        if i.getDir() == None:
            i.kurEina( pts_L2[0,1] ,pts_L1[0,1])   #      def kurEina(bSottom_line,top_line):
            if i.getDir() == 'up':
                cnt_up+=1
                print('Timestamp: {:%H:%M:%S} UP {}'.format(datetime.datetime.now(), cnt_up))
            elif i.getDir() == 'down':
                cnt_down+=1
                print('Timestamp: {:%H:%M:%S} DOWN {}'.format(datetime.datetime.now(), cnt_down))



        cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.7,i.getRGB(),1,cv2.LINE_AA)

    #########################
    # Atvaizdavimas  
    #########################
    str_up='UP: '+ str(cnt_up)
    str_down='DOWN: '+ str(cnt_down)
    frame = cv2.polylines( frame, [pts_L1], False, line_down_color,thickness=4)
    frame = cv2.polylines( frame, [pts_L2], False, line_up_color,thickness=4)
    cv2.putText(frame, str_up, (10,50), font,1,(0,0,255), 2,cv2.LINE_AA)
    cv2.putText(frame, str_down, (10,100), font,1,(255,0,0), 2,cv2.LINE_AA) 

    
    cv2.imshow('Frame',frame)


    #cv2.imwrite("img/frame %d.jpg" % counter, frame)
    #counter=counter+1
    
    #Abort and exit with 'Q' or ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release() #release video file
cv2.destroyAllWindows() #close all openCV windows
