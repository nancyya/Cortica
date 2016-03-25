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
import shutil
import numpy as np
import pandas as pd
from scipy import stats
import multiprocessing as mp
from os import listdir, stat, makedirs
from os.path import isfile, join
from collections import defaultdict
from datetime import datetime as time


""" 
################################ ################################
################### GLOBAL VARIABLES ############################ 
################################ ################################ 
""" 

class MultithreadedMatching():
    
    def __init__(self, folderA, folderB, folderC, k):
        
        self.folderA = folderA
        self.folderB = folderB
        self.folderC = folderC
        self.k = k # minimal amount of equal numbers
        self.vectorsA = defaultdict(lambda: list)
        self.vectorsB = defaultdict(lambda: list)
        self.vectorsC = []
        
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
            for vec_i in self.vectorsA:
                fn_vec_i, v_vec_i = self.validateRow(vec_i)
                for vec_j in self.vectorsB:
                    _ , v_vec_j = self.validateRow(vec_j)
                    # Vectors are ordered (ascending),
                    if v_vec_i[0] > v_vec_j[-1]:
                        continue
                    if v_vec_j[0] > v_vec_i[-1]:
                        continue
                    else:
                        # Check how many of equal numbers in both arrays
                        _k = len(set(v_vec_i).intersection(set(v_vec_j)))
                        # if the intersection is more than the minimum m.k
                        if (_k >= self.k): 
                            self.vectorsC.append(fn_vec_i) 
                            # copy all vectors from "A", which are similar to at least 1 in "B"
                            break
        else: 
            print "k, the minimal amount of equal numbers is set to zero. Nothing to do here.."
    
        return self.vectorsC
    
    def validateRow(self, rowDict):
        try:
            for key, value in rowDict.iteritems():
                row = value[0].split(',')
                # convert all strings to ints, make sure all are numbers
                row = map(int, row)
        except ValueError:
            row = []
        return key, row
    
    def copyCSVFiles(self, dstdir):
        
        if (self.vectorsC):
            try:
                makedirs(dstdir) # create all directories, raise an error if it already exists
            except:
                pass
            
            for srcfile in self.vectorsC:
                shutil.copy(srcfile, dstdir)
        return
    
def workerLoadFile(fileName):
    """ 
        Load the CSV files content with multithreading
        note: 
            This function is defined here since the pool methods use a queue.Queue to pass tasks to the worker processes. 
            Everything that goes through the queue.Queue must be pickable, but functions are only picklable if they are defined at the top-level of a module.
    """
    
    vecs = {}
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
    X=1
    
    m = MultithreadedMatching(folderA, folderB, folderC, k=X)
    
    
    pool = mp.Pool()
    m.vectorsA = pool.map(workerLoadFile, m.filesToSearch(m.folderA))
    m.vectorsB = pool.map(workerLoadFile, m.filesToSearch(m.folderB))
    pool.close()
    
    m.similarityTesting()
    
    m.copyCSVFiles(folderC)
    
    running_time = time.now() - running_time
        
    print("FINISH -----> " + str(time.now()) + " Total running time : %s " % str(running_time))
        
##############################
       
if __name__ == '__main__':
    mp.freeze_support()
    main()