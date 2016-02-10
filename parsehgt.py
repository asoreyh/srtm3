# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 14:40:28 2013
Modified on Thu Apr  3 15:59:52 COT 2014
Modified on mar feb  9 09:51:49 ART 2016
@author: asoreyh

Produce .dat ASCII files of SRTMv3 data from the original .hgt files. 
Files are availables at https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/

usage: python2 parsehgt.py [files-to-convert (space separated)]
"""

import struct
import sys
        
class srtmParser(object):
    def __init__(self):
        self.north=1.
        self.east=1.
        self.lat = 0.
        self.lon =0.

    def parseFile(self,filename):
        # read 1,442,401 (1201x1201) high-endian
        # signed 16-bit words into self.               
        if (filename[0]=="S"):
          self.north=-1.
        if (filename[3]=="W"):
          self.east=-1.        
        self.lat=self.north*float(filename[1:3])
        self.lon=self.east*float(filename[4:7])
        fi=open(filename,"rb")
        contents=fi.read()
        fi.close()
        self.z=struct.unpack(">1442401h", contents)
        
    def writeCSV(self,filename):
        if self.z:
            fo=open(filename,"w")
            lat=0.
            lon=0.
            for row in range(0,1201):
                offset=row*1201
                thisrow=self.z[offset:offset+1201]
                col=0
                lat=(self.lat+1)-row/1201. # top left cell is lat+1,lon
                for z in thisrow:
                    lon=self.lon+col/1201.
                    if (z>-1000):
                      fo.write("{0} {1} {2}\n".format(lat,lon,z))
                    col+=1
                fo.write("\n")
            fo.close()
        else:
            return None

if __name__ == '__main__':
    a=len(sys.argv)
    if (a<2):
        print "No .hgt files provided. Try python2 parsehgt.py [files-to-analize]"
        sys.exit(1)
    f = srtmParser()
    for i in range(1,a):
        fn=sys.argv[i]
        print "Opening %s file..."%(fn),
        f.parseFile(fn)
        print "Done.\nConverting to ASCII...",
        nn=fn.rstrip('.hgt')+".dat"
        f.writeCSV(nn)
        print "Done.\n%s is ready for interpolation"%(nn)
