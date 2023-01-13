import cvzone
import mediapipe
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
# we use cvzone,bcoz it autimatically draw detection pattern while in mediapipe, you have to do.



# Importing Image:
BackImg = cv2.imread(r"Resources/backgroundImage.png")
# BackImg = cv2.imread("Resources\\backgroundImage.png")
ballImg= cv2.imread(r"Resources/ball.png",cv2.IMREAD_UNCHANGED)
# cv2.IMREAD_UNCHANGED: maintains the transparency.
rect2 = cv2.imread(r"Resources/rectangl2.png", cv2.IMREAD_UNCHANGED)
rect1 = cv2.imread(r"Resources/rectangle1.png", cv2.IMREAD_UNCHANGED)
BackgroundImage= cv2.resize(BackImg,(1280,720))
rect1= cv2.resize(rect1,(37,156))
rect2= cv2.resize(rect2,(37,156))


cap= cv2.VideoCapture(0)
# most camera has 640X480 resolution. but here we want more resolution to play game.
cap.set(3,1280)
cap.set(4,720)
# set(): This method takes in two arguments: the property identifier and the value that you want to set for that property. The property identifier is an integer value that specifies the property that you want to set.

# hand detection:
detector= HandDetector(detectionCon=0.8,maxHands=2)

# variables:
ballposition=[100,100]
speed_x=16
speed_y=16
gameover=False
score=0

while True:
      success,img= cap.read()
      image=cv2.flip(img,1) #flip the image vertically.

      hands,img= detector.findHands(image,flipType=False)
      # flipType: when you filp the image then also it showing right hand as the left hand. So when we make flipType= False, it will resolve the issue. Basically , we are telling the cvzone that don't flip the image.
      # If you pass draw=False,then the patterns drawn on hands dissapear.


      img=cv2.addWeighted(image,0.3,BackgroundImage,0.7,0.0)
      # allows you to combine two images using a weighted sum.
      # it takes 5 arguments: first image source,alpha,second image source,beta(1-alpha),gamma.
      # Both images should have same size and type otherwise you will get error.
      

      # check hand: we will check for the type of hands and acc. to that we will put our rectangles
      
      # Displaying High Score:
      with open("HighScore.txt","r") as scoreFile:
            highScore= scoreFile.read()
            cv2.putText(img, "HS: "+highScore, (60, 70),cv2.FONT_HERSHEY_COMPLEX, 2, (16, 246, 0), 5)
            scoreFile.close()
      if score>int(highScore):
            with open("HighScore.txt","w") as scoreFile:
                  scoreFile.write(str(score))
                  scoreFile.close()
      cv2.putText(img, "Score: "+str(score), (245, 70),cv2.FONT_HERSHEY_COMPLEX, 2, (20, 0, 255), 4)

      if hands:
            for hand in hands:
                  x,y,w,h=hand['bbox'] #bbox" bounding box,it is a dictionary type and bbox is the key name.Similarly you have lmlist.
                  h1,w1,_= rect1.shape #it will return h,w,channel. here, we do not need channel.

                  # now, we have to set that our finger to the center of rectangle,i.e. rectangle moves wrt to the position of center.
                  y1= y-h1//2 #give the centre position of y1
                  y1= np.clip(y1,20,415)
                  # we want clip y1 and then provide min. and max. value.++
                  # we are clipping it bcoz if we go above the camera then it raises error that it cannot draw image and after it in bottom,hand detection is not proper.

                  if hand['type']=="Left":
                        # If hands is left then we put the rectangle on the left side.
                        img=cvzone.overlayPNG(img,rect1,(36,y1))
                        # This image have to move in y- axis so for that we have to give the y value of hbad movement. similar for right hand also.

                        # Now,rectangle will hit ball only if hand is present:
                        if 45<ballposition[0]<45+w1 and y1< ballposition[1]<y1+h1:
                              speed_x= -speed_x
                              # Giving this bcoz we want to give the illusion of hitting the ball:
                              ballposition[0]+=25 # addding 25 to it bcoz after hittig left, it should move to right
                              score+=1

                  if hand['type']=="Right":
                        # If hands is left then we put the rectangle on the left side.
                        img=cvzone.overlayPNG(img,rect2,(1233,y1))
                        if 1160 < ballposition[0] < 1160+w1 and y1 < ballposition[1] < y1+h1:
                              speed_x = -speed_x
                              ballposition[0]-=25 # we are subtracting it bcoz after hitting right ,it should move to left
                              score+=1

      if ballposition[0]<30 or ballposition[0]>1170:
            gameover=True
      if gameover:
            cv2.putText(img,"Game Over!!",(500,250),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,4,(255,0,0),3)
            cv2.putText(img, "Score:"+str(score), (550, 700),cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 5)
      else:
            if ballposition[1]>=484 or ballposition[1]<=4: #checking whther it hits bottom or top.
                  speed_y=-speed_y
            ballposition[0]+=speed_x
            ballposition[1]+=speed_y
            # putting ball: Usually its difficult to overlap images in opencv,but in cvzone we can do it easily:
            img=cvzone.overlayPNG(img,ballImg,ballposition)


      img= cv2.line(img,(0,550),(1280,550),(255,0,0),7)
      cv2.imshow("Image",img)
      if cv2.waitKey(1)== ord('q'):
            break
      
cv2.destroyAllWindows()
cap.release()


# You have to add that when ball collides with rectangle, you have icrease the speed slighlty of the ball.
# increase spped with time
# roll the ball
# save the high score and display it.

