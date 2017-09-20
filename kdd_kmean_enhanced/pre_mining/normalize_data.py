import numpy as np


# Task 2: Calculate descriptive summary
def calculate_descriptive_summary(list_2dim):

    # Extract values from the 4 lists ->store data in descriptive_statistic for each dimension
    descriptive_statistic_list = []

    # Calculate statistic value
    all_point_list_np = np.array(list_2dim)
    min_values = np.min(all_point_list_np, axis=0)
    max_values = np.max(all_point_list_np, axis=0)
    mean_values = np.mean(all_point_list_np, axis=0)
    std_values = np.std(all_point_list_np, axis=0)

    descriptive_statistic_list.append(min_values)
    descriptive_statistic_list.append(max_values)
    descriptive_statistic_list.append(mean_values)
    descriptive_statistic_list.append(std_values)

    return descriptive_statistic_list


# Task 3: Normalize data using Zscore
def normalize_by_zscore(list_2dim):
    descriptive_statistic_list = calculate_descriptive_summary(list_2dim)
    mean_list = descriptive_statistic_list[2]
    std_list = descriptive_statistic_list[3]

    list_zscores = (list_2dim - mean_list)/std_list
    return list_zscores.tolist(), mean_list.tolist(), std_list.tolist()


# Task 4: Normalize data using lower_bound and upper_bound (eg: 0-1)
def normalize_by_lower_upper_bound(list_2dim, min_bound, max_bound):
    descriptive_statistic_for_each_dim_list = calculate_descriptive_summary(list_2dim)
    min_list = descriptive_statistic_for_each_dim_list[0]
    max_list = descriptive_statistic_for_each_dim_list[1]

    list_values_normalized = (max_bound - min_bound) / (max_list - min_list) * (list_2dim - min_list) + min_bound
    #print("List after MinMax normalization")
    #display_element_in_list(list_values_normalized)
    return list_values_normalized.tolist(), min_list.tolist(), max_list.tolist()


# Task 5: Display data points in the list in console window
def display_element_in_list(points_list):
    print("There are: {} points in list".format(len(points_list)))
    count_point = 1
    for point in points_list:
        print("Point {}: {}".format(count_point, point))
        #print(point)
        count_point +=1

