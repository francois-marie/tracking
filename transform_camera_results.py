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


# subsampler toutes les secondes au min

result_time = import_json('results_poc_after_time.json')

print(len(result_time["points"]))

for i in range (len(result_time["points"])):
    if (i > 202210 or i<0):
        print(i)
    if (result_time["points"][i]["t"] % 1000 != 0):
        #print(result_time["points"][i]["t"])
        del result_time["points"][i]

export_json(result_time, 'results_poc_after_subsample.json')

# étape 1: c'est construire le dict des users


# En 2 tu passes tous les points en caméra avec des t_id différents (met leur r_id au pire -> dans ce cas, prends les u_id à partir de 1000 pour éviter les collisions).



# En 3 tu enumerate sur les items du dict u_id, list_rids et en parcourant les r_ids, si (c'est le premier ou le dernier point ou si il est dans une zone autour d'un beacon), tu passes simplement son t_id à u_id



# enlever des tid user pour les remplacer par des tid camera



# envoyer un dict des tids users vers la liste des rids de leurs points



# affecter des points bluetooth par zone autour de supposés beacons bluetooth pour donner des points nominatifs
#  au début et le plus possible au milieu des trajectoires
# Ex: id < 1000 pour users et > 1000 pour les traces




# liste des beacons avec leur position et leur rayon