import copy
from tracking.homography import get_homograpy
import numpy as np

num_list = []

with open('gt.txt', 'r') as fh:
    num_list = [line.split(',') for line in fh]


for line_index in range (len(num_list)):
    num_list[line_index] = num_list[line_index][:6]

for line_index in range (len(num_list)):
    for item in range (len(num_list[line_index])):
        num_list[line_index][item] = int(num_list[line_index][item])

print(type(num_list[0]))
print(num_list[0])

point = {
            "r_id": 1,
            "x": 0.1,
            "y": 2.1,
            "t": 0,
            "t_id": 1,
            "r_type": "camera",
            "v_x": 0.1,
            "v_y": 0.1,
            "md": {
                "exit": 0,
                "sensor":{
                    "accuracy":""
                }
            }
        }

results = {
    "t0":0,
    "tf":111280,
    "dt":40,
    "points": []
}

record_unique = 1
for line in num_list:
    new_point = copy.deepcopy(point)
    new_point["r_id"] = record_unique
    new_point["x"] = line[2]+line[4]/2
    new_point["y"] = line[3] + line[5]
    new_point["t"] = line[0]
    new_point["t_id"] = line[1]

    results["points"].append(new_point)
    record_unique += 1




# exit

for record in results["points"]:
    if (record["x"] > 1860 or record["y"] >1050):
        record["md"]["exit"] = 1

#print(results)
import json
with open('results_poc_before_homography.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

# perform several homography depending on time

# time stamps:
timestamps = [1, 25, 50, 75, 100, 200, 400, 800, 1200, 1600, 2000, 2400, 2700]


# TODO: multiply the points by two
images_coordinates = [[
                    [39, 161],
                    [120, 91],
                    [371, 98],
                    [401, 172]
                ],
                [
                    [83, 321],
                    [246, 176],
                    [746, 192],
                    [808, 341],
                ],
                [
                    [91, 315],
                    [247, 176],
                    [748, 189],
                    [812, 342],
                ],
                [
                    [82, 332],
                    [248, 188],
                    [748, 204],
                    [811, 354],
                ],
                [
                    [84, 348],
                    [252, 200],
                    [746, 219],
                    [809, 369],
                ],
                [
                    [81, 353],
                    [241, 212],
                    [741, 226],
                    [805, 375],
                ],
                [
                    [105, 381],
                    [256, 245],
                    [757, 252],
                    [820, 400],
                ],
                [
                    [109, 421],
                    [268, 273],
                    [768, 275],
                    [835, 423],
                ],
                [
                    [100, 441],
                    [262, 292],
                    [760, 296],
                    [827, 445],
                ],
                [
                    [87, 432],
                    [246, 283],
                    [747, 291],
                    [814, 441],
                ],
                [
                    [86, 433],
                    [253, 289],
                    [754, 292],
                    [820, 442],
                ],
                [
                    [78, 427],
                    [238, 279],
                    [737, 280],
                    [804, 427],
                ],
                [
                    [83, 435],
                    [241, 288],
                    [738, 287],
                    [806, 436],
                ]
                ]

# multiply by two each coordinates
# ex point_camera = np.array([[78, 322], [240, 182], [742, 196], [802, 344]])


for i in range (len(images_coordinates)):
    images_coordinates[i] = [[2*term for term in coord] for coord in images_coordinates[i]]


h = [get_homograpy(np.array(points_2D_plane), points_2D_plane) for points_2D_plane in images_coordinates]


def find_appropriate_homography(h, record):
    if record["t"]>=0 and record["t"]<25:
        homography = h[0]
    elif record["t"]>=25 and record["t"]<50:
        homography = h[0]
    elif record["t"]>=50 and record["t"]<75:
        homography = h[0]
    elif record["t"]>=75 and record["t"]<100:
        homography = h[0]
    elif record["t"]>=100 and record["t"]<200:
        homography = h[0]
    elif record["t"]>=200 and record["t"]<400:
        homography = h[0]
    elif record["t"]>=400 and record["t"]<800:
        homography = h[0]
    elif record["t"]>=800 and record["t"]<1200:
        homography = h[0]
    elif record["t"]>=1200 and record["t"]<1600:
        homography = h[0]
    elif record["t"]>=1600 and record["t"]<2000:
        homography = h[0]
    elif record["t"]>=2000 and record["t"]<2400:
        homography = h[0]
    elif record["t"]>=2400 and record["t"]<2700:
        homography = h[0]
    elif record["t"]>=2700:
        homography = h[0]
    else:
        print("error")
        return()
    return()

# change x and y for all records with homography

import cv2
for record in results["points"]:
    homography = find_appropriate_homography(h, record)
    point_before = np.array([[record["x"], record["y"]]], dtype='float32')
    point_before = np.array([point_before])

    # finally, get the mapping
    pointsOut = cv2.perspectiveTransform(point_before, homography)
    record["x"] = float(pointsOut[0][0][0])
    record["y"] = float(pointsOut[0][0][1])


with open('results_poc_after_homography.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)