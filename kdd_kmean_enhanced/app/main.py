# Using starting midpoint in the range lower-upper percentile
# With a NEW FILE: user provides 4 input: filename, num_columns_taken_out, k_cluster, value_cut_off_clustering
import time
from kdd_kmean_enhanced.pre_mining import get_relevant_data
from kdd_kmean_enhanced.pre_mining import normalize_data
from kdd_kmean_enhanced.data_mining import mining_process
from kdd_kmean_enhanced.post_mining import evaluate_result
from kdd_kmean_enhanced.post_mining import denormalize_data
from kdd_kmean_enhanced.post_mining import output_csv
from kdd_kmean_enhanced.app import validate_input

#=========================================PRE-MINING ===================================================================
# 1. INITIAL SETUPS WITH DEFAULT PARAMETERS
num_attributes_unwanted = 2
cut_off_clustering = 100
min_bound = 0
max_bound = 1
normalization_dict = {"Z":"Zscore","M":"MinMax"}
inital_centroids_dict = {"P": "Partition", "A": "Actual"}


# 2. READ CSV FILE INTO PROGRAM AND REMOVE UNWANTED ATTRIBUTES
file_object = open("Wholesale_customers_data.csv", "r")

# Read point into all_point_list, Remove unwanted attributes from file input
# Note: Explicitly pass all_point_list to functions (pass object ref)
list_points_interested_attr = []
list_points_interested_attr=\
   get_relevant_data.remove_unwanted_attributes(list_points_interested_attr, file_object, num_attributes_unwanted)
num_records = len(list_points_interested_attr)


# 3. GET USER 2 INPUTS AND VALIDATE THEM (Number of cluster, Method for Normalization, Initial centroids)
# Number of cluster must be integer within 1 to num_records
message= "Enter number of cluster: "
k_cluster = validate_input.validate_int_in_range_inc(1, num_records, message)
print("You chose {} clusters".format(k_cluster))

# Method for normalization: MinMax(0,1) or Zscore
valid_input_method_bool = False
while not valid_input_method_bool:
    input_str = input("Normalization method(Z for Zscore, M for MinMax[0,1]): ").upper()
    if input_str == "Z":
        norm_method = normalization_dict.get(input_str)
        valid_input_method_bool = True
    elif input_str == "M":
        norm_method = normalization_dict.get(input_str)
        valid_input_method_bool = True
    else:
        print("Bad input, it must be Z or M")
print("You chose method {} for Normalization".format(norm_method))

# Option for initial centroids
validate_input_initial_centroid_bool = False
while not validate_input_initial_centroid_bool:
    input_str_centroids = input("Input option initial centroids(P for Partition, A for Actual: ").upper()
    if input_str_centroids == "P":
        option_initial_centroids = inital_centroids_dict.get(input_str_centroids)
        validate_input_initial_centroid_bool = True
    elif input_str_centroids == "A":
        option_initial_centroids = inital_centroids_dict.get(input_str_centroids)
        validate_input_initial_centroid_bool = True
    else:
        print("Bad input, it must be P or A")
print("You chose {} for Initial Centroids".format(option_initial_centroids))


#4. NORMALIZATION: Z for Zscore, M: MinMax[min_bound, max_bound]
#list_norm = []
if norm_method == "Zscore":
    list_norm, mean_list, std_list = normalize_data.normalize_by_zscore(list_points_interested_attr)
elif norm_method == "MinMax":
    list_norm, min_list, max_list = \
        normalize_data.normalize_by_lower_upper_bound(list_points_interested_attr, min_bound, max_bound)
#========================================== END OF PRE-MINING===========================================================


#===========================================START K-MEAN CLUSTERING=====================================================
# Input: cluster_list, k_cluster, list point normalized
# Output: cluster_list, each cluster includes midpoint, points belonging to that cluster
print("\nStart clustering..............")

cluster_list_norm = []
start = time.time()
if norm_method == "Zscore":
    if option_initial_centroids == "Actual":
        print("User delibrately Clustering: Norm.Zscore, Initial centroids:Actual")
        cluster_list_norm, initial_k_midpoint_normalized, num_iter = \
            mining_process.clustering(cluster_list_norm, list_norm, k_cluster, cut_off_clustering, "Actual")
    elif option_initial_centroids == "Partition":
        try:
            print("Clustering: Norm. Zscore, Initial centroids: Partition")
            cluster_list_norm, initial_k_midpoint_normalized, num_iter =\
            mining_process.clustering(cluster_list_norm, list_norm, k_cluster, cut_off_clustering)
        except Exception:
            print("Exception occurs, Change: Norm. Zscore, Initial centroids: Partition =========>Actual")
            cluster_list_norm, initial_k_midpoint_normalized, num_iter = \
                mining_process.clustering(cluster_list_norm, list_norm, k_cluster, cut_off_clustering,"Actual")
        #!!!!!!!!!!!!!!!!!Attention: To handle error occurs, can't assign values to clusters with Partion => Swtich to Actual

elif norm_method == "MinMax":
    if option_initial_centroids == "Actual":
        print("User delibrately: Norm. MinMax, Initial centroids: Actual")
        cluster_list_norm, initial_k_midpoint_normalized, num_iter = \
            mining_process.clustering(cluster_list_norm, list_norm, k_cluster, cut_off_clustering, "Actual")
    elif option_initial_centroids == "Partition":
        try:
            print("Clustering: Norm. MinMax, Initial centroids: Partition")
            cluster_list_norm, initial_k_midpoint_normalized, num_iter = \
                mining_process.clustering(cluster_list_norm, list_norm, k_cluster, cut_off_clustering)
        except Exception:
            print("Exception occurs, Change: Initial centroids: Partition ====> Actual")
            cluster_list_norm, initial_k_midpoint_normalized, num_iter = \
                mining_process.clustering(cluster_list_norm, list_norm, k_cluster, cut_off_clustering, "Actual")

end = time.time()
elapsed_time = end - start
print("Elapsed time: {} seconds".format(elapsed_time))
print("Number of iteration: {}".format(num_iter))

print("\nFinish clustering..............")
#===========================================END CLUSTERING ============================================================



#===========================================DENORMILIZATION OUTPUT=====================================================
# Denormalize output to orginal values before writing result to_file
#!!! ATTENTION: Return a list of list, no longer a list of Clusters object, as using scipy

if norm_method == "Zscore":
    cluster_list_denorm = denormalize_data.denormalize_clusters_zscores(cluster_list_norm, mean_list, std_list)

    initial_k_midpoint_denormalized = \
        denormalize_data.demormalize_list_by_zscores(initial_k_midpoint_normalized, mean_list, std_list)

elif norm_method == "MinMax":
    cluster_list_denorm =\
        denormalize_data.denormalize_clusters_MinMax(cluster_list_norm, min_bound, max_bound, min_list, max_list)

    initial_k_midpoint_denormalized = \
    denormalize_data.demormalize_list_by_MinMax(initial_k_midpoint_normalized, min_bound, max_bound, min_list, max_list)


#===========================================EVALUTATE OUTPUT===========================================================
# EVALUATE OUTPUT by Sum Square Error (SSE) = Within SSE (WSSE) + Between SSE (BSSE)

wsse = evaluate_result.calculate_within_sum_square_error(cluster_list_norm)
print("Within SSE = {}".format(wsse))

bsse = evaluate_result.calculate_between_sum_square_error(cluster_list_norm, list_norm)
print("Between SSE = {}".format(bsse))

total_sse = evaluate_result.calculate_total_sum_square_error(cluster_list_norm, list_norm)
print("Total SSE = {}".format(total_sse))


#===========================================OUTPUT RESULTS TO CSV FILE==================================================
# Write detail points in each cluster
output_csv.write_detail_result_to_file(cluster_list_denorm, norm_method, option_initial_centroids)

num_observations =len(list_norm)

# Write summary of output including sse
output_csv.write_summary_result_to_file(cluster_list_denorm, num_observations, \
                                        initial_k_midpoint_denormalized, num_iter, \
                                        elapsed_time, wsse, bsse, norm_method, option_initial_centroids)
#===========================================END OF OUTPUT RESULTS TO CSV FILE===========================================

