import time
from kdd_kmean_enhanced.pre_mining import get_relevant_data
from kdd_kmean_enhanced.pre_mining import normalize_data
from kdd_kmean_enhanced.data_mining import mining_process
from kdd_kmean_enhanced.post_mining import evaluate_result
from kdd_kmean_enhanced.post_mining import denormalize_data
from kdd_kmean_enhanced.app import validate_input
import csv

# Function to perform clustering with k from 1 to_num_cluster
# given combination of user input (Normalization method, Initial centroids)
# Note: Already update validate input (13/09/2016)

def eval_enhance_kmeans(to_num_cluster, norm_method, option_initial_centroids):
    file_out = open("eval_kmeans_k_1_{}clusters_{}_{}.csv".format(to_num_cluster, norm_method,option_initial_centroids),"w")
    csvwriter = csv.writer(file_out, delimiter=' ',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(["Norm.method", "Init.centroids", "___k___", "__iter__",\
                        "____Time____", "___wsse___", "___bsse___", "___sse___", "___%wsse/sse___"])

    # 1. INITIAL SETUPS WITH DEFAULT PARAMETERS
    num_attributes_unwanted = 2
    cut_off_clustering = 100

    min_bound = 0
    max_bound = 1
    #normalization_dict = {"Z": "Zscore", "M": "MinMax"}
   # option_initial_centroids = "Partition"

    # 2. READ CSV FILE INTO PROGRAM AND REMOVE UNWANTED ATTRIBUTES
    file_object = open("Wholesale_customers_data.csv", "r")

    # Read point into all_point_list, Remove unwanted attributes from file input
    # Note: Explicitly pass all_point_list to functions (pass object ref)
    list_points_interested_attr = []
    list_points_interested_attr = \
        get_relevant_data.remove_unwanted_attributes(list_points_interested_attr, file_object, num_attributes_unwanted)
    num_records = len(list_points_interested_attr)


    for k_cluster in range (1,to_num_cluster+1):
        print("===============================\nK_cluster =", k_cluster)

        if norm_method == "Zscore":
            list_norm, mean_list, std_list = normalize_data.normalize_by_zscore(list_points_interested_attr)
        elif norm_method == "MinMax":
            list_norm, min_list, max_list = \
                normalize_data.normalize_by_lower_upper_bound(list_points_interested_attr, min_bound, max_bound)

        # ===========================================START K-MEAN CLUSTERING=====================================================
        # Input: cluster_list, k_cluster, list point normalized
        # Output: cluster_list, each cluster includes midpoint, points belonging to that cluster

        # !!!!!!!!!!Note that: By default, USING INITAL CENTROIDS ARE MEANS OF EQUAL PARTITIONS
        print("\nStart clustering..............")

        cluster_list_norm = []
        start = time.time()
        if norm_method == "Zscore":
            if option_initial_centroids == "Actual":
                print("User delibrately Clustering: Norm.Zscore, Initial centroids:Actual")
                cluster_list_norm, initial_k_midpoint_normalized, num_iter = \
                    mining_process.clustering(cluster_list_norm, list_norm, k_cluster, cut_off_clustering, "Actual")
            else:
                try:
                    print("Clustering: Norm. Zscore, Initial centroids: Partition")
                    cluster_list_norm, initial_k_midpoint_normalized, num_iter = \
                        mining_process.clustering(cluster_list_norm, list_norm, k_cluster, cut_off_clustering)
                except Exception:
                    print("Exception occurs, Change: Norm. Zscore, Initial centroids: Partition =========>Actual")
                    cluster_list_norm, initial_k_midpoint_normalized, num_iter = \
                        mining_process.clustering(cluster_list_norm, list_norm, k_cluster, cut_off_clustering, "Actual")
                    # !!!!!!!!!!!!!!!!!Attention: To handle error occurs, can't assign values to clusters with Partion => Swtich to Actual


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
        # ===========================================END CLUSTERING ============================================================



        # ===========================================DENORMILIZATION OUTPUT=====================================================
        # Denormalize output to orginal values before writing result to_file
        # !!! ATTENTION: Return a list of list, no longer a list of Clusters object, as using scipy

        if norm_method == "Zscore":
            cluster_list_denorm = denormalize_data.denormalize_clusters_zscores(cluster_list_norm, mean_list, std_list)

            initial_k_midpoint_denormalized = \
                denormalize_data.demormalize_list_by_zscores(initial_k_midpoint_normalized, mean_list, std_list)

        elif norm_method == "MinMax":
            cluster_list_denorm = \
                denormalize_data.denormalize_clusters_MinMax(cluster_list_norm, min_bound, max_bound, min_list, max_list)

            initial_k_midpoint_denormalized = \
                denormalize_data.demormalize_list_by_MinMax(initial_k_midpoint_normalized, min_bound, max_bound,
                                                           min_list, max_list)

        # ===========================================EVALUTATE OUTPUT===========================================================
        # EVALUATE OUTPUT by Sum Square Error (SSE) = Within SSE (WSSE) + Between SSE (BSSE)

        wsse = evaluate_result.calculate_within_sum_square_error(cluster_list_norm)
        print("Within SSE = {}".format(wsse))

        bsse = evaluate_result.calculate_between_sum_square_error(cluster_list_norm, list_norm)
        print("Between SSE = {}".format(bsse))

        total_sse = evaluate_result.calculate_total_sum_square_error(cluster_list_norm, list_norm)
        print("Total SSE = {}".format(total_sse))

        #============================Writing to a file==================================================================
        # csvwriter.writerow(["Norm.method", "Init.centroids", "___k___", "__iter__", "____Time____", "___wsse___", "___bsse___", "___sse___", "___%wsse/sse___"])

        out = []
        out.append(norm_method)
        out.append(option_initial_centroids)
        out.append(str(k_cluster))
        out.append(str(num_iter))
        out.append(str(elapsed_time))
        out.append(str(wsse))
        out.append(str(bsse))
        out.append(str(total_sse))
        out.append(str(wsse/total_sse*100))
        csvwriter.writerow(out)


#================================================================================================================
# Get input from user and validate before running program

#Step 1: Get To number cluster to evaluate. Program will run from 1 to k input
print("Enter options to generate WSS accordingly")
message = "To k-cluster inclusive(input integer from 1 to 440): "
to_num_cluster = validate_input.validate_int_in_range_inc(1, 440, message)

#Step 2: Method for normalization: MinMax(0,1) or Zscore
normalization_dict = {"Z": "Zscore", "M": "MinMax"}
valid_input_method_bool = False
while not valid_input_method_bool:
    input_str_norm = input("Normalization method(Z for Zscore, M for MinMax[0,1]): ").upper()
    if input_str_norm == "Z":
        norm_method = normalization_dict.get(input_str_norm)
        valid_input_method_bool = True
    elif input_str_norm == "M":
        norm_method = normalization_dict.get(input_str_norm)
        valid_input_method_bool = True
    else:
        print("Bad input, it must be Z or M")
print("You chose method {} for Normalization".format(norm_method))

#Step 3: Option for initial centroids
inital_centroids_dict = {"P": "Partition", "A": "Actual"}
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

# Calling the method to run
eval_enhance_kmeans(to_num_cluster,norm_method, option_initial_centroids)


"""
to_num_cluster = 15
norm_method = "MinMax"
option_initial_centroids = "Partition"
eval_enhance_kmeans(to_num_cluster,norm_method, option_initial_centroids)
"""
