import numpy as np
from scipy.spatial import distance
from kdd_kmean_enhanced.data_mining import Cluster
from kdd_kmean_enhanced.data_mining import initial_centroids
from kdd_kmean_enhanced.pre_mining import get_relevant_data, normalize_data



#===========================================START K-MEAN CLUSTERING=====================================================
# Input: cluster_list, k_cluster, list point normalized
# Output: cluster_list, and initial_centroids. Each cluster includes midpoint, points belonging to that cluster


#=================Create cluster_list THE FIRST TIME====================
# 1. Having a cluster_list containing k_cluster elements
# Each element is a cluster (cluster_midpoint, cluster_point_list)
def declare_brandnew_k_cluster_list_with_k_midpoint(cluster_list, k_cluster, all_k_midpoint_list):

    #CLEAR ALL EXISTING POINTS IN THE CURRENT LIST
    cluster_list = []

    for k in range(k_cluster):
        midpoint_kth = all_k_midpoint_list[k]
        new_cluster = Cluster.Cluster(midpoint_kth)
        cluster_list.append(new_cluster)
    return cluster_list


# Calculate distance between 2 points
def calculate_distance_between_two_point(dp, midpoint):
    #print("dp=", dp)
    #print("midpoint=", midpoint)
    a = np.array(dp)
    b = np.array(midpoint)
    dist = distance.euclidean(a,b)
    return dist

def assign_a_point_to_cluster_closest(dp, midpoint_closest, cluster_list):
    for cluster in cluster_list:
        if cluster.get_midpoint() == midpoint_closest: #FORGET () For method
            cluster.add_point_to_cluster_point_list(dp)


def allocate_points_to_brandnew_k_cluster_list(cluster_list, all_point_list, all_k_midpoint_list):
    #print("\nCalculate distance and assign points to nearest cluster")
    for dp in all_point_list:
        # For each dp, initially assuming that:
        # midpoint_closest is first midpoint,
        # distant_closest will be from dp to midpoint_closest
        midpoint_closest = all_k_midpoint_list[0]
        current_dist_closest = calculate_distance_between_two_point(dp, midpoint_closest)

        # Calculate and compare all distance from dp to all other midpoints
        for midpoint in all_k_midpoint_list:
            dist_temp = calculate_distance_between_two_point(dp, midpoint)
            if dist_temp < current_dist_closest:
                current_dist_closest = dist_temp
                midpoint_closest = midpoint

        # Assign to the cluster that having distance min
        assign_a_point_to_cluster_closest(dp, midpoint_closest, cluster_list)
    return cluster_list


def recalculate_all_k_midpoint_list(cluster_list):
    all_k_midpoint_list_brandnew_temp = []

    for cluster in cluster_list:
        new_midpoint = cluster.recalculate_midpoint()
        all_k_midpoint_list_brandnew_temp.append(new_midpoint)

    return all_k_midpoint_list_brandnew_temp

def is_all_cluster_midpoint_changed(all_k_midpoint_list, all_k_midpoint_list_brandnew):
    return not (all_k_midpoint_list == all_k_midpoint_list_brandnew) #when 2 values different: not false -> true


def clustering(cluster_list, all_point_list, k_cluster, value_cut_off_clustering, option_initial_centroids="Partition"):
    num_iter = 1
    print("{} round - Starting clustering----------".format(num_iter))

    all_k_midpoint_list = []

    # By default: starting midpoints using equal partitions (Percentile).
    # If error occurs: switch to randomly distinct actual points
    if(option_initial_centroids =="Partition"): #06/09/2016: MIS---SPELLING
        all_k_midpoint_list =\
            initial_centroids.find_all_k_midpoint_list(all_k_midpoint_list, all_point_list, k_cluster)
    elif (option_initial_centroids =="Actual"):
        all_k_midpoint_list = \
            initial_centroids.find_initial_centroids_in_actual_points(all_k_midpoint_list,all_point_list, k_cluster)
    inital_k_midpoint = all_k_midpoint_list[:]

    # STEP 1: Create Only midpoints Attribute for each cluster
    cluster_list = declare_brandnew_k_cluster_list_with_k_midpoint(cluster_list, k_cluster, all_k_midpoint_list)

    # STEP 2: Assign point to each cluster
    cluster_list = allocate_points_to_brandnew_k_cluster_list(cluster_list, all_point_list, all_k_midpoint_list)
    print("{} round - Finish clustering----------".format(num_iter))


   #====================================RECALCULATE MIDPOINT FOR EACH CLUSTER=========================================
    ''' Algos:
        for each cluster in cluster_list
         - Recalculate cluster_midpoint
         - Unless all cluster_midpoint unchanged or cut-off: break
         - otherwise assign a new value to cluster_midpoint
         -      go for Step 1, 2 (create midpoint for clusters, assign points to clusters)
        '''
    all_k_midpoint_list_brandnew = recalculate_all_k_midpoint_list(cluster_list)
    while is_all_cluster_midpoint_changed(all_k_midpoint_list, all_k_midpoint_list_brandnew)\
            and (num_iter<=value_cut_off_clustering):
        num_iter += 1
        print("{} round - Start clustering-----------".format(num_iter))

        # Assign new value for all_k_midpoint_list
        all_k_midpoint_list = all_k_midpoint_list_brandnew

        # Go back step 1, 2
        cluster_list = declare_brandnew_k_cluster_list_with_k_midpoint(cluster_list, k_cluster, all_k_midpoint_list)
        cluster_list = allocate_points_to_brandnew_k_cluster_list(cluster_list, all_point_list, all_k_midpoint_list)

        # 14/09/2016: Take it down, combine this condition into while loop's criteria
        #if (num_iter > value_cut_off_clustering):
         #   break

        # If not reach cutoff value, RECALCULATE MIDPOINT for new clusters
        all_k_midpoint_list_brandnew = recalculate_all_k_midpoint_list(cluster_list)

        print("{} round - Finish clustering-----------".format(num_iter))

        # Reach this point: While loop does its job to call a function to check condition: MIDPOINTS CHANGED OR NOT

        # DISPLAY ON CONSOLE WINDOWS TO CHECK list of midpoint new and old
        #print("\nPrint out all_k_midpoint_list_brandnew: ")
        #display_elements_in_a_list(all_k_midpoint_list_brandnew)
        #print("\nPrint out all_k_midpoint_list current:")
        #display_elements_in_a_list(all_k_midpoint_list)

    #print("\n=====================FINISH CLUSTERING=============================")
    #print("Midpoints finally have been unchanged or greater than cutof = {}".format(value_cut_off_clustering))
    #print("Program stopped at {}th loop".format(num_iter))
    #display_info_cluster_list(cluster_list)

    return cluster_list, inital_k_midpoint, num_iter
    # =====================================END OF CLUSTERING FUNCTIONG=================================================



#====================================== 2 functions below to DISPLAY results============================================
# Display items in a list
def display_elements_in_a_list(point_list):
    print("There are: {} points in list".format(len(point_list)))
    count_point = 1
    for point in point_list:
        print("Point {}: {}".format(count_point, point))
        count_point +=1

# Display each cluster in cluster list
def display_info_cluster_list(cluster_list):
    print("\nPrint out Cluster_list:")
    count_cluster = 1
    for cluster in cluster_list:
        print("\nCluster ", count_cluster)
        print("Midpoint =", cluster.get_midpoint())
        display_elements_in_a_list(cluster.get_cluster_point_list())
        count_cluster += 1
#====================================== 2 functions below to DISPLAY results============================================
