# -*- coding: utf-8 -*-
"""
Created on mar feb  9 16:29:49 ART 2016
@author: asoreyh

Produce a file with the distribution of distances between two points in a
metric or interpolated altitude file. 

usage: python2 dist.py [base-file.or*]
"""

import math
import sys

class point(object):
    def __init__(self,lista):
        self.x=[]
        for xi in lista:
            self.x.append(float(xi))
        self.dim=len(self.x)

def distance(a,b):
    d=0.
    for k in range(a.dim):
       d += (a.x[k] - b.x[k])**2
    return math.sqrt(d)

points = []

print "Reading file..."
f=open(sys.argv[1],"r")
for a in f:
    if ((a.strip()).startswith("#")):
        continue
    b=point(a.split())
    if not b.dim:
        continue
    points.append(b)
f.close()
# points is a list of objects class points that contains coordinates and heights

# calculate distances
dist=[];
l=len(points)
print "Calculating distances..."
for i in range(l):
    for j in range(i+1,l):
        dist.append(distance(points[i],points[j]))
    print "%d/%d"%(i,l)

dn=len(dist)
res=70.
hist = [0] * (int(max(dist)/res)+1)

print "Creating histogram..."
for x in dist:
    hist[int(x/res)]+=1
print "Printing histogram..."
f=open("out.hst","w")
for i in range(len(hist)):
    f.write("%d %d %.7e\n"%(i*res, hist[i], 1.*hist[i]/dn))
f.close()
print "Done."

