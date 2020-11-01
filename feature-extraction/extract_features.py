#!/usr/bin/python

import sys
import math

def distanceTwoTasks(task1, task2):
    dx = task1.x - task2.x
    dy = task1.y - task2.y
    return math.sqrt(dx**2 + dy**2)

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

lines = file.readlines()[1:]
N_Tasks = len(lines)
for line in lines:
    line = line.split("\t")
    line = list(map(int, line))
    task = Task(line[0], line[1], line[2], line[4], line[5], line[7], line[8])
    if task.pickupID == 0 and task.deliveryID == 0:
        depot_task = task
    else:
        if task.pickupID == 0:
            pickupTasks[task.taskID] = task
            pickupIDs.append(task.taskID)
        else:
            deliveryTasks[task.taskID] = task
            deliveryIDs.append(task.taskID)

# Start of the features retrieving:

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

print("Max Distance:", maxDistance)
print("Min Distance:", minDistance)
print("Average Distance:", avgDistance)
print("Standart Deviation:", stdDeviation)
print("Median:", median)
