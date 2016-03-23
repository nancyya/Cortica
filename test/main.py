""" Multithreaded Matching - home assignment"""

'''
Created on Mar 22, 2016

@author: nancy yacovzada
'''

"""
################################ ################################
############################ IMPORTS ############################ 
################################ ################################
""" 

import copy_reg

import re
import sys
import numpy as np
import pandas as pd
from os import listdir, stat
from os.path import isfile, join
from csv import reader
from scipy import stats
from pprint import pprint # Data pretty printer
import multiprocessing as mp
 
from collections import defaultdict
from datetime import datetime as time
from pandas.core.frame import DataFrame

## inner classes
from CSVHandler import reader 

""" 
################################ ################################
################### GLOBAL VARIABLES ############################ 
################################ ################################ 
""" 

global filesMapper; filesMapper = defaultdict(lambda: list)

class MultithreadedMatching():
    
    def __init__(self, folderA, folderB, folderC, k):
        
        self.folderA = folderA
        self.folderB = folderB
        self.folderC = folderC
        self.k = k # minimal amount of equal numbers
        self.vectorsA = defaultdict(lambda: list)
#       self.vectorsA = [{"filename": '', "id": '', "content": ''}]
                
        self.vectorsB = defaultdict(lambda: list)
        self.vectorsC = defaultdict(lambda: list)
        
    
    def getFilesInFolder(self, folderName):
        """ Returens a list of a file names in a folder"""
        fileNames = [folderName + "//" + fileName for fileName in listdir(folderName) if isfile(join(folderName, fileName))]
        return fileNames
    
    def filesToSearch(self, folderName):
        """Returns full pathname for only files we want to search"""
        if folderName:
            try:
                # if it is a regular file and not empty, we want to search it
                fileNames = [ fn for fn in self.getFilesInFolder(folderName) if (stat(fn).st_size > 0)]  
            except OSError:
                pass
        return fileNames
    
    def similarityTesting(self):
        """ updates m.vectorsC with files from A that are similar to at least 1 file from B"""
        if (self.k > 0):
            for vec_i in self.vectorsA.iteritems():
                print "XXXXXXXXXXXXXX"
                print vec_i[0], vec_i[1]
                vec_i = self.validateRow(vec_i)
                for j, vec_j in self.vectorsB.iteritems():
                    vec_j = self.validateRow(vec_j)
                    # Vectors are ordered (ascending),
                    if vec_i[0] > vec_j[-1]:
                        continue
                    if vec_j[0] > vec_i[-1]:
                        continue
                    else:
                        # Check how many of equal numbers in both arrays
                        _k = len(set(vec_i).intersection(set(vec_j)))
                        print _k
                        if (_k >= self.k): # if more than the minimum m.k
                            
                            print vec_i, i
                            self.vectorsC.append(vec_i) 
                            # copy all vectors from "A", which are similar to at least 1 in "B"
                            break
            print self.vectorsC
        else: 
            print "k, the minimal amount of equal numbers is set to zero. Nothing to do here.."
    
        return self.vectorsC
    
    def validateRow(self, row):
        try:
            row = row[0].split(',')
            # convert all strings to ints, make sure all are numbers
            row = map(int, row)
        except ValueError:
            row = []
        return row
    
def workerLoadFile(fileName):
    """ note: functions are only picklable if they are defined at the top-level of a module."""
    
    vecs = {}#defaultdict(lambda: defaultdict(list))
    print "Loading File: " + fileName
    with open(fileName, 'rt') as f:
        # read one line at a time from file
        for line in f:
            try:
                line = line.strip().rstrip('\n')
                vecs[fileName] = []
                vecs[fileName].append(line)
                
            except ValueError: 
                pass
    
    return vecs

    
def main():
    
    print "STRAT -----> " + str(time.now())
    
    running_time = time.now()
    
    folderA="C://Users//nancy yacovzada//workspace//Cortica//input//A"
    folderB="C://Users//nancy yacovzada//workspace//Cortica//input//B"
    folderC="C://Users//nancy yacovzada//workspace//Cortica//input//C"
    X=3
    
    m = MultithreadedMatching(folderA, folderB, folderC, k=X)
    
    
    pool = mp.Pool()
    m.vectorsA = pool.map(workerLoadFile, m.filesToSearch(m.folderA))
    m.vectorsB = pool.map(workerLoadFile, m.filesToSearch(m.folderB))
    pool.close()
    
    m.similarityTesting()
    
    for vec in m.vectorsA:
        print "XXX"
        
if __name__ == '__main__':
    mp.freeze_support()
    main()