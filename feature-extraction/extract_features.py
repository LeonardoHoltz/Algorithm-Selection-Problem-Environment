#!/usr/bin/python

import sys
import math
import graham_scan

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


file_name = sys.argv[1]
file = open(file_name, "r")

first_line = file.readline()

# Getting the vehicles and capacity by the first line:

print(first_line)
first_line = first_line.split("\t")

vehicles = int(first_line[0])
capacity = int(first_line[1])

# Reading of the tasks:

pickupTasks = {}
pickupIDs = []
deliveryTasks = {}
deliveryIDs = []
depotTask = None

lines = file.readlines()[0:]
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

# Start of the features extraction:

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

# Standard Deviation:

soma = 0
for distance in distances:
    soma = (distance - avgDistance) ** 2

stdDeviation = math.sqrt(soma/(N_Tasks / 2))

# Median:

distances.sort()
if len(distances) % 2 == 0:
    median = (distances[len(distances)/2] + distances[len(distances)/2 - 1]) / 2
else:
    median = distances[math.floor(len(distances)/2)]

# Initial Point

#depotTask.x
#depotTask.y

# Total Amount of Points

#N_Tasks

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

len(convex_hull)

# Convex Hull Length

convex_hull_lenght = 0
for i in range(len(convex_hull)-1):
    convex_hull_lenght += graham_scan.distance(convex_hull[i], convex_hull[i+1])
convex_hull_lenght += graham_scan.distance(convex_hull[-1], convex_hull[0])

# Total Amount of Points inside the Convex Hull

points_inside_hull = 0
for pickup_id in pickupIDs:
    if(isInside(pickupTasks[pickup_id].x, pickupTasks[pickup_id].x, convex_hull)):
        points_inside_hull += 1
for delivery_id in deliveryIDs:
    if(isInside(deliveryTasks[delivery_id].x, deliveryTasks[delivery_id].x, convex_hull)):
        points_inside_hull += 1

# Convex Hull Area

convex_hull_area = polygonArea(convex_hull)

