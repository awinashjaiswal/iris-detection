import numpy as np
import cv2
face_cascade = cv2.CascadeClassifier('xmlfile/haarcascade_frontalface_alt.xml')
camera=cv2.VideoCapture(0)
numerator=0
denominator=0
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
		
		#------------ estimation of distance of the human from camera--------------#
		d=10920.0/float(w)

		#-------- coordinates of interest --------------# 
		x1=int(x+w/4.2)+1 		#-- +1 is done to hide the green color
		x2=int(x+w/2.5)
		y1=int(y+h/3)+1
		y2=int(y+h/2.2)
		roi=frame[y1:y2,x1:x2]
		gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
		equ = cv2.equalizeHist(gray)
		thres=cv2.inRange(equ,0,20)
		kernel = np.ones((3,3),np.uint8)
		#/------- removing small noise inside the white image ---------/#
		dilation = cv2.dilate(thres,kernel,iterations = 2)
		#/------- decreasing the size of the white region -------------/#
		erosion = cv2.erode(dilation,kernel,iterations = 3)
		#/-------- finding the contours -------------------------------/#
		image, contours, hierarchy = cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
		#--------- checking for 2 contours found or not ----------------#
		if len(contours)==2 :
			numerator+=1
			#img = cv2.drawContours(roi, contours, 1, (0,255,0), 3)
			#------ finding the centroid of the contour ----------------#
			M = cv2.moments(contours[1])
			#print M['m00']
			#print M['m10']
			#print M['m01']
			if M['m00']!=0:
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				cv2.line(roi,(cx,cy),(cx,cy),(0,0,255),3)
			#print cx,cy
		#-------- checking for one countor presence --------------------#
		elif len(contours)==1:
			numerator+=1
			#img = cv2.drawContours(roi, contours, 0, (0,255,0), 3)

			#------- finding centroid of the countor ----#
			M = cv2.moments(contours[0])
			if M['m00']!=0:
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				#print cx,cy
				cv2.line(roi,(cx,cy),(cx,cy),(0,0,255),3)
		else:
			denominator+=1
			#print "iris not detected"
		ran=x2-x1
		mid=ran/2
		if cx<mid:
			print "looking left"
		elif cx>mid:
			print "looking right"
			
	cv2.imshow("frame",frame)
	#cv2.imshow("eye",image)
	if cv2.waitKey(30)==27 & 0xff:
		break
camera.release()
print "accurracy=",(float(numerator)/float(numerator+denominator))*100
cv2.destroyAllWindows()
