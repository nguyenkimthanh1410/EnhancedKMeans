import csv
import numpy as np

# Purpose: Read data from file into list of points.
# Remove unwanted attributes and normalize leftover

#==============Pre-Process data from csv file=====================================

# Point class is used to hold data read from file,
# REMOVED unwanted attributes, NOT YET normalized
class Point:
    def __init__(self, row_list): #row_list: list of string, with attributes needed
        self.point = np.float_(np.array(row_list)).tolist()

    def __str__(self):
        return str(self.point)

    def get_dimension(self):
        return self.point


# Task 1: Process file, get attributes needed, store points into all_point_list,
'''
    Note: explicitly put list into parameter of function: pass object reference whose object is mutable
'''
def remove_unwanted_attributes(list_points_removed_unwanted_attributes, file_object, num_attributes_unwanted):
    reader = csv.reader(file_object)
    for row in reader: # each row is a list of string already
        if (not row[0].isalpha()): # Remove heading
            lefover = row[num_attributes_unwanted:]
            #print("leftover: ", lefover)
            a_point = Point(lefover).get_dimension()
            list_points_removed_unwanted_attributes.append(a_point)
    return list_points_removed_unwanted_attributes

#==============Pre-Process data from csv file=====================================