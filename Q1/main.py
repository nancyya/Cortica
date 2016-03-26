""" Multithreaded Matching - home assignment"""

'''
Created on Mar 22, 2016

@author: nancy yacovzada
'''

"""
############################ IMPORTS ############################ 
""" 
import sys
import shutil
import multiprocessing as mp
from functools import partial
from collections import defaultdict
from datetime import datetime as time
from os import listdir, stat, makedirs, path

""" 
################### GLOBAL VARIABLES ############################ 
""" 

folderA="C://Users//nancy yacovzada//workspace//Cortica//input//A"
folderB="C://Users//nancy yacovzada//workspace//Cortica//input//B"
folderC="C://Users//nancy yacovzada//workspace//Cortica//input//C"
X=1

""" 
################################ ################################
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
        
        if not (self.k != "" and self.k > 0 and self.k is not None):
            print "k, the minimal amount of equal numbers is not legal. Nothing to do here.."
            sys.exit()
            
        
    def getFilesInFolder(self, folderName):
        """ 
        Returns a list of all file names in a folder. 
        
            Parameters
            ----------
            folderName : str.
                The full path of the folder 
             
            Returns
            ------- 
            fileNames : list of strings
        """
        fileNames = []
        if folderName:
            fileNames = [folderName + "//" + fileName for fileName in listdir(folderName) if path.isfile(path.join(folderName, fileName))]
        return fileNames
    
    def filesToSearch(self, folderName):
        """ 
        Validates files in a given folder. Returns the full path name for only files we want to search.
        Valid files are non-empty and regular files 
        
            Parameters
            ----------
            folderName : str.
                The full path of the folder 
             
            Returns
            ------- 
            fileNames : list of strings
        """
        fileNames = []
        if folderName:
            try:
                # if it is a regular file and not empty, we want to search it
                fileNames = [ fn for fn in self.getFilesInFolder(folderName) if (stat(fn).st_size > 0)]  
            except OSError:
                pass
        else:
            print "Folder is empty. Nothing to do here.."
            sys.exit()
        
        return fileNames
    
    def similarityTesting(self):
        """ 
        Updates "m.vectorsC" with files from A that are "similar" to at least 1 file from B.
        Each CSV file contain a sorted (ascending) set of integer numbers (1 row only).
        Similar == A CSV file is considered "similar" to another CSV file if both files contain at least "k" of the same numbers.
       
            Parameters
            ----------
            
            Returns
            ------- 
            vectorsC : updates self.vectorsC, a list of file names to copy
        """
        print "Similarity Testing ..."
        
        # Go over all files in A,
        for vec_i in self.vectorsA:
            fn_vec_i, v_vec_i = self.validateRow(vec_i)
            # Find 1 file in B that is similar,
            for vec_j in self.vectorsB:
                _ , v_vec_j = self.validateRow(vec_j)
                # Vectors are ordered (ascending), so we can optimize by skipping on the following cases:
                if v_vec_i[0] > v_vec_j[-1]:
                    continue
                if v_vec_j[0] > v_vec_i[-1]:
                    continue
                else:
                    # Check how many of equal numbers are in both arrays, store in _k
                    _k = len(set(v_vec_i).intersection(set(v_vec_j)))
                    # if the intersection is higher than the minimum k (self.k), 
                    if (_k >= self.k): 
                        # Keep the file name in "self.vectorsC"
                        self.vectorsC.append(fn_vec_i) 
                        # if found one similar file - break! (copy all vectors from "A", which are similar to at least 1 in "B")
                        break
        
        return self.vectorsC
    
    def validateRow(self, rowDict):
        """ Process the file content stored in rowDict"""
        try:
            for key, value in rowDict.iteritems():
                # breaks by "," to be able to compare numbers
                row = value[0].split(',')
                # convert all strings to ints, make sure all are numbers
                row = map(int, row)
        except ValueError:
            row = []
        return key, row
    
    def copyCSVFiles(self, dstdir):
        
        if (self.vectorsC): # if there are files to copy
            try:
                makedirs(dstdir) # create directory, raise an error if it already exists
            except:
                pass
            
            for srcfile in self.vectorsC:
                shutil.copy(srcfile, dstdir)
        return

"""
Note: 
    workerCopyCSVFile, workerLoadCSVFile functions is defined here 
    since the pool methods use a queue.Queue to pass tasks to the worker processes. 
    Everything that goes through the queue.Queue must be pickable, 
    but functions are only picklable if they are defined at the top-level of a module.
"""
def workerCopyCSVFile(dstdir, srcfile):
    """ 
    Copy the CSV file (content and meta-data) to a given directory with multithreading 
        Parameters
        ----------
        dstdir : str.
            The full path of the destination folder C
        srcfile : str.
            The full path of the file to copy from folder A
                     
        Returns
        ------- 
        
    """
    print "Coping File: " + srcfile
    if not path.isdir(dstdir):
        makedirs(dstdir)
    shutil.copy(srcfile, dstdir)
    return
    
def workerLoadCSVFile(fileName):
    """ 
    Load the CSV file content with multithreading
        Parameters
        ----------
        fileName : str.
            The full path of the file to load.
        Returns
        ------- 
        vecs : dictionary. 
            The "key" is the file full path, the "value" is the content of the file (a vector of numbers) 
    """
    
    vecs = {}
    print "Loading File: " + fileName
    # open connection
    with open(fileName, 'rt') as f:
        # read one line at a time from file. should be only one line.
        for line in f:
            try:
                line = line.strip().rstrip('\n')
                # The key of the dictionary - the file name. 
                vecs[fileName] = []
                # Store the file content as a value of the key 
                vecs[fileName].append(line)
                
            except ValueError: 
                pass
    
    return vecs

    
def main():
    
    print "STRAT -----> " + str(time.now())
    running_time = time.now()
    # Init
    m = MultithreadedMatching(folderA, folderB, folderC, k=X)
    
    # Load files and validate
    pool1 = mp.Pool()
    m.vectorsA = pool1.map(workerLoadCSVFile, m.filesToSearch(m.folderA))
    m.vectorsB = pool1.map(workerLoadCSVFile, m.filesToSearch(m.folderB))
    pool1.close()
    pool1.join()
    # Compute similarity between files
    m.similarityTesting()
    # Copy files to folder C
    pool2 = mp.Pool()
    pool2.map(partial(workerCopyCSVFile, folderC), m.vectorsC)
    pool2.close()
    pool2.join()
    
    running_time = time.now() - running_time
    print("FINISH -----> " + str(time.now()) + " Total running time : %s " % str(running_time))
        
##############################
       
if __name__ == '__main__':
    mp.freeze_support()
    main()