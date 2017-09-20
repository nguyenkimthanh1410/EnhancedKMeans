import csv

#=================================== WRITE OUT THE RESULT OF CLUSTER TO CSV FILE =======================================
# Input: a list of list
def write_detail_result_to_file(cluster_list_denorm, option_normalization, option_initial_centroids):
    print("Start writing detail of points in clusters to file")
    number_cluster = len(cluster_list_denorm)
    file_name_str = "{}clusters_detail_{}_{}.csv".format(str(number_cluster), option_normalization, option_initial_centroids)

    a_file = open(file_name_str, "w")
    csvwriter = csv.writer(a_file, delimiter=' ',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)

    csvwriter.writerow(["OUTPUT DETAIL OBSERVATIONS ASSIGNED TO CLUSTERS:\n\
                    Normalization method: {}\n\
                    Initial centroids: {}".format(option_normalization, option_initial_centroids)])

    csvwriter.writerow(["Fresh", "Milk", "Grocery", "Frozen", "Detergents_Paper", "Delicassen", "Cluster#"])
    count_cluster = 0
    for a_cluster in cluster_list_denorm:
        for a_point in a_cluster: #Never append to a_point (as it's object reference)
            output_row = []
            output_row.extend(a_point) #extend, not append
            output_row.extend([count_cluster]) # append because
            csvwriter.writerow(output_row)
        count_cluster +=1
    print("Successful writting details to a file")


def write_summary_result_to_file(cluster_list_denorm, num_observations, \
                                 initial_k_midpoint, num_iteration, elapsed_time, wsse,\
                                 bsse, option_normalization, option_initial_centroids):

    print("Start writing a summary of clustering result")

    number_cluster = len(cluster_list_denorm)
    file_name_str = "{}clusters_summary_{}_{}.csv".format(str(number_cluster), option_normalization,
                                                     option_initial_centroids)
    a_file = open(file_name_str, "w")

    csvwriter = csv.writer(a_file, delimiter=' ',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)

    #Write initial_k_midpoint
    csvwriter.writerow(["OUTPUT SUMMARY with options:\n\
                Normalization method: {}\n\
                Initial centroids: {}".format(option_normalization, option_initial_centroids)])
    csvwriter.writerow(["Initial {} midpoints".format(len(initial_k_midpoint))])
    csvwriter.writerow(["Fresh", "Milk", "Grocery", "Frozen", "Detergents_Paper", "Delicassen", "Cluster#"])

    count_k = 0
    for point in initial_k_midpoint:
        text = []
        text.extend(point)
        text.extend([count_k])
        csvwriter.writerow(text)
        count_k +=1

    # Write out midpoint for each cluster, Cluster#, #Points in cluster
    csvwriter.writerow(["Final midpoints"])
    csvwriter.writerow(["Fresh", "Milk", "Grocery", "Frozen", "Detergents_Paper", "Delicassen", "Cluster#", "#Points", "%"])
    for i in range(len(cluster_list_denorm)):
        output_row = []
        midpoint = initial_k_midpoint[i]
        output_row.extend(midpoint) #extend, not append
        output_row.extend([i])

        num_points = len(cluster_list_denorm[i])
        output_row.extend([num_points])

        percent = "{:5.2%}".format(num_points/num_observations)
        output_row.extend([percent])

        csvwriter.writerow(output_row)

    # Write out iteration and running time
    csvwriter.writerow(["Number of iteration: {}".format(num_iteration)])
    csvwriter.writerow(["Elapsed Time: {} seconds".format(elapsed_time)])

    # Write out Square Error
    csvwriter.writerow(["Square Error"])
    csvwriter.writerow(["Within Sum Square Error (WSSE): ", str(wsse)])
    csvwriter.writerow(["Between Sum Square Error (BSSE): ", str(bsse)])
    total_sse = wsse +bsse
    csvwriter.writerow(["Total Sum Square Error (SSE): ", str(total_sse)])
    print("Successful writting a summary of clustering result in file")