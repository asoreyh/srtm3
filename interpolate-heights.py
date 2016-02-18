# -*- coding: utf-8 -*-
"""
Created  on Sun Jun  9 14:40:28 COT 2013
Modified on Thu Apr  3 15:59:52 COT 2014
Modified on Mar Feb  9 10:31:03 ART 2016
@author: asoreyh

Produce an interpolated altitude file from parsed data of STRMv3 
mission. To obtain and process data see parsehgt.py

usage:
    python2 interpolate-heights.py original-heights-data.dat lat0 lon0  distance np output_base_name

produces:
    output_base_name.ord: data extracted from original file in Lat,Lon,Alt, centered at lat0,lon0
    output_base_name.orm: data extracted from original file and converted to meters. centered at lat0,lon0 
    output_base_name.itp: interpolated data in a grid of +/- distance meters in each direction, having np points in each direction 
"""

import math
import sys
import numpy as np
from scipy import interpolate as ip

# file name with altitudes read as argument
# grid, interpreted as a matrix: x is for rows(index j), and y is for columns (index i)
# units: meters

xmax=int(sys.argv[4])
xmin=-xmax
nx=int(sys.argv[5])  # number of points for x
#and then dx=(xmax-xmin)/nx

ymax=xmax
ymin=xmin
ny=nx # number of points for y
#and then dy=(ymax-ymin)/ny

file0=sys.argv[1]
lat0d=float(sys.argv[2])
lon0d=float(sys.argv[3])
file1=sys.argv[6]

lat0=math.radians(lat0d)
lon0=math.radians(lon0d)

### no need to change anything below this point ###

# max dist to include points for interpolation, should be greater than max (or min) values for x or y
maxdist=0.
tmp=[xmax,xmin,ymax,ymin]
tmpx=abs(max(tmp))
tmpn=abs(min(tmp))
maxdist=2.*(tmpx if tmpx > tmpn else tmpn)

dearth=12742018.
clat0=math.cos(lat0)

def haversine(rads):
    return ((1.-math.cos(rads))/2.)
    
def dist(lat,lon):
    dlat=lat-lat0
    dlon=lon-lon0
    aux0=math.cos(lat)*clat0
    aux1=math.sqrt(haversine(dlat)+aux0*haversine(dlon))
    return (dearth*math.asin(aux1))

points=[]
values=[]
coords=[]
for line in open(file0):
  row=line.split()
  if (len(row)<3):
    continue

  alt=float(row[2])
  if (alt<-10000):
      continue
  lat=math.radians(float(row[0]))
  lon=math.radians(float(row[1]))
  dr=dist(lat,lon)
  if (dr<maxdist):
    dx=dist(lat0,lon)*((lon-lon0)/math.fabs(lon-lon0))
    dy=dist(lat,lon0)*((lat-lat0)/math.fabs(lat-lat0))
    coords.append([math.degrees(lat),math.degrees(lon)])
    points.append([dx,dy])
    values.append(alt)

grid_x, grid_y = np.mgrid[xmin:xmax:nx*1j, ymin:ymax:ny*1j]
grid=ip.griddata(points,values, (grid_x,grid_y), method='cubic')

# printing interpolated data
f=open(file1+".itp", 'w')
f.write("#Original file: "+file0+"\n")
f.write("#Center located at: Lat %.7f, Lon: %.7f\n"%(lat0d,lon0d))
f.write("#Grid on X direction: (%.1f,%.1f,%d), one point every %.2f m \n"%(xmin,xmax,nx,abs(1.0*(xmax-xmin)/nx)))
f.write("#Grid on Y direction: (%.1f,%.1f,%d), one point every %.2f m \n"%(ymin,ymax,ny,abs(1.0*(ymax-ymin)/ny)))
f.write("#North-South(m) #West-East(m) #Altitude(m)\n")
for i in range(0,ny):
  for j in range(0,nx):
    output="%.2f %.2f %.1f\n" % (grid_x[j][i],grid_y[j][i],grid[j][i])
    f.write(output)
  f.write("\n")
f.close()

# original values in this region
pp=points[0][0]
f=open(file1+".orm", 'w')
f.write("#Original file: "+file0+"\n")
f.write("#Center located at: Lat %.7f, Lon: %.7f\n"%(lat0d,lon0d))
f.write("#Grid on X direction: (%.1f,%.1f,%d), one point every %.2f m \n"%(xmin,xmax,nx,abs(1.0*(xmax-xmin)/nx)))
f.write("#Grid on Y direction: (%.1f,%.1f,%d), one point every %.2f m \n"%(ymin,ymax,ny,abs(1.0*(ymax-ymin)/ny)))
f.write("#North-South(m) #West-East(m) #Altitude(m)\n")

g=open(file1+".ord", 'w')
g.write("#Original file: "+file0+"\n")
g.write("#Center located at: Lat %.7f, Lon: %.7f\n"%(lat0d,lon0d))
g.write("#Grid on X direction: (%.1f,%.1f,%d), one point every %.2f m \n"%(xmin,xmax,nx,abs(1.0*(xmax-xmin)/nx)))
g.write("#Grid on Y direction: (%.1f,%.1f,%d), one point every %.2f m \n"%(ymin,ymax,ny,abs(1.0*(ymax-ymin)/ny)))
g.write("#North-South(deg) #West-East(deg) #Altitude(m)\n")

for i in range(1,len(values)):
  if (points[i][0]>xmin and points[i][0]<xmax):
    if (points[i][1]>ymin and points[i][1]<ymax):
      if (pp>0 and points[i][0]<0):
        f.write("\n")
        g.write("\n")
      output="%.2f %.2f %.1f\n" % (points[i][0], points[i][1], values[i])
      f.write(output)
      output="%.7f %.7f %.1f\n" % (coords[i][0], coords[i][1], values[i])
      g.write(output)
      pp=points[i][0]
f.close()
g.close()
