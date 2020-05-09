import numpy as np
import cv2
from tracking.personnal import path_to_cascade, path_to_data


cascades = {
    "face": {
        "name": "haarcascade_frontalface_alt",
        "color": (255,0,0),
        "positions": [],
        "detect_properties": ()
    },
    "lowerbody": {
        "name": "haarcascade_lowerbody",
        "color": (0,255,0),
        "positions": [],
        "detect_properties": ()
    },
    "upperbody": {
        "name": "haarcascade_upperbody",
        "color": (0,0,255),
        "positions": [],
        "detect_properties": ()
    },
    "fullbody": {
        "name": "haarcascade_fullbody",
        "color": (255,255,0),
        "positions": [],
        "detect_properties": ()
    },
}

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




def get_single_feature(img, feature):
    """get the square of the position of a face on an image

    Arguments:
        img {str} -- path to the image
        feature {str} -- name of the feature
    """
    if (feature=="face"):
        cascade = cv2.CascadeClassifier(path_to_cascade+'haarcascade_frontalface_alt.xml')
    elif (feature=="eye"):
        cascade = cv2.CascadeClassifier(path_to_cascade+'haarcascade_eye.xml')
    elif (feature=="upperbody"):
        cascade = cv2.CascadeClassifier(path_to_cascade+'haarcascade_upperbody.xml')
    elif (feature=="fullbody"):
        cascade = cv2.CascadeClassifier(path_to_cascade+'haarcascade_fullbody.xml')
    else:
        print("Not a covered feature")
        return()


    img = cv2.imread(path_to_data+img)
    cv2.imshow('img',img)
    print(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # features = cascade.detectMultiScale(gray, 1.3, 5)
    features = cascade.detectMultiScale(gray, 1.1, 1)


    for (x,y,w,h) in features:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return([(x,y,w,h) for (x,y,w,h) in features])

def which_feature(source):
    if (type(source) == int or type(source) == str):
        img = cv2.imread(source)
    elif (type(source) == np.ndarray):
        img = source
    else:
        print("Wrong type for source")
        print(type(source))
        return()
    # cv2.imshow('img',img)
    print(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for feature in cascades.keys():
        cascade = cv2.CascadeClassifier(path_to_cascade+cascades[feature]["name"]+'.xml')
        features = cascade.detectMultiScale(gray, 1.1, 1)
        for (x,y,w,h) in features:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),cascades[feature]["color"],1)
            cv2.putText(
                img, #numpy array on which text is written
                feature, #text
                (x+3,y+15), #position at which writing has to start
                cv2.FONT_HERSHEY_SIMPLEX, #font family
                0.5, #font size
                cascades[feature]["color"], #font color
                1) #font stroke
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            cascades[feature]["positions"].append((x,y,w,h))
            print((x,y,w,h))
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return(cascades)

if __name__ == "__main__":

    # print(get_single_feature('../data/mot/Capture.JPG', "fullbody"))
    # print(get_single_feature('../data/fullbody.JPG', "fullbody"))

    # cascades = which_feature(path_to_data+'../data/fullbody.JPG')
    cascades = which_feature(path_to_data+'../data/mot/Capture.JPG')
    # cascades = which_feature(path_to_data+'../data/mot/train_station.webm')
    print(cascades)
