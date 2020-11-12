#!/usr/bin/python

import sys

clusters_name_file = sys.argv[1]
clusters_file = open(clusters_name_file, "r")
current_cluster = None
for line in clusters_file:
	line = line.split(",")
	line[1] = line[1][:-1]
	if current_cluster == None or line[1] != current_cluster:
		if current_cluster != None:
			current_cluster_file.close()
		current_cluster = line[1]
		current_cluster_file = open("cluster" + current_cluster + ".txt", "a")
		current_cluster_file.write(line[0] + "\n")
	else:
		current_cluster_file.write(line[0] + "\n")

current_cluster_file.close()
clusters_file.close()
