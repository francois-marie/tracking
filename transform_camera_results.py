import json
import copy
import numpy as np
import cv2
from tracking.homography import get_homograpy, calibration_image

def export_json(data, name):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    return()

def import_json(name):
    data = json.load(open(name, 'r'))
    return(data)

def create_records_list_from_txt(name):
    num_list = []
    with open(name, 'r') as fh:
        num_list = [line.split(',') for line in fh]
    for line_index in range (len(num_list)):
        # TODO: change the removal of the suffixe to get more data
        num_list[line_index] = num_list[line_index][:6]
    for line_index in range (len(num_list)):
        for item in range (len(num_list[line_index])):
            num_list[line_index][item] = int(num_list[line_index][item])


class Point(dict):

    def init(self, r_id, x, y, t, t_id, v_x = 0, v_y = 0, r_type='camera', exit=False, accuracy=None):
        self.r_id = r_id
        self.x = x
        self.y = y
        self.t = t
        self.v_x = v_x
        self.v_y = v_y
        self.t_id = t_id
        self.r_type = r_type
        self.exit = exit
        self.accuracy = accuracy

    def get_necessary_info(self):
        result_file = {
            "r_id": self.r_id,
            "x": self.x,
            "y": self.y,
            "t": self.t,
            "t_id": self.t_id,
            "r_type": self.r_type,
            "md":{
                "exit":self.exit
            }
        }
        return(result_file)

    def get_full_info(self):
        result_file = {
            "r_id": self.r_id,
            "x": self.x,
            "y": self.y,
            "v_x": self.v_x,
            "v_y": self.v_y,
            "t": self.t,
            "t_id": self.t_id,
            "r_type": self.r_type,
            "md":{
                "exit":self.exit,
                "accuracy":self.accuracy,
            }
        }
        return(result_file)

class Result(dict):

    def init(self, t0, tf, dt, points):
        self.t0 = t0
        self.tf = tf
        self.dt = dt
        self.points = points

    def get_full_info(self):
        results = {
                    "t0":self.t0,
                    "tf":self.tf,
                    "dt":self.dt,
                    "points": self.generate_json_points()
                }
        return(results)

    def generate_json_points(self):
        result = []
        for point in self.points:
            result.append(point.get_necessary_info())
        return(result)

class ReadableData():
    homographies = []
    camera_points = []
    users = dict()
    beacons = dict()
    result = Result()


    def init(self, homographies, camera_points):
        self.homographies = homographies
        self.camera_points = camera_points
        self.build_resuls()
        return()

    def get_full_info(self):
        return(self.users, self.beacons, self.result.get_full_info())

    def get_number_of_users(self):
        nb_users = 0
        for raw_point in self.camera_point:
            if (raw_point[1] > nb_users):
                nb_users = raw_point[1]
        return(nb_users)

    def build_results(self):
        r_id = self.get_number_of_users + 1
        for raw_point in self.camera_points:
            new_point = Point(r_id,
                            raw_point[2]+raw_point[4]/2,
                            raw_point[3] + raw_point[5],
                            raw_point[0],
                            raw_point[1])
            self.result.points.append(new_point)
            r_id += 1

    def build_users(self):
        for point in self.result.points:
            if (point.t_id in self.user_dict.keys()):
                self.user_dict[point.t_id].append(point.r_id)
            else:
                self.user_dict[point.t_id] = [point.r_id]

    def get_homography_from_frame(self, file_name):
        coordinates = [(0, 0)]
        camera_coordinates = calibration_image(file_name, coordinates)[1:]
        # TODO:
        # transform type of camera coordinates from list of tuple to list of lsit of int
        # set or input the corresponding 2D points form the camera
        # compute the homography
        # store: the homography, the index of the frame

def get_point_from_json(point_json):
    point = Point(point_json["r_id"],
                point_json["x"],
                point_json["y"],
                point_json["t"],
                point_json["t_id"],
                point_json["r_type"],
                point_json["exit"])
    return(point)


def get_result_from_json(result_json):
    result = Result(result_json["t0"],
                    result_json["tf"],
                    result_json["dt"],
                    result_json["points"], )
    return(result)


#########################################
# enlever vx, vy, sensor -> facultatifs

# result_homography = import_json('results_poc_after_homography.json')

# for record in result_homography["points"]:
#     record.pop("v_x", None)
#     record.pop("v_y", None)
#     record.pop("v_x", None)
#     record["md"].pop("sensor", None)

# export_json(result_homography, 'results_poc_after_facultatifs.json')


#######################################
# temps des points ne vont pas non plus -> rajouter *40


# result_facultatif = import_json('results_poc_after_facultatifs.json')

# for record in result_facultatif["points"]:
#     record["t"] = record["t"]*40

# export_json(result_facultatif, 'results_poc_after_time.json')

#########################################
# subsampler toutes les secondes au min

# result_time = import_json('results_poc_after_time.json')

# list_to_keep = []
# for i in range (len(result_time["points"])):
#     if (result_time["points"][i]["t"] % 1000 == 0):
#         list_to_keep.append(i)

# list_of_records = []
# for i in list_to_keep:
#     list_of_records.append(result_time["points"][i])

# result_time["points"] = list_of_records


# export_json(result_time, 'results_poc_after_subsample.json')


###################################
# store float x & y on 5 digits

# result_time = import_json('results_poc_after_subsample.json')

# for i in range (len(result_time["points"])):
#     result_time["points"][i]["x"] = round(result_time["points"][i]["x"], 5)
#     result_time["points"][i]["y"] = round(result_time["points"][i]["y"], 5)


# export_json(result_time, 'results_poc_after_round.json')



####################################
# étape 1: c'est construire le dict des users


# result_round = import_json('results_poc_after_round.json')

# user_dict=dict()


# print(len(result_round["points"]))
# for i in range (len(result_round["points"])):
#     if (result_round["points"][i]["t_id"] in user_dict.keys()):
#         user_dict[result_round["points"][i]["t_id"]].append(result_round["points"][i]["r_id"])
#     else:
#         user_dict[result_round["points"][i]["t_id"]] = [result_round["points"][i]["r_id"]]

# export_json(user_dict, 'user_dict.json')


#


#########################################
# En 2 tu passes tous les points en caméra avec des t_id différents (met leur r_id au pire -> dans ce cas, prends les u_id à partir de 1000 pour éviter les collisions).


# result_round = import_json('results_poc_after_round.json')

# for i in range (len(result_round["points"])):
#     result_round["points"][i]["t_id"] = result_round["points"][i]["r_id"]

# export_json(result_round, 'results_poc_after_r_id.json')

###############################
# liste des beacons avec leur position et leur rayon

# beacon =  {"beacon" : [
#     {"x": 0,
#     "y": 11,
#     "r": 1},
#     {"x": 0,
#     "y": 0,
#     "r": 1},
#     {"x": 10,
#     "y": 0,
#     "r": 1},
#     {"x": 10,
#     "y": 11,
#     "r": 1},
#     {"x": 5,
#     "y": 5.5,
#     "r": 1}
# ]}

# export_json(beacon, 'beacon_dict.json')


#########################################
# ajouter 300 à tous les r_ids de user_dict et de results

# user_dict_300 = import_json("user_dict.json")
# for key in user_dict_300.keys():
#     for index in range (len(user_dict_300[key])):
#         user_dict_300[key][index] += 300
# export_json(user_dict_300, "user_dict_300.json")

# results = import_json('results_poc_after_r_id.json')

# for record in results["points"]:
#     record["t_id"] += 300
#     record["r_id"] += 300

# export_json(results, 'results_poc_after_300.json')

########################################
# En 3 tu enumerate sur les items du dict u_id, list_rids et en parcourant les r_ids, si (c'est le premier ou le dernier point ou si il est dans une zone autour d'un beacon), tu passes simplement son t_id à u_id


# user_dict = import_json("user_dict_300.json")
# beacon_dict = import_json("beacon_dict.json")

# result = import_json('results_poc_after_300.json')

# def inside_beacon(results, i, beacon_dict):
#     """know if a record is inside a beaon

#     Arguments:
#         results {dict} -- dict for the algo
#         i {int} -- index of record in list "points"
#         beacon_dict {dict} -- dict of referenced beacons bluetooth
#     """
#     x = results["points"][i]["x"]
#     y = results["points"][i]["y"]
#     for beacon in beacon_dict["beacon"]:
#         center_x = beacon["x"]
#         center_y = beacon["y"]
#         radius = beacon["r"]
#         if ((x - center_x)**2 + (y - center_y)**2 < radius**2):
#             return(True)
#     return(False)


# for i, (k, v) in enumerate(user_dict.items()):
#     # print(i, k, v)
#     # print("#"*10)
#     # print(k + "  "+str(v))
#     for r_id_of_u in v:
#         for i in range (len(result["points"])):
#             if (result["points"][i]["t_id"] == r_id_of_u):
#                 # print("i : ", i)
#                 if (r_id_of_u == user_dict[k][0] or r_id_of_u == user_dict[k][-1] or inside_beacon(result, i, beacon_dict)):
#                     result["points"][i]["t_id"] = int(k)
#                     result["points"][i]["r_type"] = "bluetooth"
#                     if (r_id_of_u == user_dict[k][-1]):
#                         result["points"][i]["md"]["exit"] = True


# export_json(result, 'results_poc_after_ennum.json')

# # check
# check_list = []
# for i in range (len(result["points"])):
#     if(result["points"][i]["t_id"] < 300):
#         check_list.append(i)


########################################
# change tf

#########################################
# diminuer le nombre d'utilisateurs à 50

# load data
# user_dict = import_json("user_dict_300.json")


# new_user_dict = dict()
# for i in range (1, 51):
#     i = i+195
#     new_user_dict[str(i)] = user_dict[str(i)]
# export_json(new_user_dict, '50_user_dict.json')

# result = import_json('results_poc_after_ennum.json')
# user_dict = import_json("50_user_dict.json")

# new_result_dict = copy.deepcopy(result)
# new_result_dict["points"] = []

# for record in result["points"]:
#     r_id = record["r_id"]
#     for user in user_dict.keys():
#         if (r_id in user_dict[user]):
#             new_result_dict["points"].append(record)

# export_json(new_result_dict, 'results_poc_50_users.json')

###########################################
# enlever les records tels que y > y_seuil = 18
# result = import_json('results_poc_50_users.json')
# new_result = copy.deepcopy(result)
# new_result["points"] = []
# print(new_result)
# y_seuil = 18
# for record in result["points"]:
#     if (record["y"] < y_seuil):
#         new_result["points"].append(record)


# export_json(new_result, 'results_poc_y_seuil.json')


#####################################
#  filtre les murs et caddies
# murs: 242, 194, 190,
# 178, 176, 175 , 171
# velo: 288
# TO REMOVE:
# décor: 163, 164, 165, 166, 188, 190, 191, 192, 193, 194, 195, 240, 241, 242, 296
# netoyage & caddies: 169, 57, 157, 167, 170, 181, 288

# def remove_user(user_dict, result_dict, user_id):
#     """remove a user from the dict of users and from the list of records

#     Arguments:
#         user_dict {dict} -- dict of user
#         result_dict {dict} -- data for the algo
#         user_id {int} -- index of user
#     """
#     records_to_remove = user_dict[str(user_id)]
#     user_dict.pop(str(user_id), None)
#     records_removed = 0
#     for r_id_to_remove in records_to_remove:
#         for index_record in range (len(result_dict["points"])):
#         # print(result_dict["points"][index_record]["r_id"])
#             if (result_dict["points"][index_record]["r_id"] == r_id_to_remove):
#                 del result_dict["points"][index_record]
#                 records_removed += 1
#                 break

#     # check
#     print(len(records_to_remove) == records_removed)
#     return(user_dict, result_dict)

# result = import_json("results_poc_after_ennum.json")
# user_dict = import_json("user_dict_300.json")
# users_to_remove = [169, 57, 157, 167, 170, 181, 288, 163, 164, 165, 166, 188, 190, 191, 192, 193, 194, 195, 240, 241, 242, 296]

# for user in users_to_remove:
#     new_user_dict, new_result = remove_user(user_dict, result, user)

# # export
# export_json(new_result, "results_poc_after_user_removal.json")
# export_json(new_user_dict, "user_dict_after_user_removal.json")

#################
# changer tf: ok
# changer à la main les quelques doubles exit =1,
# une seule homographie,
# mettre y seuil

# results_poc_after_tf_exit.json

####################
# revert homography
# change x and y from initial results

# frame 1680
# pts_camera = [
#     [87, 432],
#     [246, 287],
#     [746, 292],
#     [814, 441]
# ]
# pts_2D_plane = [
#     [0, 11],
#     [0, 0],
#     [10, 0],
#     [10, 11]
# ]
# h = get_homograpy(np.array(pts_camera), np.array(pts_2D_plane))

# # import result
# result = import_json("results_poc_after_tf_exit.json")
# result_before_h = import_json("results_poc_before_homography.json")
# for record in result["points"]:
#     r_id = record["r_id"]
#     r_id_in_list = r_id-300
#     x = result_before_h["points"][r_id_in_list-1]["x"]
#     y = result_before_h["points"][r_id_in_list-1]["y"]
#     point_before = np.array([[x,y]], dtype='float32')
#     point_before = np.array([point_before])
#     pointsOut = cv2.perspectiveTransform(point_before, h)
#     record["x"] = float(pointsOut[0][0][0])
#     record["y"] = float(pointsOut[0][0][1])
# # export
# export_json(result, "results_poc_after_one_h.json")
# # x and y to round


######################
# remove seuil

###########################################
# enlever les records tels que y > y_seuil = 18
result = import_json('results_poc_after_one_h.json')
new_result = copy.deepcopy(result)
new_result["points"] = []
print(new_result)
y_seuil = 20
for record in result["points"]:
    if (record["y"] < y_seuil):
        new_result["points"].append(record)


export_json(new_result, 'results_poc_y_seuil.json')



# TO SEND
# user dict
# beacon_dict
# last results

# Voici les résultats avec quelques modif:
# * changer tf
# * changer les quelques doubles exit =1,
# * une seule homographie sur la frame 1680 assez stable à partir de la frame ~1500
# * mettre y seuil = 20
