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

def getCategory(distB,distG,distA,threshold):
    definedClass = ""
    distB = float(distB)
    distA = float(distA)
    distG = float(distG)
    if  (distB>threshold and distG>threshold and distA>threshold):
        definedClass = "MMM"
    elif (distB>threshold and distG>threshold and distA<=threshold):
        definedClass = "MMN"
    elif (distB>threshold and distG<=threshold and distA>threshold):
        definedClass = "MNM"
    elif(distB>threshold and distG<=threshold and distA<=threshold):
        definedClass = "MNN"
    elif(distB<=threshold and distG>threshold and distA>threshold):
        definedClass = "NMM"
    elif(distB<=threshold and distG>threshold and distA<=threshold):
        definedClass = "NMN"
    elif(distB<=threshold and distG<=threshold and distA>threshold):
        definedClass = "NNM"
    elif(distB<=threshold and distG<=threshold and distA<=threshold):
        definedClass = "NNN"
    return definedClass

def sessionClass(threshold = 200):
    inputFile = open('trajInput.csv', "r")
    reader = csv.reader(inputFile)
    
    session = pd.read_csv("sessionInput.csv")
    session["distBf"] = None #this is euclidean dist
    session["distGap"] = None
    session["distAf"] = None
    session["timeBf"] = None
    session["timeGap"] = None
    session["timeAf"] = None
    session["sessionStartX"] = None
    session["sessionStartY"] = None
    session["sessionEndX"] = None
    session["sessionEndY"] = None
    session["totalDist"] = None #this is cumulative dist
    session["category"] = None
    
    next(reader)#skip the first line in original csv file, which is the column label
    prevRow = None
    startRow = None
    gapStartRow = None
    gapEndRow = None
    totalDist = 0
    for row in reader:
        if (startRow == None):
            startRow = row
            print(row)
            print(row[7])
            if (row[7]=="3min"):
                gapStartRow = row
        elif (row[1]==startRow[1]):
            totalDist = totalDist+float(row[12])
            if (row[8]=="3min"):
                gapEndRow = row
            elif (row[7]=="3min"):
                gapStartRow = row
        else:
            
            endRow = prevRow
            
            if (gapStartRow):
                distB = np.sqrt(pow((float(startRow[10])-float(gapStartRow[10])),2)+pow((float(startRow[11])-float(gapStartRow[11])),2))
                distG = gapEndRow[12]
                distA = np.sqrt(pow((float(endRow[10])-float(gapEndRow[10])),2)+pow((float(endRow[11])-float(gapEndRow[11])),2))
                timeB = (pd.to_datetime(gapStartRow[2])-pd.to_datetime(startRow[2]))/np.timedelta64(1,'m')
                timeG = gapEndRow[9]
                timeA = (pd.to_datetime(endRow[2])-pd.to_datetime(gapEndRow[2]))/np.timedelta64(1,'m')
                startX = startRow[10]
                startY = startRow[11]
                endX = endRow[10]
                endY = endRow[11]
                Sid = startRow[1]
                definedClass = getCategory(distB,distG,distA,threshold)
                session.loc[(session["sessionID"]==Sid),"distBf"]=distB
                session.loc[(session["sessionID"]==Sid),"distGap"]=distG
                session.loc[(session["sessionID"]==Sid),"distAf"]=distA
                session.loc[(session["sessionID"]==Sid),"timeBf"]=timeB
                session.loc[(session["sessionID"]==Sid),"timeGap"]=timeG
                session.loc[(session["sessionID"]==Sid),"timeAf"]=timeA
                session.loc[(session["sessionID"]==Sid),"sessionStartX"]=startX
                session.loc[(session["sessionID"]==Sid),"sessionStartY"]=startY
                session.loc[(session["sessionID"]==Sid),"sessionEndX"]=endX
                session.loc[(session["sessionID"]==Sid),"sessionEndY"]=endY
                session.loc[(session["sessionID"]==Sid),"totalDist"]=totalDist
                session.loc[(session["sessionID"]==Sid),"category"]=definedClass
            gapStartRow = None
            gapEndRow = None
            startRow = row
            if (row[7]=="3min"):
                gapStartRow = row
            totalDist=0
        
        prevRow = row
    
    endRow = prevRow
    if (gapStartRow):
        distB = np.sqrt(pow((float(startRow[10])-float(gapStartRow[10])),2)+pow((float(startRow[11])-float(gapStartRow[11])),2))
        distG = gapEndRow[12]
        distA = np.sqrt(pow((float(endRow[10])-float(gapEndRow[10])),2)+pow((float(endRow[11])-float(gapEndRow[11])),2))
        timeB = (pd.to_datetime(gapStartRow[2])-pd.to_datetime(startRow[2]))/np.timedelta64(1,'m')
        timeG = gapEndRow[9]
        timeA = (pd.to_datetime(endRow[2])-pd.to_datetime(gapEndRow[2]))/np.timedelta64(1,'m')
        startX = startRow[10]
        startY = startRow[11]
        endX = endRow[10]
        endY = endRow[11]
        Sid = startRow[1]
        definedClass = getCategory(distB,distG,distA,threshold)
        session.loc[(session["sessionID"]==Sid),"distBf"]=distB
        session.loc[(session["sessionID"]==Sid),"distGap"]=distG
        session.loc[(session["sessionID"]==Sid),"distAf"]=distA
        session.loc[(session["sessionID"]==Sid),"timeBf"]=timeB
        session.loc[(session["sessionID"]==Sid),"timeGap"]=timeG
        session.loc[(session["sessionID"]==Sid),"timeAf"]=timeA
        session.loc[(session["sessionID"]==Sid),"sessionStartX"]=startX
        session.loc[(session["sessionID"]==Sid),"sessionStartY"]=startY
        session.loc[(session["sessionID"]==Sid),"sessionEndX"]=endX
        session.loc[(session["sessionID"]==Sid),"sessionEndY"]=endY
        session.loc[(session["sessionID"]==Sid),"totalDist"]=totalDist
        session.loc[(session["sessionID"]==Sid),"category"]=definedClass
    inputFile.close()
    session = session.drop(['sessionStartLat','sessionStartLong','sessionEndLat','sessionEndLong'],1)
    session.to_csv("output.csv")
    return
sessionClass()