import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math

BALL_DIAMETER = 1.68 #inches
HOLE_DIAMETER = 4.25
FLAG_HEIGHT = 28

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

    #method that re-labels the balls in order to make them match between obj detected #'s to manual labels
def rearrangeData(ballData, newOrder):
    newBallData = list(range(len(ballData)))
    for i in range(len(ballData)):
        newBallData[newOrder[i] - 1] = ballData[i]
    return newBallData


    #outdated?? basic display method which adds axes and annotation for ball #
def displayLocations(data, markertype = 'k.', label = 'Location Plot'):
    for index, pt in enumerate(data):
        plt.plot(pt[0], pt[1], markertype, markersize = 15)
        plt.annotate(str(index + 1), [pt[0] + .25, pt[1] - .25])
    plt.axhline(0,color='k', alpha = 0.2) # x = 0
    plt.axvline(0,color='k', alpha = 0.2) # y = 0
    plt.title(label)

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

    #method to display the actual and calculated location of golf balls. origin is flag/hole
def displayLocations(actualData, calculatedData, addAnnotations = True):
    
    ard = np.array(actualData)
    cd = np.array(calculatedData)
    plt.scatter(cd.T[0], cd.T[1], marker ='x', color = 'red')
    plt.scatter(ard.T[0], ard.T[1], marker ='.', color = 'black')

    if addAnnotations:
        for i in range(12):
            plt.annotate(i + 1, (cd.T[0][i] - 0.4, cd.T[1][i] + 0.1))
            #plt.annotate(i + 1, (ard.T[0][i] + 0.2, ard.T[1][i] + 0.1))

    plt.axhline(0,color='k', alpha = 0.2) # x = 0
    plt.axvline(0,color='k', alpha = 0.2) # y = 0
    plt.xlabel('X Distance from Hole (ft)')
    plt.ylabel('Y Distance from Hole (ft)')
    plt.title('Calculated (red) vs Actual (black) Location of Golf Balls')

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

if __name__ == "__main__":
    locData1 = populateLocationData('./instance/box.txt')
    rawDistData1 = calcDistances(locData1) 
    measData_old = [[2.6, -9.6], [1.8, -4.2], [-1.3,-3.9], [2.3,-1.3], [3.4,-0.6], [-0.8,-0.8], 
            [-7.3,-0.4], [1.3,0.4], [-0.4,1.0], [-3.2,3.1], [-0.8,4.8], [3.8,6.4]]
    measData_new = [[2.6,-10.4], [1.8,-5.8], [-2.7,-4.1], [2.3,-2.8], [3.4,-1.1], [-1.2,-0.8], 
                    [-8.7,-0.4], [1.3,0.4], [-0.4,1.0], [-4.8,3.1], [-1.3,4.8], [3.8,6.4]]

    currOrder = [7, 5, 1, 3, 9, 8, 10, 6, 12, 2, 4, 11] #handmade reordering from eyeballing
    realData = rearrangeData(measData_new, currOrder)
    currOrder1 = [ 4, 2, 12, 5, 1, 8, 10, 6, 3, 7, 9, 11] #handmade reordering from eyeballing

    rotatedData = []
    # print(locData1)
#temp. plot for image 1 data unrotated, image 2 data ROTATED!
    for num, pt in enumerate(rawDistData1):
        plt.scatter(pt[0], pt[1], color = 'red')
        print(pt[0] * 12, pt[1] * 12)
        #newPt = rotate((0,0), (rawDistData2[num][0], rawDistData2[num][1]), math.radians(90))
        #plt.scatter(newPt[0], newPt[1], color = 'blue')
        # plt.scatter(realData[num][0], realData[num][1], color = 'black')
        #plt.scatter(avgdData[num][0], avgdData[num][1], color = 'green', marker = 'x')
    plt.axhline(0,color='k', alpha = 0.2) # x = 0
    plt.axvline(0,color='k', alpha = 0.2) # y = 0
    plt.title('Ball Location Comparison: black = real, green = calculated data')
    plt.savefig('./instance/htmlfi/golf_YOLO_distance.jpg')
    printErrors(realData, rawDistData1)
     
