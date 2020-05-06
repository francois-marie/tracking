# import the required packages
# from scipy import stats, integrate
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from homography import get_homograpy

def generate_gaussian_points(n=10, scale=3):
    """Generating n points with a gaussian distribution

    Arguments:
        n {int} -- number of points
    """
    return (np.random.normal(scale=scale, size=n), np.random.normal(scale=scale, size=n))

def generate_heat_map(x, y):
    """generating heat map from points in 2D space

    Arguments:
        x {np.array} -- array for the x-axis
        y {np.array} -- array for the y-axis
    """

    # call the kernel density estimator function
    ax = sns.kdeplot(x, y, cmap="Blues", shade=True, shade_lowest=False)
    # the function has additional parameters you can play around with to fine-tune your heatmap, e.g.:
    #ax = sns.kdeplot(x, y, kernel="gau", bw = 25, cmap="Reds", n_levels = 50, shade=True, shade_lowest=False, gridsize=100)

    # plot your KDE
    ax.set_frame_on(False)
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.axis('off')
    plt.show()

    # save your KDE to disk
    fig = ax.get_figure()
    fig.savefig('kde.png', transparent=True, bbox_inches='tight', pad_inches=0)
    return()




if __name__ == "__main__":

    # load the coordinates file
    x, y = generate_gaussian_points(n=100)
    generate_heat_map(x, y)

    # generating the heat map of a homography
    # provide points from camera
    pts_camera = np.array([[154, 174], [702, 349], [702, 572],[1, 572], [1, 191]])
    # corresponding points from 2D plan (i.e. (154, 174) matches (212, 80))
    pts_2D_plan = np.array([[212, 80],[489, 80],[505, 180],[367, 235], [144,153]])

    # calculate matrix H
    h = get_homograpy(pts_camera, pts_2D_plan)

    # to get a mapping from a point on the camera to a point on the 2D plan
    # provide a point you wish to map from image 1 to image 2
    a = np.array([[154, 174]], dtype='float32')
    a = np.array([a])
    # finally, get the mapping
    pointsOut = cv2.perspectiveTransform(a, h)


    plt.plot(pts_camera, '+')
    plt.plot(pts_camera, '+')
    plt.show()