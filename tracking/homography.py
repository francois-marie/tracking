
import numpy as np
import matplotlib.pyplot as plt
import cv2   # import the OpenCV library
from utils import *

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


if __name__ == "__main__":

    # provide points from camera
    pts_camera = np.array([[154, 174], [702, 349], [702, 572],[1, 572], [1, 191]])
    # corresponding points from 2D plan (i.e. (154, 174) matches (212, 80))
    pts_2D_plan = np.array([[212, 80],[489, 80],[505, 180],[367, 235], [144,153]])

    # calculate matrix H
    h = get_homograpy(pts_camera, pts_2D_plan)

    # provide a point you wish to map from image 1 to image 2
    a = np.array([[154, 174]], dtype='float32')
    a = np.array([a])

    # finally, get the mapping
    pointsOut = cv2.perspectiveTransform(a, h)
    plot_maps(pts_2D_plan, pts_camera)