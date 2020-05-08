import numpy as np
import cv2
from tracking.motion_detection import launch_detection, countour_to_coordinate
from tracking.homography import calibration, get_homograpy
import tracking.heat_map

# file to be run to execute the different libs


if __name__ == "__main__":

    source = 1      # channel for the camera

    ###########
    # CALIBRATION
    ###########
    # coordinates = calibration(source)
    coordinates = [(265, 245), (352, 243), (270, 349), (375, 344)]
    # change format
    coordinates = np.asarray([ list(coordinates[i]) for i in range (len(coordinates))])

    pts_2D_plan = np.array([[1, 1], [4, 1], [1, 7], [4, 7]])    # corresponding points in 2D plane


    ############
    # HOMOGRAPHY
    ############
    h = get_homograpy(coordinates, pts_2D_plan)

    ###########
    # MOTION DETECTION
    ###########

    # countour_evolution = launch_detection(1)
    # object_camera_coordinates = countour_to_coordinate(countour_evolution)
    object_camera_coordinates = [[174.5, 177], [174.0, 179], [174.5, 178], [174.5, 178], [174.5, 178], [180.0, 193], [181.0, 191], [180.5, 189], [180.5, 189], [169.5,
    223], [170.5, 224], [169.5, 227], [166.0, 204], [166.0, 204], [173.0, 226], [172.5, 227],
    [166.5, 202], [173.0, 226], [173.0, 226], [167.0, 202], [173.0, 225], [173.0, 225], [174.0, 225], [174.0, 225], [173.5, 225], [173.0, 225], [171.0, 224], [168.5, 222], [168.5, 222], [156.0, 252], [156.0, 255], [155.0, 258], [155.0, 258], [156.0, 257], [156.0, 257], [156.5, 254], [157.0, 252], [157.0, 252], [158.5, 252], [158.5, 252], [156.0, 255], [156.0, 254], [156.0, 254], [139.5, 265], [138.0, 265], [136.5, 265], [136.5, 265], [135.5, 263], [135.0, 261], [133.5, 261], [148.5, 232], [148.5, 232], [149.5, 231], [148.5, 231], [142.0,
    207], [138.0, 262], [138.0, 262], [137.5, 261], [137.0, 260], [137.0, 262], [154.0, 161],
    [154.0, 161], [130.0, 241], [128.5, 239], [128.0, 238], [128.5, 238], [128.5, 238], [129.5, 238], [129.5, 239], [130.0, 240], [130.0, 241], [130.0, 241], [130.0, 241], [130.0, 241], [129.0, 240], [128.5, 239], [129.0, 238]]

    ###########
    # 2D-PLAN COORDINATES
    ###########
    object_plan_coordinates = []
    for coord in object_camera_coordinates:
        # provide a point you wish to map from image 1 to image 2
        a = np.array([coord], dtype='float32')
        a = np.array([a])

        # finally, get the mapping
        object_plan_coordinates.append(list(cv2.perspectiveTransform(a, h)[0][0]))

    print(object_plan_coordinates)

