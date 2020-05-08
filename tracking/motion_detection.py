import cv2
import numpy as np

def launch_detection(source):
    """launch the motion detection

    Arguments:
        source {int or string} -- source of the input: int for webcam and string for the path of a video
    """

    countour_evolution = []
    toogle_evolution = -1

    #  create a VideoCapture object to read the frames from the input ie. our webcam video. If you want to work with another input file already saved on your PC, you can just type its path instead of the 0.
    cap=cv2.VideoCapture(source)

    # Reading our first frame
    ret1,frame1= cap.read()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (25, 25), 0)
    cv2.imshow('window',frame1)

    # reading other frames
    while(True):
        ret2,frame2=cap.read()
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
        # comparing frames
        deltaframe=cv2.absdiff(gray1,gray2)
        cv2.imshow('delta',deltaframe)
        #threshold = cv2.threshold(deltaframe, 25, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.threshold(deltaframe, 70, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold,None)
        cv2.imshow('threshold',threshold)

        # Detecting contours
        countour,heirarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    # returns two variables, contour and hierarchy, and the parameters passed to it are the threshold variable, retrieval method and approximation method.
        countour_frame = []
        for i in countour:

            # loop through the contour numpy array and draw a rectangle around the moving object
            if cv2.contourArea(i) < 50:
                continue

            (x, y, w, h) = cv2.boundingRect(i)
            countour_frame.append([x, y, w, h])
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if (toogle_evolution == 1):

            print("#"*10 )
            print(countour_frame)
            if (countour_frame != []):
                countour_evolution.append(countour_frame)
        cv2.imshow('window',frame2)

        if cv2.waitKey(20) == ord('s'):
            toogle_evolution = - toogle_evolution
        # waits for the user to enter a certain character, for instance ‘q’, to break out of the loop and quit all the windows
        if cv2.waitKey(20) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return(countour_evolution)

def countour_to_coordinate(countour):
    """from an array of countours gives the points for each time steps. each countour is a square (x, y, w, h) from which we create a point ((x+w)/2, y)

    Arguments:
        countour {list} -- array of the countoured object for each time steps
    """
    coordinates = [[(object[0]+ object[3])/2, object[1]] for object in step for step in countour]
    return(coordinates)


if __name__ == "__main__":
    # countour_evolution = launch_detection(1)
    # print(countour_evolution)

    countour_evolution = [[[340, 177, 14, 9]], [[341, 179, 12, 7]], [], [[341, 178, 12, 8]], [[341, 178, 12, 8]], [[341, 178, 12, 8]], [], [], [], [], [], [], [], [], [], [[351, 193, 12, 9]], [[351, 191, 12, 11]], [[348, 189, 16, 13]], [[348, 189, 16, 13]], [[329, 223, 19, 10], [346, 189, 21, 13]], [[329, 224, 18, 12], [346, 193, 17, 10]], [[330, 227, 16, 9], [348, 196, 11, 7]], [[323, 204, 12, 9]], [[323, 204, 12, 9]], [[337, 226, 9, 9], [323, 202, 13, 11]], [[336, 227, 10, 9], [322, 202, 14, 11]], [[322, 202, 14, 11]], [[337, 226, 9, 9], [322, 201, 14, 12]], [[337, 226, 9, 9], [322, 201, 14, 12]], [[323, 202, 13, 11]], [[336, 225, 11, 10], [322, 201, 14, 13]], [[336, 225, 11, 10], [322, 201, 14, 13]], [[338, 225, 8, 10], [324, 202, 12, 12]], [[338, 225, 8, 10], [324, 202, 12, 12]], [[338, 225, 9, 9], [323, 201, 14, 13]],
    [[337, 225, 10, 9], [323, 201, 13, 13]], [[332, 224, 13, 10], [323, 203, 12, 12]], [[327,
    222, 13, 10], [323, 206, 9, 10]], [[327, 222, 13, 10], [323, 206, 9, 10]], [[300, 252, 24, 12], [326, 219, 14, 12]], [[297, 255, 26, 15], [295, 229, 14, 12], [324, 221, 12, 10]], [[297, 258, 25, 13], [292, 230, 20, 13]], [[297, 258, 25, 13], [291, 230, 21, 14]], [[297,
    257, 25, 15], [291, 230, 21, 13]], [[297, 257, 25, 15], [291, 230, 21, 13]], [[297, 254, 26, 16], [293, 229, 16, 13]], [[300, 252, 24,
    14], [297, 230, 9, 10], [327, 221, 9, 9]], [[303, 252, 21, 11]], [], [], [[304, 252, 20, 13]], [[300, 252, 24, 17], [291, 227, 15, 15]], [[297, 255, 25, 15], [285, 227, 22, 15]], [[298, 254, 21, 14], [282, 226, 27, 17]], [[298, 254, 21, 14], [282, 226, 27, 17]], [[267,
    265, 16, 12], [300, 255, 14, 12], [282, 226,
    27, 16]], [[263, 265, 19, 13], [281, 226, 26, 16]], [[260, 265, 22, 13], [282, 226, 24, 15]], [[260, 265, 22, 13], [282, 226, 24, 15]], [[258, 263, 24, 13], [283, 225, 21, 15], [284, 176, 7, 12]], [[258, 261, 24, 12], [288, 230, 13, 9], [283, 173, 7, 16]], [[259, 261, 18, 8], [278, 211, 14, 12], [283, 170, 8, 18]], [[288, 232, 11, 9], [276, 209, 18, 13], [283, 169, 7, 20]], [[288, 232, 11, 9], [276, 209, 18, 13], [283, 169, 7, 20]], [[288, 231, 11, 11], [274, 207, 21, 14], [282, 168, 8, 22]], [[287, 231, 11, 10], [272, 206, 23, 15], [280, 168, 8, 24]], [[270, 207, 24, 14], [278, 168, 7, 27]], [[267, 262, 14, 9], [268, 206, 24, 14], [275, 169, 8, 31]], [[267, 262, 14, 9], [268, 206, 24, 14], [275, 169, 8, 31]],
    [[263, 261, 19, 12], [264, 204, 26, 16], [272, 168, 8, 32]], [[262, 260, 18, 12], [259, 203, 29, 16], [269, 166, 8, 34]], [[266, 262, 11, 8], [246, 164, 41, 62], [266, 122, 5, 17]], [[245, 161, 42, 63]], [[245, 161, 42, 63]], [[247, 241, 18, 13], [246, 157, 42, 65]], [[244, 239, 23, 13], [248, 190, 39, 29], [268,
    155, 7, 32]], [[244, 238, 24, 12], [249, 188, 36, 30], [269, 152, 7, 32]], [[245, 238, 23, 12], [250, 187, 36, 30], [270, 152, 8, 33]], [[245, 238, 23, 12], [250, 187, 36, 30], [270, 152, 8, 33]], [[246, 238, 22, 13], [251, 189, 37, 29], [271, 154, 7, 33]], [[246, 239,
    21, 13], [250, 190, 39, 28], [271, 155, 7, 34]], [[247, 240, 19, 13], [250, 156, 40, 63]], [[248, 241, 17, 12], [249, 157, 41, 63]], [[247, 241, 18, 13], [247, 192, 42, 29], [268,
    157, 8, 34]], [[247, 241, 18, 13], [247, 192, 42, 29], [268, 157, 8, 34]], [[247, 241, 19, 13], [247, 192, 42, 28], [268, 155, 7, 35]], [[245, 240, 21, 13], [247, 191, 41, 29], [268, 155, 8, 34]], [[245, 239, 22, 12], [249, 190, 39, 28], [270, 155, 7, 32]], [[246, 238,
    23, 12], [251, 189, 36, 28], [272, 153, 7, 32]]]
    # final_evol = []
    # for step in (countour_evolution):
    #     if (step != []):
    #         final_evol.append(step[0])
    # print(final_evol)

    final_evol = [[340, 177, 14, 9], [341, 179, 12, 7], [341,
    178, 12, 8], [341, 178, 12, 8], [341, 178, 12, 8], [351, 193, 12, 9], [351, 191, 12, 11],
    [348, 189, 16, 13], [348, 189, 16, 13], [329, 223, 19, 10], [329, 224, 18, 12], [330, 227, 16, 9], [323, 204, 12, 9], [323, 204, 12, 9], [337, 226, 9, 9], [336, 227, 10, 9], [322,
    202, 14, 11], [337, 226, 9, 9], [337, 226, 9, 9], [323, 202, 13, 11], [336, 225, 11, 10],
    [336, 225, 11, 10], [338, 225, 8, 10], [338,
    225, 8, 10], [338, 225, 9, 9], [337, 225, 10, 9], [332, 224, 13, 10], [327, 222, 13, 10],
    [327, 222, 13, 10], [300, 252, 24, 12], [297, 255, 26, 15], [297, 258, 25, 13], [297, 258, 25, 13], [297, 257, 25, 15], [297, 257, 25,
    15], [297, 254, 26, 16], [300, 252, 24, 14],
    [303, 252, 21, 11], [304, 252, 20, 13], [300, 252, 24, 17], [297, 255, 25, 15], [298, 254, 21, 14], [298, 254, 21, 14], [267, 265, 16,
    12], [263, 265, 19, 13], [260, 265, 22, 13],
    [260, 265, 22, 13], [258, 263, 24, 13], [258, 261, 24, 12], [259, 261, 18, 8], [288, 232,
    11, 9], [288, 232, 11, 9], [288, 231, 11, 11], [287, 231, 11, 10], [270, 207, 24, 14], [267, 262, 14, 9], [267, 262, 14, 9], [263, 261, 19, 12], [262, 260, 18, 12], [266, 262, 11,
    8], [245, 161, 42, 63], [245, 161, 42, 63], [247, 241, 18, 13], [244, 239, 23, 13], [244,
    238, 24, 12], [245, 238, 23, 12], [245, 238,
    23, 12], [246, 238, 22, 13], [246, 239, 21, 13], [247, 240, 19, 13], [248, 241, 17, 12], [247, 241, 18, 13], [247, 241, 18, 13], [247,
    241, 19, 13], [245, 240, 21, 13], [245, 239,
    22, 12], [246, 238, 23, 12]]

    import matplotlib.pyplot as plt
    import numpy


    evol_coordinates = [[(position[0]+ position[3])/2, position[1]] for position in final_evol]

    print(evol_coordinates)

