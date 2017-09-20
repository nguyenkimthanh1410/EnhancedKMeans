import numpy as np

# Purpose: Holding midpoint, and list of points belongs to this cluster
# Midpoint should be: list of floats

class Cluster:
    def __init__(self, midpoint):
        self.midpoint = midpoint
        self.cluster_point_list = []

    def __str__(self):
        return "Current_midpoint= " + str(self.midpoint) + \
               "\nNumber of points= " + str(len(self.cluster_point_list)) + \
               "\nMembers of clusters: " + str(self.cluster_point_list)

    def get_midpoint(self):
        return self.midpoint

    def get_cluster_point_list(self):
        return self.cluster_point_list

    def add_point_to_cluster_point_list(self, new_point):
        self.cluster_point_list.append(new_point)

    def recalculate_midpoint(self):
        midpoint_temp = self.midpoint
        np_array_temp = np.array(self.cluster_point_list)
        np_array_midpoint = np.mean(np_array_temp, axis=0)
        return np_array_midpoint.tolist()