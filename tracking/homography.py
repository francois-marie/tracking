
import numpy as np
import matplotlib.pyplot as plt
import cv2   # import the OpenCV library
from tracking.utils import *

from tracking.personnal import path_to_data, path_to_image

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
    cap = cv2.VideoCapture(source)

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

def calibration_image(file_name, coordinates):
    """calibrate a source image

    Arguments:
        file_name {int} -- image index
        coordiantes {list} -- list of coordinates for homography to plot
    """
    prefix_length = 6 - len(str(file_name))
    source = path_to_image + str(0)*prefix_length + str(file_name) +'.jpg'
    print(source)
    img = cv2.imread(source, 3000)
    cv2.namedWindow("img")
    def left_click(event, x, y, flags, params):
        if (event == cv2.EVENT_LBUTTONDOWN):
            coordinates.append((x, y))
            print((x, y))
        return()
    cv2.setMouseCallback("img", left_click)
    while True:
        for center_position in coordinates:
            cv2.circle(img, center_position, 3, (0, 0, 255), -1)
        cv2.imshow("img", img)
        key = cv2.waitKey(1)
        if cv2.waitKey(20) == ord('e'):
            # pour 'enregistrer'
            file_name += 50
            prefix_length = 6 - len(str(file_name))
            source = path_to_image + str(0)*prefix_length + str(file_name) +'.jpg'
            img = cv2.imread(source)
            break
        elif (key == ord("d")):
            print(file_name)
            coordinates = []
    cv2.destroyAllWindows()
    return(coordinates)

if __name__ == "__main__":

    # source=1

    coordinates = [(78, 429)]
    new_coordinates = calibration_image(1680, coordinates)


    # video
    source = path_to_data + "mot\\train_station.webm"
    # calibration(source)






