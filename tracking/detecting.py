import numpy as np
import cv2
from personnal import path_to_cascade

def get_face(img):
    """get the square of the position of a face on an image

    Arguments:
        img {str} -- path to the image
    """
    face_cascade = cv2.CascadeClassifier(path_to_cascade+'haarcascade_frontalface_alt.xml')
    eye_cascade = cv2.CascadeClassifier(path_to_cascade+'haarcascade_eye.xml')
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)


    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return([(x,y,w,h) for (x,y,w,h) in faces])



if __name__ == "__main__":

    print(get_face('face.jpg'))

    face_cascade = cv2.CascadeClassifier(path_to_cascade+'haarcascade_frontalface_alt.xml')
    eye_cascade = cv2.CascadeClassifier(path_to_cascade+'haarcascade_eye.xml')
    full_body_cascade = cv2.CascadeClassifier(path_to_cascade+'haarcascade_fullbody.xml')
    upper_body_cascade = cv2.CascadeClassifier(path_to_cascade+'haarcascade_upperbody.xml')

    # TODO works fine with face detection
    img = cv2.imread('full.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = full_body_cascade.detectMultiScale(gray, 1.3, 5)
    upper_bodies = upper_body_cascade.detectMultiScale(gray, 1.3, 5)


    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()