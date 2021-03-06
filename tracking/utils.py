import numpy as np

def points_to_coordinates(points):
    """switch from an array of points used for finding homography to arrays of coordinates x, y for plotting

    Arguments:
        points {np.array} -- array containing a list of points
    """
    x = np.array([point[0] for point in points])
    y = np.array([point[1] for point in points])
    return(x, y)


def coordinates_to_points(x, y):
    """switch from arrays of coordinates x, y for plotting to an array of points used for finding homography

    Arguments:
        x {np.array} -- array of x-axis coordinates
        y {np.array} -- array of y-axis coordinates
    """
    size = int(np.shape(x)[0])
    return(np.array([[x[i], y[i]] for i in range (size)]))


if __name__ == "__main__":


    pts_camera = np.array([[154, 174], [702, 349], [702, 572],[1, 572], [1, 191]])
    x, y = np.array([154, 702, 702, 1, 1]), np.array([174, 349, 572, 572, 191])

    # points_to_coordinates
    x_res, y_res = points_to_coordinates(pts_camera)
    print("x res : ", x_res)
    print("y res : ", y_res)

    if ((x_res==x).all and (y_res==y).all):
        print("transformation points_to_coordinates OK")
    else:
        print("transformation points_to_coordinates wrong")

    # coordinates_to_points
    points_res = coordinates_to_points(x, y)
    print("points res : ", points_res)

    if ((pts_camera==points_res).all):
        print("transformation coordinates_to_points OK")
    else:
        print("transformation coordinates_to_points wrong")


def save_video(source, output_name='output.avi'):
    """save a video from a source channel

    Arguments:
        source {int or str} -- camera source or path of video
    """

    import numpy as np
    import cv2

    cap = cv2.VideoCapture(source)

    # Define the codec and create VideoWriter object
    #fourcc = cv2.cv.CV_FOURCC(*'DIVX')
    #out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
    out = cv2.VideoWriter(output_name, -1, 20.0, (640,480))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            frame = cv2.flip(frame,0)

            # write the flipped frame
            out.write(frame)

            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return()