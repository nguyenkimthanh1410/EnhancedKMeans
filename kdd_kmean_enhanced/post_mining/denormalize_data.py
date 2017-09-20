import numpy as np
#====================================DENORMALIZATION WITH ZSCORE OR MINMAX==============================================
# 1.1. Denormalize Zscore list
def demormalize_list_by_zscores(result_list_2dim_in_zscores, mean_list, std_list):
    result_list_2dim_in_zscores_np = np.array(result_list_2dim_in_zscores)
    mean_list_np = np.array(mean_list)
    std_list_np = np.array(std_list)
    list_denormalized = std_list_np*result_list_2dim_in_zscores_np + mean_list_np
    return list_denormalized.tolist()

# 1.2. Demormalization cluster_list with Zscore Normalization
# !!!!!ATTENTION: Input list of Cluster objects, return a list of list points
def denormalize_clusters_zscores(cluster_list_normalized, mean_list, std_list):
    cluster_list_denormalized = []
    for cluster_i in cluster_list_normalized:
        cluster_denormalized = demormalize_list_by_zscores(cluster_i.get_cluster_point_list(), mean_list, std_list)
        cluster_list_denormalized.append(cluster_denormalized)
        #print(cluster_denormalized)
    return cluster_list_denormalized



# 2.1. Denormalize MINMAX: min_bound, max_bound(eg:0-1)
def demormalize_list_by_MinMax(result_list_2dim_within_lower_upper_bound, min_bound, max_bound, min_list, max_list):
    result_list_2dim_within_lower_upper_bound_np = np.array(result_list_2dim_within_lower_upper_bound)
    min_list_np = np.array(min_list)
    max_list_np = np.array(max_list)

    list_denormalized = \
        (result_list_2dim_within_lower_upper_bound_np - min_bound) * (max_list_np - min_list_np) / (max_bound - min_bound) + min_list_np
    return list_denormalized

# 2.2. Demormalization cluster_list with MINMAX normalization
#!!!!!!ATTENTION: Input list of Cluster objects, return a list of list points
def denormalize_clusters_MinMax(cluster_list_normalized, lower_bound, upper_bound, min_list, max_list):
    cluster_list_denormalized = []
    for cluster_i in cluster_list_normalized:
        cluster_denormalized = demormalize_list_by_MinMax(cluster_i.get_cluster_point_list(),lower_bound, upper_bound, min_list, max_list)
        cluster_list_denormalized.append(cluster_denormalized)
        #print(cluster_denormalized)
    return cluster_list_denormalized


