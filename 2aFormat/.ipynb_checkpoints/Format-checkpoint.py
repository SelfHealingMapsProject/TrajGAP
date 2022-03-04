import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Proj, transform
import pylab as p
import math
import random
from scipy import stats
import csv
from itertools import islice
from shapely.geometry import Point, mapping
from fiona import collection
from fiona.crs import from_epsg
import geopandas as gpd
from astropy.wcs.docstrings import row
from geopandas.geodataframe import GeoDataFrame
from collections import Counter

def reproject(fromssid,tossid,x,y):
    inProj = Proj(init=fromssid)
    outProj = Proj(init=tossid)
    x1,y1 = x,y
    x2,y2 = transform(inProj,outProj,x1,y1)
    return x2,y2


def formatPoint():
    inputFile = open('input.csv', "r")
    reader = csv.reader(inputFile)
    
    outputTraj = open('output.csv', "w", newline='')
    writer = csv.writer(outputTraj, delimiter = ',')
    writer.writerow(["deviceID","sessionID","time","lat","long","sessionStart","sessionEnd","gapStart","gapEnd","timeDiff","x","y","distDiff"])
    
    next(reader)#skip the first line in original csv file, which is the column label
    prevrow = next(reader)#skip the first row of data
    sessionStart = True
    sessionEnd = False
    gapStart = None
    gapEnd = None
    prevx = None
    prevy = None
    
    for row in reader:
        if row[4]==prevrow[4]:
            if (float(row[6])>3):
                gapStart = "3min"
            elif (float(row[6])>1):
                gapStart = "1min"
            elif (float(row[6])>(10/60)):
                gapStart = "10s"
        else:
            sessionEnd = True
        # get local projection coordinates
        xx,yy = reproject('epsg:4326','epsg:3111',prevrow[3],prevrow[2])
        distDiff = None
        if(sessionStart == False and prevx != None and prevy!= None):
            distDiff = np.sqrt(pow((xx-prevx),2)+pow((yy-prevy),2))
        writer.writerow([prevrow[5],prevrow[4],prevrow[1],prevrow[2],prevrow[3],sessionStart,sessionEnd,gapStart,gapEnd,prevrow[6],xx,yy,distDiff])
        prevx = xx
        prevy = yy
        gapEnd = None
        sessionStart = False
        if sessionEnd == True:
            sessionStart = True
            sessionEnd =False
        if gapStart!=None:
            gapEnd = gapStart
            gapStart=None
        prevrow = row
    xx,yy = reproject('epsg:4326','epsg:3111',prevrow[3],prevrow[2])
    distDiff = None
    if(sessionStart == False and prevx != None and prevy!= None):
        distDiff = np.sqrt(pow((xx-prevx),2)+pow((yy-prevy),2))
    writer.writerow([prevrow[5],prevrow[4],prevrow[1],prevrow[2],prevrow[3],sessionStart,sessionEnd,gapStart,gapEnd,prevrow[6],xx,yy,distDiff])
    
    inputFile.close()
    outputTraj.close()
    return

formatPoint()