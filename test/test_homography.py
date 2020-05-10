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