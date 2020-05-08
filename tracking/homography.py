
import numpy as np
import matplotlib.pyplot as plt
import cv2   # import the OpenCV library
from tracking.utils import *

def get_homograpy(pts_camera, pts_2D_plan):
    """get the transformation which maps the camera shots to 2D plan.
    At least four such points pairs and you can then get an estimate

    Arguments:
        pts_camera {np.array} -- numpy array of the camera points
        pts_2D_plan {np.array} -- numpy array of the points on the 2D plan
    """

    # calculate matrix H
    h, status = cv2.findHomography(pts_camera, pts_2D_plan)
    return(h)

def plot_maps(pts_2D_plan, pts_camera):
    """plot of the points in the 2D plan and from the camera

    Arguments:
        pts_2D_plan {np.array} -- array of points from the 2D plan
        pts_camera {np.array} -- array of points from the camera
    """
    # Create two subplots and unpack the output array immediately
    #plt.figure()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
    x_cam, y_cam = points_to_coordinates(pts_camera)
    ax1.plot(x_cam, y_cam, '+')
    ax1.set_title('Points from camera')
    # ax1.set_xlim(-10, 10)
    x_plan, y_plan = points_to_coordinates(pts_2D_plan)
    ax2.plot(x_plan, y_plan, '+')
    ax2.set_title('Corresponding points on 2D plan')
    # ax2.set_xlim(-10, 10)

    plt.show()
    return()


def calibration(source):
    """calibrate a source channel

    Arguments:
        source {int or str} -- int for camera channel str for video
    """
    cap = cv2.VideoCapture(1)

    cv2.namedWindow("Frame")

    def left_click(event, x, y, flags, params):
        if (event == cv2.EVENT_LBUTTONDOWN):
            coordinates.append((x, y))
            print((x, y))
        return()

    cv2.setMouseCallback("Frame", left_click)

    coordinates= []

    while True:
        _, frame = cap.read()

        for center_position in coordinates:
            cv2.circle(frame, center_position, 3, (0, 0, 255), -1)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if cv2.waitKey(20) == ord('e'):
            # pour 'enregistrer'
            break
        elif (key == ord("d")):
            coordinates = []

    cap.release()
    cv2.destroyAllWindows()

    return(coordinates)


def display_homographied_plan(h, source):
    """displays the homographied version of the frame of the camera

    Arguments:
        h {homography} -- homography obtained after calibration
        source {int or str} -- source of the channel: int for camera and str for video path
    """
    # TODO

    cap=cv2.VideoCapture(source)
    # Reading our first frame
    ret1,frame1= cap.read()
    cv2.imshow('window',frame1)

    frame2 = cv2.perspectiveTransform(frame1, h)
    cv2.imshow('homography',frame2)


    while True:
        if cv2.waitKey(20) == ord('q'):
            # pour 'quitter'
            break

    cap.release()
    cv2.destroyAllWindows()
    return()

if __name__ == "__main__":

    source=1

    # coordinates = calibration(source)
    coordinates = [(265, 245), (352, 243), (270, 349), (375, 344)]
    # change format
    coordinates = np.asarray([ list(coordinates[i]) for i in range (len(coordinates))])

    pts_2D_plan = np.array([[1, 1], [1, 7], [4, 7], [4, 1]])

    h = get_homograpy(coordinates, pts_2D_plan)



    # provide a point you wish to map from image 1 to image 2
    a = np.array([[154, 174]], dtype='float32')
    a = np.array([a])

    # finally, get the mapping
    pointsOut = cv2.perspectiveTransform(a, h)




