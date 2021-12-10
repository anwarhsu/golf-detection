#!/usr/bin/env python
# coding: utf-8

# # Beginning of Shawn's Portion

# 1.    Golf ball size = 1.68” diameter == 42.7 mm
# 2.    Hole size = 4.25” diameter == 108 mm
# 3.    ECPC short flagstick = 28” from parallel to ground to top of short stick.  Center white black regions are 5” each.
# 4.    White dozen ball box = 7.5” x 5 3/8” x 1.75

# # Functions 1

# In[1]:


import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
import pandas as pd

from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment


# In[2]:


BALL_DIAMETER = 1.68 #inches
HOLE_DIAMETER = 4.25
FLAG_HEIGHT = 28


# In[3]:


#create the starting 2d list of floats by loading in .txt file (fname)
#oldFormat is bool that states whether the input txt file uses old format (flag is first row). new format has flag in last row
def populateLocationData(fname):
    #!!OLD!! output has 5 cols: 1st is identifier (0 = flag, 1 = ball), 2/3 is x/y pos of CENTER, 4/5 is width/height of box
    #13 rows: 1st is flag, 12 are balls
    
    assert type(fname) == str

    f = open(fname, 'r')
    data = []
    for i, line in enumerate(f.readlines()):
        line = line[:-2] #remove \n character from the end
        nums = line.split(' ')
        
        if nums[4] == '0': #check index here. this will change by format, current v3 has identifier in index 4 (last col)
            data.insert(0, nums)
            print(i)
        else:
            data.append(nums)

    f.close()
    
    #convert list to float (from str)
    data = [[float(y) for y in x] for x in data]    
    
    return data


# !!! something is off here. using X,Y coordinates after calculation for the surface fitting is wrong. 
#may need to separate into two functions
#calculate distances from the floats, by using ratio comparisons
def calcDistances(ballData, isRotated = False):
    IDENTIFIER_TAG_INDEX = 4
    X_LOC_INDEX = 0
    Y_LOC_INDEX = 1
    WIDTH_INDEX = 2
    HEIGHT_INDEX = 3
    
    calcData = []
    for dataRow in ballData:
        newRow = []
        if dataRow[IDENTIFIER_TAG_INDEX] == 0: #if data is flaghole
            
            flagX = dataRow[X_LOC_INDEX] 
            flagY = dataRow[Y_LOC_INDEX]
            if not isRotated:
                #since WHOLE flag is currently detected, not just the hole
                flagY += 0.5 * dataRow[HEIGHT_INDEX] 
            else: #if current data is the image from the rotated one
                flagX -= 0.5 * dataRow[WIDTH_INDEX]
        else: #if data is ball

            firstX = dataRow[X_LOC_INDEX] - flagX
            distX = firstX
            #distX = -(abs(firstX) ** 2.2) if firstX < 0 else abs(firstX) ** 2.2 #experimental. comment above line
            distY = dataRow[Y_LOC_INDEX] - flagY
            #print(distX)
            #if using non-linear ratio calculation, replace the below block with references to the new model
            xHeight = dataRow[WIDTH_INDEX] 
            yHeight = dataRow[HEIGHT_INDEX]
            
            xRatio = 1 / xHeight * BALL_DIAMETER / 2 / 3.5
            yRatio = 1 / yHeight * BALL_DIAMETER / 2.3
            
            newRow.append(distX * xRatio)
            newRow.append(distY * -1 * yRatio)
            newRow.append(xRatio)
            newRow.append(yRatio)

            calcData.append(newRow)
    return calcData


# # Step 1
# Fill in lists with raw data from text files, one 90 degrees off the other  
# Calculate the distances off of ratios, filling in RDD's 1 and 2  
# INPUT TO THIS SCRIPT is the two text files below, which contain bounding boxes of objects  


#method that re-labels the balls in order to make them match between obj detected #'s to manual labels
def rearrangeData(ballData, newOrder):
    assert type(newOrder) == list and type(ballData) == list
    
    newBallData = list(range(len(ballData)))
    for i in range(len(ballData)):
        assert type(newOrder[i]) == int
        newBallData[newOrder[i] - 1] = ballData[i]
    return newBallData


# In[7]:


#method to automatically match sets of balls for location calculation
def matchPoints(l1, l2):
    assert isinstance(l1, list) and isinstance(l2, list)
    assert len(l1) > 0 and len(l2) > 0
    order = []
    for i1, pt in enumerate(l1):
        minDist = 999999
        for i2, checkPt in enumerate(l2):
            currDist = distance(pt, checkPt)
            if currDist < minDist:
                minDist = currDist
                minPt = i2
        order.append(minPt)
        
    newOrder = list(np.zeros(len(order)))
    for index, val in enumerate(order):
        newOrder[val] = int(index + 1)
        
    for i in range(len(newOrder)): #strange bug where the zero becomes type numpy float
        newOrder[i] = int(newOrder[i])
        
    #if this assert failed, some distances were not perfectly matched
    assert sorted(newOrder) == list(range(1,len(newOrder) + 1)) 
    
    return list(newOrder)

def distance(pt_1, pt_2):
    pt_1 = np.array((pt_1[0], pt_1[1]))
    pt_2 = np.array((pt_2[0], pt_2[1]))
    return np.linalg.norm(pt_1-pt_2)


# In[8]:


def matchPointsV2(l1, l2):

    points1 = np.array(l2)[:,:2]
    N = points1.shape[0]
    points2 = np.array(l1)[:,:2]

    C = cdist(points1, points2)

    _, assignment = linear_sum_assignment(C)
    newL = []
    for pt in assignment:
        newL.append(int(pt) + 1)
    return newL


# In[9]:


#method to rotate points around the origin, used to adjust the second picture to line up with first.
def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy







# # Functions 3

#start of function. method to display the actual and calculated location of golf balls. origin is flag/hole

def displayLocations(data):
    ard = np.array(data)
    plt.scatter(ard.T[0], ard.T[1], marker ='.', color = 'red')
    for i in range(len(data)):
        plt.annotate(i + 1, (ard.T[0][i], ard.T[1][i]))
    plt.axhline(0,color='k', alpha = 0.2) # x = 0
    plt.axvline(0,color='k', alpha = 0.2) # y = 0
    plt.xlabel('X Distance from Hole (ft)')
    plt.ylabel('Y Distance from Hole (ft)')
    plt.title('Calculated Location of Golf Balls');
    plt.savefig('./instance/htmlfi/golf_YOLO_distance.jpg')

    #end of function
# In[14]:


def printErrors(ard, rdd):
    #print the distance between the calculated location vs the actual location for each ball
    dist = []
    for i in range(12):
        pt1 = ard[i]
        pt2 = rdd[i]

        xDiff = abs(pt1[0] - pt2[0])
        yDiff = abs(pt1[1] - pt2[1])

        dist.append(np.sqrt(xDiff ** 2 + yDiff ** 2))
        print('Ball #', i + 1, ': {:.2f} inches'.format(dist[i] * 12))

    print('\n{:.2f} inches total, {:.2f} inches average'.format(sum(dist) * 12, sum(dist)))

def printDataTable(data):
    for d in data:
        print('({:.2f}, {:.2f})'.format(d[0], d[1]))


def getStats(row):
    output = []
    output.append(row.mean())
    output.append(row.max())
    output.append(row.min())
    output.append(row.median())
    output.append(row.std())
    return pd.DataFrame(output)



if __name__ == "__main__":
    #beginning of main
    img1_path = './instance/box1.txt'
    img2_path = './instance/box2.txt'
    #load in two images of the same ball data, second one is 90 degrees CCW around the flagpole from the first
    locData1 = populateLocationData(img1_path)
    locData2 = populateLocationData(img2_path)

    #calcDistances() returns a 12x4 list of floats, col 1/2 is X/Y pos of center of box. col 3/4 are width/height of box
    rawDistData1 = sorted(calcDistances(locData1)) #sort rdd1 by first value in row, ie. from left to right locations
    rawDistData2 = calcDistances(locData2, False)

    # # Step 2
    # Adjust data to make it comparable for errors and visualization.
    # - Rotate the 2nd image by 90 degrees
    # - Reorder the MEASURED data and 2nd image data to make all 3 lists have the same ball order
    # - Create 4th list, which is the average of the 1st image data and the reordered & rotated 2nd image data


    rotatedData = []
    for num, pt in enumerate(rawDistData1):
        newPt = rotate((0,0), (rawDistData2[num][0], rawDistData2[num][1]), math.radians(90))
        rotatedData.append(newPt)

    #block to create real, measured data as a 2d list. order only matters for labeling currently

    #measData_old = [[2.6, -9.6], [1.8, -4.2], [-1.3,-3.9], [2.3,-1.3], [3.4,-0.6], [-0.8,-0.8], 
                #[-7.3,-0.4], [1.3,0.4], [-0.4,1.0], [-3.2,3.1], [-0.8,4.8], [3.8,6.4]]
    #measData_new = [[2.6,-10.4], [1.8,-5.8], [-2.7,-4.1], [2.3,-2.8], [3.4,-1.1], [-1.2,-0.8], 
                    #[-8.7,-0.4], [1.3,0.4], [-0.4,1.0], [-4.8,3.1], [-1.3,4.8], [3.8,6.4]]

    #currOrder = matchPointsV2(rawDistData1, measData_new)
    currOrder1 = matchPointsV2(rawDistData1, rotatedData)

    #realData = rearrangeData(measData_new, currOrder)
    rotReordData = rearrangeData(rotatedData, currOrder1) #this list holds the data from the 2nd image, rotated and reordered to match

    avgdData = []
    mainProp = 0.61
    secondaryProp = 1 - mainProp
    for i in range(len(rawDistData1)):
        tempX = (rawDistData1[i][0] * mainProp + rotReordData[i][0] * secondaryProp)
        tempY = (rawDistData1[i][1] * secondaryProp + rotReordData[i][1] * mainProp)
        
        avgdData.append([tempX, tempY])


    # # Step 3
    # Visualize lists and errors


    # # Functions 2

    # for num, pt in enumerate(rawDistData1):
    #     plt.scatter(pt[0], pt[1], color = 'red')
    #     plt.scatter(rotReordData[num][0], rotReordData[num][1], color = 'blue')
    #     #plt.scatter(realData[num][0], realData[num][1], color = 'black')
    #     plt.scatter(avgdData[num][0], avgdData[num][1], color = 'green', marker = 'x')
    # plt.axhline(0,color='k', alpha = 0.2) # x = 0
    # plt.axvline(0,color='k', alpha = 0.2) # y = 0
    # plt.title('Golf balls: red=angle1, blue=angle2, green=prediction');
    # plt.savefig('./instance/htmlfi/full_output.jpg')
    
    displayLocations(avgdData)
    df = pd.DataFrame(avgdData, columns = ['x', 'y'])
    df['dist'] = np.sqrt(df['x'] ** 2 + df['y'] ** 2)



    extra = pd.concat([
            getStats(df['x']).T, 
            getStats(df['y']).T, 
            getStats(df['dist']).T
                    ]).T
    extra = extra.rename(index = {0: 'Average', 1: 'Max', 2: 'Min', 3: 'Median', 4: 'Std dev'})
    print("\nDistance calculation output:\n")
    print(df)
    print(extra)
    df.to_csv('./instance/stats.csv')
    extra.to_csv('./instance/stats_advanced.csv')

