import random
from random import randint
from math import atan2 # for computing polar angle
from math import sqrt

# Polar angle (radians) of two points
def polar_angle(p0,p1=None):
	if p1 == None: p1 = initial_point
	y_span = p0[1] - p1[1]
	x_span = p0[0] - p1[0]
	return atan2(y_span,x_span)


# Euclidean distance of two points
def distance(p0, p1 = None):
	if p1 == None: p1 = initial_point
	y_span = p0[1] - p1[1]
	x_span = p0[0] - p1[0]
	return sqrt(y_span**2 + x_span**2)


# 3x3 matrix determinant
def det(p1,p2,p3):
	return   (p2[0]-p1[0])*(p3[1]-p1[1]) \
			-(p2[1]-p1[1])*(p3[0]-p1[0])


# Sort by increasing polar angle from the initial point.
def quicksortPolar(a):
	if len(a)<=1: return a
	smaller,equal,larger=[],[],[]
	piv_ang = polar_angle(a[randint(0,len(a)-1)]) # select random pivot
	for pt in a:
		pt_ang = polar_angle(pt) # calculate current point angle
		if   pt_ang < piv_ang:  smaller.append(pt)
		elif pt_ang == piv_ang: equal.append(pt)
		else: 				  larger.append(pt)
	return   quicksortPolar(smaller) \
			+sorted(equal,key=distance) \
			+quicksortPolar(larger)


def grahamScan(points):

    global initial_point

    # Select the point with the lowest y value, if there's more than 1 point, select with the lowest x value
    initial_point = None
    for point in points:
        if initial_point == None:
            initial_point = point
        if point[1] <= initial_point[1]:
            if point[1] == initial_point[1]:
                if point[0] < initial_point[0]:
                    initial_point = point
            else:
                initial_point = point

	# sort the points by polar angle then delete initial point
    sorted_pts = quicksortPolar(points)
    del sorted_pts[sorted_pts.index(initial_point)]

	# start the hull
    hull = [initial_point, sorted_pts[0]]

    for point in sorted_pts[1:]:
        while det(hull[-2], hull[-1], point) <= 0:
            del hull[-1]
            if len(hull)<2: break
        hull.append(point)

    return hull

initial_point = None