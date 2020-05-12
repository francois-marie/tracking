import numpy as np
import cv2

from tracking.homography import get_homograpy, plot_maps

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

def test_homography_square(pts_camera, pts_2D, pt_test):
    """verify if applying an homography  and its inverse gives identity

    Arguments:
        pts_camera {np.array} -- array of coordinates taken from the camera shot
        pts_2D {np.Array} -- array of coordinates of corresponding points
        pt_test {np.array} -- test point
    """
    h = get_homograpy(pts_camera, pts_2D)
    h_back = get_homograpy(pts_2D, pts_camera)
    pointsInterm = cv2.perspectiveTransform(pt_test, h)
    pointsOut = cv2.perspectiveTransform(pointsInterm, h_back)
    print("check test homography: ")
    print(pt_test == pointsOut)
    return(pointsOut)

def test_coordinates(pts_camera, pts_2D):
    """test if the homography applied on the coordinate points of the camera give the pts 2D

    Arguments:
        pts_camera {np.array} -- array of coordinates taken from the camera shot
        pts_2D {np.Array} -- array of coordinates of corresponding points
    """

    h = get_homograpy(pts_camera, pts_2D)
    for i in range (len(pts_camera)):
        print(cv2.perspectiveTransform(pts_camera[i], h) == pts_2D[i])


if __name__ == "__main__":
    point_camera = np.array([[39, 161],
                    [120, 91],
                    [371, 98],
                    [401, 172]])

    pts_2D = np.array([[0, 11],
                    [0, 0],
                    [10, 0],
                    [10, 11]])
    pt_test = np.array([[154, 174]], dtype='float32')
    pt_test = np.array([pt_test])

    point_out = test_homography_square(point_camera, pts_2D, pt_test)

    h = get_homograpy(point_camera, point_camera)
    print(h)