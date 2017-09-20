import math
import numpy as np
from kdd_kmean_enhanced.data_mining import mining_process

#====================================EVALUATE RESULT USING SSE (SUM SQUARE ERROR)=======================================
def calculate_midpoint_a_list(list_normalized_2dim):
    np_array_temp = np.array(list_normalized_2dim)
    np_array_midpoint = np.mean(np_array_temp, axis=0)
    return np_array_midpoint.tolist()

# Calculate Within sum square error (WSS) = Total square between points within a cluster to its midpoints
def calculate_within_sum_square_error(list_clusters_normalized):
    within_sum_square_error = 0
    for each_cluster in list_clusters_normalized:

        wsse_each_cluster = 0
        midpoint_each_cluster = each_cluster.get_midpoint()
        #print("Midpoint each cluster: ", midpoint_each_cluster)

        for each_point in each_cluster.get_cluster_point_list():
            #print("Each point examined: ", each_point)
            dist_to_midpoint = mining_process.calculate_distance_between_two_point(each_point, midpoint_each_cluster)
            #print("distance to midpoint: ", dist_to_midpoint)

            wsse_each_cluster += math.pow(dist_to_midpoint,2)

        within_sum_square_error +=wsse_each_cluster
    return within_sum_square_error

# Calculate Between sum square error (BSS) = Total square between each midpoint to mean
def calculate_between_sum_square_error(list_clusters_normalized, list_points_normalized):
    between_sum_square_error = 0
    midpoint_dataset = calculate_midpoint_a_list(list_points_normalized)

    for each_cluster in list_clusters_normalized:
        dist_to_midpoint_dataset =\
            mining_process.calculate_distance_between_two_point(each_cluster.get_midpoint(), midpoint_dataset)
        size_a_cluster = len(each_cluster.get_cluster_point_list())
        between_sum_square_error += size_a_cluster * math.pow(dist_to_midpoint_dataset,2)

    return between_sum_square_error

def calculate_total_sum_square_error(list_clusters_normalized, list_points_normalized):
    wsse = calculate_within_sum_square_error(list_clusters_normalized)
    bsse = calculate_between_sum_square_error(list_clusters_normalized, list_points_normalized)
    return (wsse + bsse)

