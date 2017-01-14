import numpy as np
import cv2
import cv2
face_cascade = cv2.CascadeClassifier('xmlfile/haarcascade_frontalface_alt.xml')
camera=cv2.VideoCapture(0)
while True:
   	ret, frame = camera.read()
   	roi=frame
   	frame=cv2.flip(frame,1)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
		#----------- vertical mid line ------------------#
		#cv2.line(frame,(x+w/2,y),(x+w/2,y+h/2),(255,0,0),1)
		# ---------- horizontal lower line ----------------# 
		cv2.line(frame,(int(x+w/4.2),int(y+h/2.2)),(int(x+w/2.5),int(y+h/2.2)),(0,255,0),1)
		#----------- horizontal upper line ------#
		cv2.line(frame,(int(x+w/4.2),y+h/3),(int(x+w/2.5),y+h/3),(0,255,0),1)
		# ---------- vertical left line ----------#
		cv2.line(frame,(int(x+w/4.2),y+h/3),(int(x+w/4.2),int(y+h/2.2)),(0,255,0),1)
		# ---------- vertical right line---------------#
		cv2.line(frame,(int(x+w/2.5),y+h/3),(int(x+w/2.5),int(y+h/2.2)),(0,255,0),1)
		#-------- coordinates of interest --------------# 
		x1=int(x+w/4.2)+1 		#-- +1 is done to hide the green color
		x2=int(x+w/2.5)
		y1=int(y+h/3)+1
		y2=int(y+h/2.2)
		roi=frame[y1:y2,x1:x2]
		gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
		equ = cv2.equalizeHist(gray)
		thres=cv2.inRange(equ,0,20)
		kernel = np.ones((5,5),np.uint8)
		dilation = cv2.dilate(thres,kernel,iterations = 1)
		erosion = cv2.erode(dilation,kernel,iterations = 2)
		image, contours, hierarchy = cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
		if len(contours)==2 :
			img = cv2.drawContours(roi, contours, 1, (0,255,0), 3)
		elif len(contours)==1:
			img = cv2.drawContours(roi, contours, 0, (0,255,0), 3)
		else:
			print "iris not detected"
		
		#if len(contours) > 0:
        #find largest contour in mask, use to compute minEnCircle 
			
	cv2.imshow("frame",frame)
	cv2.imshow("eye",img)
	if cv2.waitKey(30)==27 & 0xff:
		break
camera.release()
cv2.destroyAllWindows()