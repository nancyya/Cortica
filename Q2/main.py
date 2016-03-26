""" Rush Hour - home assignment"""

'''
Created on Mar 22, 2016

@author: nancy yacovzada
'''

"""
############################ IMPORTS ############################ 
""" 
from time import sleep
import numpy as np
from datetime import datetime as time

""" 
################### GLOBAL VARIABLES ############################ 
""" 

# Using rushHours as a Set() to represent rush hours time spans: 
#    1. Every element in the set, acts like a key in a dictionary, represents a minute in a rush hour. 
#        For example, "15.00" is 3PM and "0.59" is 12:59AM. 
#        Values in the set vary from 0.00 to 24.00. 1440 possible values. no duplications.
#    2. When the class is initialized, the set is empty (there are no rush hours at all).
#    3. A time span is added only once. If exists, not added to the set. 
#        The containment operation ("not in") takes O(1).   
#    4. isRushHour() complexity - constant time access using the "in" operator.
#    5. addTimeSpan() complexity - each "add" takes constant time access.   
#    6. Size - worst case rushHours is length 60*24=1440.

# Bonus question:
#    How would your solution be different if we changed the definition of "time" to be an integer, representing the time of day in seconds? (answer in words)
#    Answer: this solution supports the change in definition of "time" to seconds. Worst case the size of rushHours is 86,400. Additional approach is using "interval tree" (see: https://en.wikipedia.org/wiki/Interval_tree)  

rushHours = set()

def addTimeSpan(start_time, end_time):
    """ 
    Receive time-span (start_time, end_time) that is defined as "Rush Hours" and stores them.
        Parameters
        ----------
        start_time : str, in format "h.mm".
        end_time  : str, in format "h.mm".
         
        Returns
        ------- 
        Void
        """
    if ( isValidTime(start_time) and isValidTime(end_time) and start_time <= end_time):
        # Add time-span of rush hours
        # Insert into "rushHours" all the minutes in the range of [start_time, end_time)
        for minute in np.arange(roundf(start_time), roundf(end_time), 0.01):
            minute = roundf(minute)
            if minute not in rushHours and (minute%1 < 0.6): # An hour has only 60 minute 
                rushHours.add(minute)
    else:
        print "start_time:", start_time, "end_time:", end_time, " Not a valid time, behavior is not defined."  
    
    return 

def isRushHour(time):
    """ 
    Answer queries about a specific time of day - whether it is considered a rush hour or not
        Parameters
        ----------
        time : str, in format "h.mm".
            
        Returns
        ------- 
        isRushHour: boolean
    """
    isRushHour = 0
    if isValidTime(time):
        if time in rushHours:
            isRushHour = 1
            print str(time) + " is a rush hour!"
        else:
            print str(time) + " is NOT a rush hour!"
    else:
        print str(time) + " - NOT AN VALID HOUR!"
    return isRushHour

def isValidTime(time):
    """ Time T (float) is a valid time of day if (T>=0.00 and T<24.00)"""
    isValid = 0
    # First, Check if float
    if(isStrFloat(time)):
        # Take float with only precision 2 to represent "h.mm"
        time = roundf(time)
        # Extract the hour
        h = int(time)
        # Extract the minutes
        m = roundf(time - h)
        # Validate
        if (h >= 0 and h < 24 and m >= 0.00 and m < 0.60):
            isValid = 1
        
    return isValid

def isStrFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def roundf(f):
    return round(f,2)

##############################

def testInput():
    """ A test method """
    isRushHour(3.00) #--> False 
    isRushHour(5.00) #--> False
    
    addTimeSpan(2.00, 4.00) 
    isRushHour(3.00) #--> True 
    isRushHour(5.00) #--> False
    
    addTimeSpan(7.00, 9.00) 
    isRushHour(3.00) #--> True 
    isRushHour(5.00) #--> False 
    isRushHour(7.00) #--> True 
    isRushHour(11.00) #--> False
    
    addTimeSpan(8.00, 12.00)  
    isRushHour(3.00) #--> True 
    isRushHour(5.00) #--> False 
    isRushHour(7.00) #--> True 
    isRushHour(11.00) #--> True
    
    addTimeSpan(0.01, 1.01)
    isRushHour(0.01) #--> True
    isRushHour(0.00) #--> False
    isRushHour(0.59) #--> True
    
    isRushHour(5) #--> False (transforms to 5.00)
    isRushHour(500) #--> Error
    isRushHour(5.59) #--> False
    isRushHour(5.60) #--> Error
    isRushHour(25.00) #--> Error
    isRushHour(-25.00) #--> Error
    
    addTimeSpan(12.00, 8.00) # Not valid, start_time > end_time!
    
    addTimeSpan(21.01, 21.01)
    isRushHour(21.01) #--> False
    addTimeSpan(21.01, 21.02)
    isRushHour(21.01) #--> True 
    
    addTimeSpan(19, 19.05) #--> (transforms to (10.00, 10.05))
    isRushHour(19.00) #--> True
    
    ##sleep(60)
    
    addTimeSpan(0,24) # All day, 24:00 is not a valid time, behavior is not defined.
    isRushHour(0.00) #--> False, 24:00 is not a valid time, behavior is not defined.
    addTimeSpan(0,23.9) # Not valid
    addTimeSpan(0,23.5)  
    isRushHour(24.00) #--> Not valid query
    isRushHour(0.00) #--> True'
    isRushHour(5.59) #--> True

    return
##############################

class Main():
    
    print "STRAT -----> " + str(time.now())
    
    running_time = time.now()
    
    testInput() 
    
    running_time = time.now() - running_time
        
    print("FINISH -----> " + str(time.now()) + " Total running time : %s " % str(running_time))
        

