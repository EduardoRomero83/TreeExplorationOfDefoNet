# -*- coding: utf-8 -*-
"""
Created on Sun May 22 21:44:18 2022

@author: earg8
"""

from PIL import Image
from numpy import asarray
import numpy as np
from skimage import filters
from skimage.color import rgb2gray
from attention import Attention

class InputReader:
    
    def __init__(self):
        self.pixels = 108
        self.colorChannels = 1
        self.rotationAngles = []
        self.numAttentionRegions = 4
        self.regionSize = 4
        self.useAttention = False
        self.maxImages = 40000
        self.minNeg = self.maxImages / 2
        self.limitImages = False
        self.imageSize = (self.pixels * self.pixels 
                          * self.colorChannels)
        if self.useAttention:
            self.imageSizeRotated = (self.imageSize * 
                                     (len(self.rotationAngles) + 1))
            self.totalImageSize = self.imageSizeRotated + (self.regionSize 
                                                           * self.numAttentionRegions)
        
        else:
            self.imageSizeRotated = self.imageSize
            self.totalImageSize = self.imageSize
        self.numTotalAttentionRegions = ((self.imageSize / self.colorChannels) 
                                         // self.regionSize)
        self.att = Attention(self.pixels, self.imageSize, self.colorChannels)
        self.debugMode = False
        self.showAllImages = False
        
    def readInput(self, filename):
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
        print("Dataset has lines: " + str(len(lines)))
        return lines

    def rotate(self, image, degrees):
        rotatedImage = image.rotate(degrees)
        rotatedImage = rotatedImage.resize((self.pixels,self.pixels))
        return asarray(rotatedImage)

    def imageToNumpy(self, imageFile, degrees=0):
        image = Image.open(imageFile)
        if self.debugMode and self.showAllImages:
            image.show()
        image = self.rotate(image, degrees)
        if self.debugMode and self.showAllImages:
            picture = Image.fromarray(image)
            picture.show()
        data = asarray(image)
        if self.colorChannels == 1:
            bandwimage = rgb2gray(data)
            values = filters.threshold_otsu(bandwimage)
            data = bandwimage < values
        data = data.reshape(self.imageSize)
        return data

    def createDataset(self, imageFile):
        originalImageData = self.imageToNumpy(imageFile, 0)
        if not self.useAttention:
            return originalImageData
        attVector = self.att.getAttentionVector(originalImageData)
        for angle in self.rotationAngles:
            originalImageData = np.concatenate((originalImageData,
                                                self.imageToNumpy(imageFile, 
                                                                  angle)), 
                                               axis=0)
        imageWithAttention = np.concatenate((originalImageData, attVector), axis=0)
        return imageWithAttention
    

    def splitLinesIntoArray(self, lines):
        allX = []
        nnY = []
        realY = []
        i = 1
        positiveSamples = 0
        negativeSamples = 0
        for line in lines:
            fullLine = line.split()
            imageFileName = fullLine[0]
            value = float(fullLine[1])
            imageArray = self.createDataset(imageFileName)
            breakDownFileName = imageFileName.split("/")
            groundTruth = int(breakDownFileName[2])
            if value >= 0.5:
                value = 1
                positiveSamples += 1
            else:
                value = 0
                negativeSamples += 1
                if self.limitImages and negativeSamples > self.maxImages / 2: 
                    continue
            allX.append([imageArray])
            nnY.append(value)
            realY.append(groundTruth)
            i += 1
            if i > 2 and self.debugMode:
                break
            if self.limitImages and i >= self.maxImages and positiveSamples >= self.minNeg:
                break
        return allX, nnY, realY
    
    def produceDataset(self, inputFile):
        return self.splitLinesIntoArray(self.readInput(inputFile))