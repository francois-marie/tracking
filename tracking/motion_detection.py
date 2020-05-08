import cv2
import logging
import numpy as np

def launch(source):
    """launch the motion detection

    Arguments:
        source {int or string} -- source of the input: int for webcam and string for the path of a video
    """

    countour_evolution = []
    toogle_evolution = -1

    #  create a VideoCapture object to read the frames from the input ie. our webcam video. If you want to work with another input file already saved on your PC, you can just type its path instead of the 0.
    cap=cv2.VideoCapture(source)

    # Reading our first frame
    ret1,frame1= cap.read()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (25, 25), 0)
    cv2.imshow('window',frame1)

    # reading other frames
    while(True):
        ret2,frame2=cap.read()
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
        # comparing frames
        deltaframe=cv2.absdiff(gray1,gray2)
        cv2.imshow('delta',deltaframe)
        threshold = cv2.threshold(deltaframe, 25, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
        threshold = cv2.dilate(threshold,None)
        cv2.imshow('threshold',threshold)

        # Detecting contours
        countour,heirarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    # returns two variables, contour and hierarchy, and the parameters passed to it are the threshold variable, retrieval method and approximation method.
        countour_frame = []
        for i in countour:

            # loop through the contour numpy array and draw a rectangle around the moving object
            if cv2.contourArea(i) < 50:
                continue

            (x, y, w, h) = cv2.boundingRect(i)
            countour_frame.append([x, y, w, h])
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if (toogle_evolution == 1):

            print("#"*10 )
            print(countour_frame)
            countour_evolution.append(countour_frame)
        cv2.imshow('window',frame2)

        if cv2.waitKey(20) == ord('s'):
            toogle_evolution = - toogle_evolution
        # waits for the user to enter a certain character, for instance ‘q’, to break out of the loop and quit all the windows
        if cv2.waitKey(20) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return(countour_evolution)




if __name__ == "__main__":
    countour_evolution = launch(1)
    print(countour_evolution)