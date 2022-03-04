import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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



def session_summary():
    
    processList = ['input']
    
    for l in processList:
        print("processing "+l)
        inputFile = open(l+'.csv', "r")
        reader = csv.reader(inputFile)
    
        #use for the first round
        if l ==processList[0]:
            outputSession = open('output.csv', "w", newline='')
            writer1 = csv.writer(outputSession, delimiter = ',')
            writer1.writerow(["deviceID","sessionID","sessionStartTime","sessionStartLat","sessionStartLong","sessionEndTime","sessionEndLat","sessionEndLong","numberOf10sGaps","numberOf1minGaps","numberOf3minGaps"])
        else:
            #use for 2nd to last round
            outputSession = open('output.csv', "a", newline='')
            writer1 = csv.writer(outputSession, delimiter = ',')
    
    
        next(reader)#skip the first line in original csv file, which is the column label
        row1 = next(reader)#skip the first row of data
        
        deviceID = row1[5]
        sessionID = row1[4]
        sessionStartTime = row1[1]
        sessionStartLat = row1[2]
        sessionStartLong = row1[3]
        sessionEndTime = None
        sessionEndLat = None
        sessionEndLong = None
        #totalDist = 0
        numberOf10sGaps = 0
        numberOf1minGaps = 0
        numberOf3minGaps = 0
        
        lastTime = row1[1]
        lastLat = row1[2]
        lastLong = row1[3]
        
        for row in reader:
            if row[4] == sessionID:
                #totalDist = totalDist + float(row[7])
                if float(row[6]) > (10/60):
                    numberOf10sGaps = numberOf10sGaps + 1
                if float(row[6]) > 1:
                    numberOf1minGaps = numberOf1minGaps + 1
                if float(row[6]) > 3:
                    numberOf3minGaps = numberOf3minGaps + 1          
            else:
                sessionEndTime = lastTime
                sessionEndLat = lastLat
                sessionEndLong = lastLong
                
                r1 = [deviceID,sessionID,sessionStartTime,sessionStartLat,sessionStartLong,sessionEndTime,sessionEndLat,sessionEndLong,numberOf10sGaps,numberOf1minGaps,numberOf3minGaps]
                if(numberOf3minGaps==1):
                    writer1.writerow(r1)
                
                #totalDist = 0
                numberOf10sGaps = 0
                numberOf1minGaps = 0
                numberOf3minGaps = 0
                deviceID = row[5]
                sessionID = row[4]
                sessionStartTime = row[1]
                sessionStartLat = row[2]
                sessionStartLong = row[3]
            
            lastTime = row[1]
            lastLat = row[2]
            lastLong = row[3]
        
        sessionEndTime = lastTime
        sessionEndLat = lastLat
        sessionEndLong = lastLong
        r1 = [deviceID,sessionID,sessionStartTime,sessionStartLat,sessionStartLong,sessionEndTime,sessionEndLat,sessionEndLong,numberOf10sGaps,numberOf1minGaps,numberOf3minGaps]
        if(numberOf3minGaps==1):
            writer1.writerow(r1)
        
        inputFile.close()
        outputSession.close()
    
    return

session_summary()