from numpy import asarray
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.tree import export_graphviz
from sklearn import tree as sktree
from getInput import InputReader
from scipy import stats
import random


"""
Created on Mon Feb  7 20:00:28 2022

@author: Eduardo Romero
"""

class Classifier:
    
    def __init__(self, classType, prevTrainPredictions = None, needPrev = False):
        self.classifierType = classType # tree or forest
        self.inReader = InputReader()
        self.trainSetFile = "data_result_train.txt"
        self.testSetFile = "data_result_test.txt"
        self.prevTrainPred = prevTrainPredictions
        self.prevTestPred = None
        self.needPrevPred = needPrev
        self.trainX, self.trainNNy, self.trainRealY = self.extractDataset(self.trainSetFile)
        self.testX, self.testNNy, self.testRealY = self.extractDataset(self.testSetFile)
        self.trainX = self.expandDataWithPrev(self.trainX, self.prevTrainPred)
        self.train()
        self.trainPredictions = self.test("train")
        self.featuresSeenSoFar = 0

    def addPredToTest(self, predictions):
        self.testX = self.expandDataWithPrev(self.testX, predictions)

    def extractDataset(self, inputFile):
        X, nny, realy = self.inReader.produceDataset(inputFile)
        X = asarray(X).reshape((-1, self.inReader.totalImageSize))
        y = asarray(nny)
        realy = asarray(realy)
        return X, y, realy

    def expandDataWithPrev(self, X, prevPred):
        if self.needPrevPred:
            prevPred = prevPred.reshape(-1,1)
            newX = np.append(X, prevPred, axis=1)
            return newX
        else:
            return X

    def train(self):    
        X = self.trainX
        y = self.trainNNy
        if self.classifierType == "tree":
            self.tree  = DecisionTreeClassifier(max_depth=5, class_weight={0:1, 1:2})
        else:
            self.tree = RandomForestClassifier(n_estimators=20, max_depth=20, class_weight={0:1, 1:2})
        self.tree.fit(X, y)
        if self.classifierType == "tree":
            sktree.export_graphviz(self.tree, out_file="tree.dot")

    def test(self, dataset="test"):
        if dataset == "test":
            X = self.testX
            y = self.testNNy
            realy = self.testRealY
        elif dataset == "train":
            X = self.trainX
            y = self.trainNNy
            realy = self.trainRealY
        predictions = self.tree.predict(X)
        if dataset == "test":
            self.testAccuracy(predictions, y, realy)
            self.getImportances()
        return predictions

    def printClasses(self, distribution, distName):
        total = 0
        f = 0
        t = 0
        for x in distribution:
            total += 1
            if x == 1:
                t += 1
            else:
                f += 1
        print("For " + distName + ": ")
        print("Out of " + str(total) + " samples: ")
        print("there are " + str(f) +" 0's and ")
        print("there are " + str(t) +" 1's ")
        
        
    def testAccuracy(self, predictions, y, realy):
        print("Accuracy from ground truth: " + str(accuracy_score(predictions, realy)))
        print("Accuracy from nn: " + str(accuracy_score(predictions, y)))
        print("Precision for ground truth is: " + str(precision_score(realy, predictions)))
        print("Precision for nn is: " + str(precision_score(y, predictions)))
        print("Recall for ground truth is: " + str(recall_score(realy, predictions, zero_division=0)))
        print("Recall for nn is: " + str(recall_score(y, predictions, zero_division=0)))
        self.printClasses(y, "NN predictions")
        self.printClasses(predictions, "Tree predictions")
        self.printClasses(realy, "GroundTruth")
        
    def getImportances(self):
        importances = self.tree.feature_importances_
        #print(importances)
        uniformRandomDist = self.getUniformDist(importances)
        print(stats.kstest(importances, uniformRandomDist))
        #print(stats.kstest(importances, "norm"))
        #print(stats.shapiro(importances))
        
    def getUniformDist(self, importances):
        tolerance = 0.2
        imp = np.array(importances)
        importancesMean = np.mean(imp)
        #importancesStd = np.std(imp)
        low = (1.0 - tolerance) * importancesMean
        high = (1.0 + tolerance) * importancesMean
        #print("Std is: " + str(importancesStd))
        return np.random.uniform(low, high, len(importances))
    
    def testWithPath(self):
        X = self.testX
        print(X.shape)
        numSamples, numFeatures = X.shape
        sampleFeatMatrix, treeNodeOffset = self.tree.decision_path(X)
        leafIDs = self.tree.apply(X)
        usedFeatures = {}
        seenSamples = 0
        usedSamples = set()
        testedSamples = set()
        sampleID = -1
        usedSamples.add(sampleID)
        timesOutOfLoop = 0
        lastSampleUseful = False
        uselessSamples = 0
        while not self.everyFeatureUsed(usedFeatures, numFeatures) and len(testedSamples) < numSamples:
            while (sampleID in usedSamples or self.testNNy[sampleID] == 0 or
                   not lastSampleUseful) and len(testedSamples) < numSamples:
                sampleID = random.randint(0, numSamples -  1)
                lastSampleUseful = not sampleID in testedSamples
                testedSamples.add(sampleID)
            usefulSample = False
            timesOutOfLoop += 1
            usedSamples.add(sampleID)
            forestFeatures = self.getFeaturesInForest(sampleFeatMatrix, 
                                                      treeNodeOffset, leafIDs, 
                                                      sampleID)
                
            for feat in forestFeatures:
                if feat not in usedFeatures:
                    usedFeatures[feat] = 1
                    usefulSample = True
                else:
                    usedFeatures[feat] += 1
            if usefulSample:
                seenSamples += 1
                # Next lines only if getting actual heat map
                """threeZones, usedZones = self.threeZones(usedFeatures)
                if threeZones:
                    print("Found image")
                    print(usedFeatures)
                    print(sampleID)
                    break"""
            else:
                usedSamples.remove(sampleID)
                self.featuresSeenSoFar -= len(forestFeatures)
                lastSampleUseful = False
                uselessSamples += 1
        #print(usedFeatures)
        expected = self.expectedTrialsBeforeAllFeats()
        expectedFeatures = expected * seenSamples / self.featuresSeenSoFar
        sampleReduction = seenSamples / timesOutOfLoop
        print("We expect to need samples: " + str(expectedFeatures))
        print("We expect to need features: " + str(expected))
        print("We needed samples: " + str(seenSamples))
        print("We needed features: " + str(self.featuresSeenSoFar))
        print("We saw total samples (include useless): " + str(timesOutOfLoop))
        print("Reduction of samples: " + str(sampleReduction))
    #def findOptimalSubset(self, usedSamples):
        
    
    def printForest(self):
        estimators = self.tree.estimators_
        i = 0
        for t in estimators:
            export_graphviz(t, out_file="tree" + str(i) + ".dot")
            i += 1
    
    def threeZones(self, usedFeatures):
        zone1 = [0,1,2,3,8,9,10,11,16,17,18,19,24,25,26,27]
        zone2 = [4,5,6,7,12,13,14,15,20,21,22,23,28,29,30,31]
        zone3 = [32,33,34,35,40,41,42,43,48,49,50,51,56,57,58,59]
        zone4 = [36,37,38,39,44,45,46,47,52,53,54,55,60,61,62,63]
        usedZones = set()
        for key in usedFeatures:
            if "zone1" not in usedZones and key in zone1 and usedFeatures[key] >= 2:
                usedZones.add("zone1")
            if "zone2" not in usedZones and key in zone2 and usedFeatures[key] >= 2:
                usedZones.add("zone2")
            if "zone3" not in usedZones and key in zone3 and usedFeatures[key] >= 2:
                usedZones.add("zone3")
            if "zone4" not in usedZones and key in zone4 and usedFeatures[key] >= 2:
                usedZones.add("zone4")
        if len(usedZones) == 3:
            return True, usedZones
        return False, usedZones
    
    def everyFeatureUsed(self, usedFeatures, numTotalFeatures):
        if len(usedFeatures) < numTotalFeatures:
            return False
        print("Success")
        return True
    
    
    def getFeaturesInForest(self, pathIndicator, treeOffsets, leafIDs, sampleID):
        usedFeatures = []
        pathList = pathIndicator.indices[pathIndicator.indptr[sampleID]:pathIndicator.indptr[sampleID + 1]]
        if self.classifierType == "tree":
            features = self.tree.tree_.feature
            return self.getFeaturesInTree(treeOffsets, pathList, features, leafIDs)
        
        for treeIndex, tree in enumerate(self.tree.estimators_): 
            features = tree.tree_.feature
            treeNodeBoundaries = [treeOffsets[treeIndex], treeOffsets[treeIndex + 1]]
            usedFeatures.extend(self.getFeaturesInTree(treeNodeBoundaries, pathList, features, leafIDs))
        return usedFeatures
    
    def getFeaturesInTree(self, treeNodeBoundaries, pathList, features, leafIDs):
        initialBoundary = treeNodeBoundaries[0]
        pathList = [x - initialBoundary for x in pathList if x >= initialBoundary 
                    and x < treeNodeBoundaries[1] and x - initialBoundary not in leafIDs]
        featuresUsed = [features[x] for x in pathList]
        self.featuresSeenSoFar += len(featuresUsed)
        return featuresUsed
    
    def harmonic(self, n):
        harmonic = 1.00
        
        for i in range(2, n + 1):
            harmonic += 1/i
        
        return harmonic
    
    def expectedTrialsBeforeAllFeats(self):
        return self.inReader.totalImageSize * self.harmonic(self.inReader.
                                                       totalImageSize)
    
        

if __name__ == "__main__":
    for i in range(1):
        print("Execution number: " + str(i+1))
        classifier = Classifier("forest")
        #classifier.test()
        classifier.testWithPath()
