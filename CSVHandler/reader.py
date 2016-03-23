'''
Created on Mar 22, 2016

@author: nancy yacovzada
'''

"""
################################ ################################
############################ IMPORTS ############################ 
################################ ################################
"""
import sys
import ast
import pickle
import numpy as np
from csv import reader
from pprint import pprint
from scipy.sparse import csr_matrix
from datetime import datetime as time
from sklearn.feature_extraction import DictVectorizer, FeatureHasher
from sklearn.datasets import dump_svmlight_file 

def readDatasetFromFile(filepath):
    
    print "Read Dataset From File..." + str(time.now())
    
    number_of_entries = 0
        
    with open(filepath, "r") as f:
        
        # using the csv module to split a line by commas, but ignore commas within quotes 
        csv_reader = reader(f)
        
        for line in csv_reader:
            
            yield line # "yield" return a generator. Handy when this function will return a huge set of values that we will only need to read once.
            
            number_of_entries += 1
        
        print "Number of entries read from file: %s" % str(number_of_entries)
        
    return