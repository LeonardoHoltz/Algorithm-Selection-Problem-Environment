#!/usr/bin/python

import sys
import csv
import math
import os
import numpy as np
import graham_scan
import cluster_points

def distanceTwoTasks(task1, task2):
    dx = task1.x - task2.x
    dy = task1.y - task2.y
    return math.sqrt(dx**2 + dy**2)

def isInside(x, y, poly):
    n = len(poly)
    inside = False
    p2x = 0.0
    p2y = 0.0
    xints = 0.0
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def polygonArea(polygon):
    j = len(polygon) - 1
    area = 0
    # Shoelace formula:
    for i in range(len(polygon)):
        area += (polygon[j][0] + polygon[i][0]) * (polygon[j][1] - polygon[i][1])
        j = i # j is previous vertex to i
    
    return abs(area/2)

class Task:
    def __init__(self, ID, x, y, earliestTime, latestTime, pickupID, deliveryID):
        self.taskID = ID
        self.x = x
        self.y = y
        self.earliestTime = earliestTime
        self.latestTime = latestTime
        self.pickupID = pickupID        # If the pickupID is zero, it means that the task itself is a pickup point
        self.deliveryID = deliveryID    # If the deliveryID is zero, it means that the task itself is a delivery point
        # If both the pickup and delivery IDs are zero, it means that the task is the depot


features_list = ["instance", "avgDistance", "minDistance", "maxDistance", "stdDeviation", "distanceMedian", 
                    "depotTask-x", "depotTask-y", "N_Tasks", "convex_hull_points", "convex_hull_length", 
                    "points_inside_hull", "convex_hull_area", "average_timespan", "std_deviation_timespan", 
                    "highest_last_time", "highest_early_time", "lowest_last_time", "lowest_early_time",
                    "Q1_early_time", "Q2_early_time", "Q3_early_time", "Q1_late_time", "Q2_late_time", "Q3_late_time",
                    "n_clusters", "avg_clusterSize"]

with open("features.csv", "w", newline='') as features_file:
    wr = csv.writer(features_file, dialect='excel')
    wr.writerow(features_list)
features_file.close()

instances_names_file = sys.argv[1]
inst_file = open(instances_names_file, "r")
inst_file_lines = inst_file.readlines()
directory = "instances/all/"

for inst_line in inst_file_lines:
    inst_line = inst_line[:-1]
    if not inst_line.startswith("#") and inst_line.endswith(".txt"):
        file_name = inst_line
        print(file_name)
        file = open(directory + file_name, "r")

        first_line = file.readline()

        # Getting the vehicles and capacity by the first line:

        first_line = first_line.split("\t")

        vehicles = int(first_line[0])
        capacity = int(first_line[1])

        # Reading of the tasks:

        pickupTasks = {}
        pickupIDs = []
        deliveryTasks = {}
        deliveryIDs = []
        depotTask = None

        lines = file.readlines()
        N_Tasks = len(lines)
        for line in lines:
            line = line.split("\t")
            line = list(map(int, line))
            task = Task(line[0], line[1], line[2], line[4], line[5], line[7], line[8])
            if task.pickupID == 0 and task.deliveryID == 0:
                depotTask = task
            else:
                if task.pickupID == 0:
                    pickupTasks[task.taskID] = task
                    pickupIDs.append(task.taskID)
                else:
                    deliveryTasks[task.taskID] = task
                    deliveryIDs.append(task.taskID)

        file.close()

        # Start of the features extraction:

        features_list = [file_name]

        # Average Distance, Min Distance & Max Distance:

        totalDistance = 0
        distances = []
        minDistance = float('inf')
        maxDistance = float('-inf')

        for ID in pickupIDs:
            task1 = pickupTasks[ID]
            task2 = deliveryTasks[pickupTasks[ID].deliveryID]
            distance = distanceTwoTasks(task1, task2)
            if distance > maxDistance:
                maxDistance = distance
            elif distance < minDistance:
                minDistance = distance
            totalDistance += distance
            distances.append(distance)

        avgDistance = totalDistance / (N_Tasks / 2)

        features_list.append(avgDistance)
        features_list.append(minDistance)
        features_list.append(maxDistance)

        # Standard Deviation of the Distance:

        soma = 0
        for distance in distances:
            soma = (distance - avgDistance) ** 2

        stdDeviation = math.sqrt(soma/(N_Tasks / 2))
        features_list.append(stdDeviation)

        # Median Distance:

        distances.sort()
        if len(distances) % 2 == 0:
            distanceMedian = (distances[math.floor(len(distances)/2)] + distances[math.floor(len(distances)/2 - 1)]) / 2 # 2 e 3 de 6
        else:
            distanceMedian = distances[math.floor(len(distances)/2)]

        features_list.append(distanceMedian)

        # Initial Point

        features_list.append(depotTask.x)
        features_list.append(depotTask.y)

        # Total Amount of Points

        features_list.append(N_Tasks)

        # Convex Hull

        # List with all points:
        points = []
        points.append((depotTask.x, depotTask.y))
        for pickup_id in pickupIDs:
            points.append((pickupTasks[pickup_id].x, pickupTasks[pickup_id].y))
        for delivery_id in deliveryIDs:
            points.append((deliveryTasks[delivery_id].x, deliveryTasks[delivery_id].y))

        convex_hull = graham_scan.grahamScan(points)

        # Total Amount of Points in the Convex Hull

        convex_hull_points = len(convex_hull)

        features_list.append(convex_hull_points)

        # Convex Hull Length

        convex_hull_length = 0
        for i in range(len(convex_hull)-1):
            convex_hull_length += graham_scan.distance(convex_hull[i], convex_hull[i+1])
        convex_hull_length += graham_scan.distance(convex_hull[-1], convex_hull[0])

        features_list.append(convex_hull_length)

        # Total Amount of Points inside the Convex Hull

        points_inside_hull = 0
        for pickup_id in pickupIDs:
            if(isInside(pickupTasks[pickup_id].x, pickupTasks[pickup_id].x, convex_hull)):
                points_inside_hull += 1
        for delivery_id in deliveryIDs:
            if(isInside(deliveryTasks[delivery_id].x, deliveryTasks[delivery_id].x, convex_hull)):
                points_inside_hull += 1

        features_list.append(points_inside_hull)

        # Convex Hull Area

        convex_hull_area = polygonArea(convex_hull)

        features_list.append(convex_hull_area)

        # Average timespan 
        pickupIDs_timespan = [(pickupTasks[i].latestTime - pickupTasks[i].earliestTime) for i in pickupIDs]
        deliveryIDs_timespan = [(deliveryTasks[i].latestTime - deliveryTasks[i].earliestTime) for i in deliveryIDs]
        IDs_timespan = np.array(pickupIDs_timespan + deliveryIDs_timespan)

        features_list.append(np.average(IDs_timespan))

        # Standar deviation timespan
        features_list.append(np.std(IDs_timespan))

        # High/Low time information
        early_time = np.array([pickupTasks[i].earliestTime for i in pickupIDs] + [deliveryTasks[i].earliestTime for i in deliveryIDs])
        late_time  = np.array([pickupTasks[i].latestTime   for i in pickupIDs] + [deliveryTasks[i].latestTime   for i in deliveryIDs])
            # Highest last time
        features_list.append(np.max(late_time))
            # Highest early time
        features_list.append(np.max(early_time))
        
            # Lowest last time
        features_list.append(np.min(late_time))
            # Lowest early time
        features_list.append(np.min(early_time))

        # Quantile&Median early time
        features_list.append(np.quantile(early_time, q=0.25))
        features_list.append(np.quantile(early_time, q=0.50)) # same as median
        features_list.append(np.quantile(early_time, q=0.75))

        # Quantile&Median late time
        features_list.append(np.quantile(late_time, q=0.25))
        features_list.append(np.quantile(late_time, q=0.50)) # same as median
        features_list.append(np.quantile(late_time, q=0.75))

        # Clusters of data
        if (file_name.lower().startswith("lc") or file_name.lower().startswith("lrc")): # currently working only for li&lim
            xy_data = [[float(pickupTasks[i].x), float(pickupTasks[i].y)] for i in pickupIDs] + [[float(deliveryTasks[i].x), float(deliveryTasks[i].y)] for i in deliveryIDs]
            xy_data = np.array(xy_data)
            n_clusters, avg_size_cluster = cluster_points.number_clusters(xy_data)
            features_list.append(n_clusters)
            features_list.append(avg_size_cluster)
        else:
            features_list.append(1)
            features_list.append(len(pickupIDs)+len(deliveryIDs))
        
        # Insertion of the features in the CSV file

        with open("features.csv", "a", newline='') as features_file:
            #wr = csv.writer(features_file, dialect='excel')
            wr = csv.writer(features_file)
            wr.writerow(features_list)
        features_file.close()

inst_file.close()
