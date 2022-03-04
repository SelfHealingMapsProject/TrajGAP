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

def get_core_columns():
    processList = ['2016-09-11short']
    for l in processList:
        data = pd.read_csv(l+".csv", dtype={14:str} , header = None,usecols = [0,1,2,13,14],names=["time","lat","long","sessionID","deviceID"])
        data["time"] = pd.to_datetime(data["time"])
        data["timeDiff"] = data.groupby("sessionID")["time"].diff()/np.timedelta64(1,"s")/60 # in minute
        data.to_csv("output.csv")
    return

get_core_columns()