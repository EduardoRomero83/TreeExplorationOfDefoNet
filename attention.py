# -*- coding: utf-8 -*-
"""
Created on Sun May 22 22:00:21 2022

@author: earg8
"""
import random
import numpy as np 


class Attention:
     
    def __init__(self, pixels, imageSize, colorChannels):
        self.pixels = pixels
        self.imageSize = imageSize
        self.colorChannels = colorChannels
        self.numAttentionRegions = 4
        self.regionwidth = 2
        self.regionHeight = 2
        self.regionSize = self.regionwidth * self.regionHeight
        self.numTotalAttentionRegions = (imageSize / colorChannels) // self.regionSize
        self.regions = self.selectRegions()


    def selectRegions (self):
        regions = []
        for i in range(self.numAttentionRegions):
            regions.append(random.randint(0, self.numTotalAttentionRegions - 1))
        return regions


    def getRegionMask(self, region, image):
        mask = []
        horizontalRegions = self.pixels // self.regionwidth
        currentRow = (region // horizontalRegions) * self.regionHeight
        rowOffset = (region % horizontalRegions) * self.regionwidth * self.colorChannels
        for i in range(self.regionHeight):
            currentPixel = (currentRow * self.pixels * self.colorChannels) + rowOffset
            for j in range(self.regionwidth):
                mask.append(currentPixel)
                currentPixel += self.colorChannels
            currentRow += 1
        return mask
    
    def getMaskValue(self, region, image):
        mask = self.getRegionMask(region, image)
        values = []
        for index in mask:
            newNum = 0
            if image[index] > 128:
                newNum = 1
            values.append(newNum)
        return values
    
    def getAttentionVector(self, image):
        vector = []
        for region in self.regions:
            vector.extend(self.getMaskValue(region, image))
        return np.array(vector)