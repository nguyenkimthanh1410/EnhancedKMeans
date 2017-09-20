import numpy as np
import scipy
import random

# Purpose: Initialize centroids as centers of equal partitions by default.
# If error occurs, switch automatically to the distinct actual points


# =====================INITIAL MIDPOINTS AS CENTER OF EQUAL PARTITIONS (USING PERCENTILE)===============================
# Class Partition is used to hold data about a specific partition (lower_bound, upper_bound, list_values, midpoint)
class Partition:
    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.list_values = []

    def add_a_value_to_partition(self, new_point):
        self.list_values.append(new_point)

    def get_list_values(self):
        return self.list_values

    def get_partition_midpoint(self):
        np_array_temp = np.array(self.list_values)
        partition_midpoint = np.mean(np_array_temp).tolist()
        return partition_midpoint

    def get_lower_bound(self):
        return self.lower_bound

    def get_upper_bound(self):
        return self.upper_bound

# =====================FIND MEAN FOR EACH FEATURE ONLY==================================================================
"""
    Purpose: Find midpoint of each partition.
            Divide the range_value into num_partion, number of data value in each partition equally (using percentile)
    Input: a range_values_of_a_feature, and num_partition
    Output: list_scrambled_midpoints_for_each_feature
    How to do:
    1. Find lower and upper bound of each partition
    2. Assign points belong to each partition
    3. Find midpoint of a partition
    => Use a class Partition to keep (lower bound, upper bound, list_partitions_points)
"""

def find_initial_midpoints_for_each_feature(range_values_of_a_feature, num_partition):

    list_scrambled_midpoints_for_a_feature = []

    #1.Find lower_bound, upper_bound of each partition
    list_partitions = []
    np_range_values = np.array(range_values_of_a_feature)  # convert into numpy array to get percentile

    for i in range(num_partition):
        #print("i=", i)
        lower_bound = np.percentile(np_range_values, round(100 / num_partition * i, 2))
        upper_bound = np.percentile(np_range_values, round(100 / num_partition * (i + 1), 2))

        new_partition = Partition(lower_bound, upper_bound)
        list_partitions.append(new_partition)  # keep new_partition otherwise, it will go away
        # print("\nlower_bound: {}, upper_bound: {}".format(lower_bound, upper_bound))


    #2. Assign right values to each partition
    """
    Scan through np_range_values, for each value
        scan through list of partition
            if value in [lower, upper)
                append to the list_values for respective partion
        if the value >=upper of last partition (check each value in array to cover up the upper-bound of last partition)
                append that value into last partition
    """
    last_partition = list_partitions[len(list_partitions) - 1]
    for value in np_range_values:
        for partition in list_partitions:
            if value >= partition.get_lower_bound() and value < partition.get_upper_bound():
                partition.add_a_value_to_partition(value)


        # check each value in array to cover up the upper-bound of last partition
        if value >= last_partition.get_upper_bound():
            last_partition.add_a_value_to_partition(value)


    # !!!!!!IMPORTANT: If ANY PARTITION HAS NO ELEMENTS ASSIGNED FOR IT
    # (OR When empty list), Notify caller, to change method to randomly select actual points
    empty_value =""
    for partition in list_partitions:
        if len(partition.get_list_values()) ==0:
            print("No actual values assigned to partition of this dimension")
            empty_value = True

    #3. Find midpoint for each partition
    count_parttiton = 1
    for partition in list_partitions:
        scrambled_midpoint = partition.get_partition_midpoint()
        list_scrambled_midpoints_for_a_feature.append(scrambled_midpoint)
        count_parttiton += 1

    #print("Display list_scrambled_midpoints_for_a_feature:")
    #print(list_scrambled_midpoints_for_a_feature)

    return list_scrambled_midpoints_for_a_feature, empty_value
#===============================END OF FUNCTION: Output: list_scrambled_midpoints_for_a_feature only====================



#====================================FUNCTION: Find all dimensions for k midpoint=======================================
def find_all_k_midpoint_list(all_k_midpoint_list, all_point_list, k_cluster):
    print("Inital midpoints: Equal Partitions")

    # Grab entire column
    scipy_array = scipy.array(all_point_list) #to extract values from 2 dimenstional array vertically

    print(all_point_list)

    # Add on 04/09/2016: If no values assigned to partition.
    # Let switch to randomly choose distinct datapoint to become initial midpoint
    not_empty = True
    while not_empty:
        list_initial_midpoints_combined = []
        for feature_index in range(len(all_point_list[0])):

            x = scipy_array[:, feature_index] #Extract a feature
            y = x.tolist()

            list_initial_midpoints_for_a_feature, empty_value = find_initial_midpoints_for_each_feature(y, k_cluster)
            #print("list_midpoint in {}th feature".format(feature_index))
            #print(list_initial_midpoints_for_a_feature)

            if empty_value == True:
                not_empty = False
                break #break for loop

            # Combined into 2-dimensional array according to each feature
            list_initial_midpoints_combined.append(list_initial_midpoints_for_a_feature)

        if not_empty == False:
             break #brak while loop

        #Transposed numpy_array to get co-ordinate of each midpoint
        all_k_midpoint_list = np.array(list_initial_midpoints_combined).T.tolist()


        #print("Out of For loop but inside While loop==========================")
        #print(all_k_midpoint_list)
        return all_k_midpoint_list


    #print("Out of while loop==============================")
    print("Inital midpoints: Partition-> Actual as No actual values assigned to certain partitions")
    all_k_midpoint_list = find_initial_centroids_in_actual_points(all_k_midpoint_list, all_point_list, k_cluster)
    return all_k_midpoint_list



# =====================INITIAL MIDPOINTS AS DISTINCT ACTUAL DATA POINTS=================================================
# OP2: Select starting midpoints as randomly distinct data points
def find_initial_centroids_in_actual_points(all_k_midpoint_list, all_point_list, k_cluster):
    print("Initial centroids: Actual points")
    for i in range(k_cluster):
        rand_index = random.randint(0,k_cluster-1)
        rand_point = all_point_list[rand_index]

        while rand_point in all_k_midpoint_list: # Check for distinction
            rand_index = random.randint(0, k_cluster-1)
            rand_point = all_point_list[rand_index]
        all_k_midpoint_list.append(rand_point)

    return all_k_midpoint_list