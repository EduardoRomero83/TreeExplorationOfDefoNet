# -*- coding: utf-8 -*-
"""
Created on Wed May 25 15:50:28 2022

@author: earg8
"""

from executeTree import Classifier

class DeepForest:
    
    def __init__(self, classifierTypes):
        self.classifierTypes = classifierTypes
        self.numLayers = len(self.classifierTypes)
        self.classifiers = []
    
    def test(self):
        pred = None
        for i in range(self.numLayers):
            if i > 0:
                self.classifiers[i].addPredToTest(pred)
            print("Layer ", i)
            pred = self.classifiers[i].test()
        return
        
    def train(self):
        for i in range(self.numLayers):
            kindOfClassifier = self.classifierTypes[i]
            previousPred = None
            needPrev = False
            if i > 0:
                previousPred = self.classifiers [i - 1].trainPredictions
                needPrev = True
            self.classifiers.append(Classifier(kindOfClassifier, previousPred, needPrev))
            
        
if __name__ == "__main__":
    listOfClassifiers = ["tree"] * 1
    deepForest = DeepForest(listOfClassifiers)
    deepForest.train()
    deepForest.test()  
