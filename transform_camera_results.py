import json


def export_json(data, name):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    return()

def import_json(name):
    data = json.load(open(name, 'r'))
    return(data)




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


user_dict = import_json("user_dict_300.json")
beacon_dict = import_json("beacon_dict.json")

result = import_json('results_poc_after_300.json')

def inside_beacon(results, i, beacon_dict):
    """know if a record is inside a beaon

    Arguments:
        results {dict} -- dict for the algo
        i {int} -- index of record in list "points"
        beacon_dict {dict} -- dict of referenced beacons bluetooth
    """
    x = results["points"][i]["x"]
    y = results["points"][i]["y"]
    for beacon in beacon_dict["beacon"]:
        center_x = beacon["x"]
        center_y = beacon["y"]
        radius = beacon["r"]
        if ((x - center_x)**2 + (y - center_y)**2 < radius**2):
            return(True)
    return(False)


for i, (k, v) in enumerate(user_dict.items()):
    # print(i, k, v)
    # print("#"*10)
    # print(k + "  "+str(v))
    for r_id_of_u in v:
        for i in range (len(result["points"])):
            if (result["points"][i]["t_id"] == r_id_of_u):
                # print("i : ", i)
                if (r_id_of_u == user_dict[k][0] or r_id_of_u == user_dict[k][-1] or inside_beacon(result, i, beacon_dict)):
                    result["points"][i]["t_id"] = int(k)
                    result["points"][i]["r_type"] = "bluetooth"
                    if (r_id_of_u == user_dict[k][-1]):
                        result["points"][i]["md"]["exit"] = True


export_json(result, 'results_poc_after_ennum.json')

# check
check_list = []
for i in range (len(result["points"])):
    if(result["points"][i]["t_id"] < 300):
        check_list.append(i)



# change tf


# affecter des points bluetooth par zone autour de supposés beacons bluetooth pour donner des points nominatifs
#  au début et le plus possible au milieu des trajectoires
# Ex: id < 1000 pour users et > 1000 pour les traces




# liste des beacons avec leur position et leur rayon


# SEND
# user dict
# beacon_dict
# last results