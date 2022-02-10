from PIL import Image
from numpy import asarray
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from skimage import filters
from skimage.color import rgb2gray

"""
Created on Mon Feb  7 20:00:28 2022

@author: Eduardo Romero
"""

pixels = 10
colorChannels = 1
debugMode = False
imageSize = pixels * pixels * colorChannels



def readInput (filename):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    return lines

def imageToNumpy(imageFile):
    image = Image.open(imageFile)
    image = image.resize((pixels,pixels))
    data = asarray(image)
    bandwimage = rgb2gray(data)
    values = filters.threshold_otsu(bandwimage)
    data = bandwimage < values
    data = data.reshape(imageSize)
    return data

def splitLinesIntoArray(lines):
    allX = []
    nnY = []
    realY = []
    i = 10
    for line in lines:
        fullLine = line.split()
        imageFileName = fullLine[0]
        value = float(fullLine[1])
        imageArray = imageToNumpy(imageFileName)
        breakDownFileName = imageFileName.split("/")
        groundTruth = int(breakDownFileName[2])
        if value >= 0.5:
            value = 1
        else:
            value = 0
        allX.append([imageArray])
        nnY.append(value)
        realY.append(groundTruth)
        i += 1
        if i > 9 and debugMode:
            break
    return allX, nnY, realY
        

def train():
    print("Started training")
    inputFile = "data_result_train.txt"
    
    X, nny, realy = splitLinesIntoArray(readInput(inputFile))
    
    X = asarray(X).reshape((-1,imageSize))
    y = asarray(nny)
    realy = asarray(realy)
    print("Processed data")
    #♣tree  = DecisionTreeClassifier(max_depth=5)
    tree = RandomForestClassifier(n_estimators=20, max_depth=10)
    tree.fit(X, y)
    print("Done training")
    return tree


def test(tree):
    print("Started testing")
    inputFile = "data_result_test.txt"
    X, nny, realy = splitLinesIntoArray(readInput(inputFile))
    X = asarray(X).reshape((-1,imageSize) )
    y = asarray(nny)
    realy = asarray(realy)
    print("Processed data")
    predictions = tree.predict(X)
    print("Done training")
    testAccuracy(predictions, y, realy)

def testAccuracy(predictions, y, realy):
    print("Accuracy from ground truth: " + str(accuracy_score(predictions, realy)))
    print("Accuracy from nn: " + str(accuracy_score(predictions, y)))
    print("Precision for ground truth is: " + str(precision_score(realy, predictions)))
    print("Precision for nn is: " + str(precision_score(y, predictions)))
    print("Recall for ground truth is: " + str(recall_score(realy, predictions)))
    print("Recall for nn is: " + str(recall_score(y, predictions)))
test(train())