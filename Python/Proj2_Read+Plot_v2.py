#! /usr/bin/env python

# imports of external packages to use in our code
import sys # sys to read the commandline flags and respond
#import math # To do math stuff currently unused
import numpy as np # to do other math stuff
import matplotlib.pyplot as plt # To make a pretty plot
#import Random
#import scipy.stats as st # Including scipy for its stat package
plt.figure(figsize = (14, 10), dpi = 100)   

# import our MySort  and DiscretePoissonProb from PHSX815_Project1 folder
sys.path.append("C:\\Users\\bergd\\Desktop\\github")#\\PHSX815_Project1") # For running in the IDE console
sys.path.append('/mnt/c/Users/bergd/Desktop/github') # For running in the Ubuntu terminal
from PHSX815_Project2.Python.MySort import MySort
from PHSX815_Project2.Python.Random import Random

def data_import(file):
    #initialize
    need_rate = True
    Nmeas = 0
    Nexp = 0
    events = []
    
    #import data
    with open(file) as ifile:
        for line in ifile:
            if need_rate:
                need_rate = False
                rate = float(line)
                continue
        
            # Getting the values from the file 
            lineVals = line.split()
            Nmeas += len(lineVals)
            Nexp += 1

            # Converting the recorded values to floats and adding them to respective events array.
            for v in lineVals:
                events.append(float(v))
    
    #Returning the rate, number of pull, number of experiments, and the actual results
    return rate, Nmeas, Nexp, events;

def stats(events):
    #initialzie mean, median, and various sigma vars
    median = 0
    mean = 0
    sig68 = 0.68
    sig95 = 0.95
    sig99 = 0.99
    sig1 = []
    sig2 = []
    sig3 = []
    
    #calculating the median
    medianx = int(len(events) // 2 )
    oddlength = int(len(events) % 2)
    
    if oddlength:
        median = events[medianx] 
    else:
        median = (events[medianx] + events[medianx-1]) / 2
    
    #calculate the mean
    mean = sum(events)/len(events)
    
    #calculate sigma
    sig68x = int((len(events) * sig68) // 2 )
    sig95x = int((len(events) * sig95) // 2 )
    sig99x = int((len(events) * sig99) // 2 )
    
    sig1 = [events[medianx-sig68x], events[medianx+sig68x]]
    sig2 = [events[medianx-sig95x], events[medianx+sig95x]]
    sig3 = [events[medianx-sig99x], events[medianx+sig99x]]
    
    #Return all calculated quantities that were initialized
    return mean, median, sig1, sig2, sig3; 
    
def theory_Plot(theorytitle, savename, theoryevents, theoryavg = -1, theorymedian = -1, theorysig1 = [-1, -1], theorysig2 = [-1, -1], theorysig3 = [-1, -1]):
    #Find the number of bins in the histogram
    maxval = max(theoryevents)
    minval = min(theoryevents)
    nbins = int(maxval - minval)
    
    #Making the histogram with the data
    n, bins, patches = plt.hist(theoryevents, nbins, density = True, facecolor='g', alpha=0.75)
    plt.xlabel('Hairs missing per day')
    plt.ylabel('Probability')
    plt.title(theorytitle)
    plt.grid(True)
    
    #Overplotting the statistical quantities
    #avg + Median lines
    plt.axvline(theoryavg, color = '#6602a8', linestyle = 'dashed', linewidth = 2)
    plt.axvline(theorymedian, color = '#a602a8', linestyle = 'dashed', linewidth = 2)
    
    #plotting all the standard deviations
    plt.axvline(theorysig1[0], color = '#fc0000', linestyle = 'dashed', linewidth = 2, label = '1 $\sigma$ C.I.')
    plt.axvline(theorysig1[1], color = '#fc0000', linestyle = 'dashed', linewidth = 2)
    
    plt.axvline(theorysig2[0], color = '#0004fc', linestyle = 'dashed', linewidth = 2, label = '2 $\sigma$ C.I.')
    plt.axvline(theorysig2[1], color = '#0004fc', linestyle = 'dashed', linewidth = 2)
  
    plt.axvline(theorysig3[0], color = '#107a00', linestyle = 'dashed', linewidth = 2, label = '3 $\sigma$ C.I.')
    plt.axvline(theorysig3[1], color = '#107a00', linestyle = 'dashed', linewidth = 2)
    
    plt.legend(bbox_to_anchor=(1.0, 1), loc='upper left')
    
    plt.savefig(savename + '.png')
    plt.show()
    return nbins

    
if __name__ == "__main__":
    
    # Boolean telling us to resolve command line flags if there are any
    # Or continue if there aren't any flags. Initializing it here at the
    # beginning of the script
    haveInputh0 = False
    haveInputh1 = False
    havedata = False
    analyzeh0 = False
    analyzeh1 = False
    #lam0 = 5
    #lam1 = 15
    #datarate = 0
    h0file = ''
    h1file = ''
    datafile = ''
    h0data = np.random.randint(100, size=(5))
    h1data = np.random.randint(100, size=(5))
    data = np.random.randint(100, size=(5))
    poiprobcalc = Random()
    
    #Check the command line flags. Current options are to give only the file name and the help flag, -h
    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            print ("Usage: %s [options]" % sys.argv[0])
            print ("  options:")
            print ("   --help(-h)          print options")
            print ("   -input0 [filename]  name of file for H0 data")
            print ("   -input1 [filename]  name of file for H1 data")
            print ("   -prob0 [number]     probability of 1 for single toss for H0")
            print ("   -prob1 [number]     probability of 1 for single toss for H1")
            print
            sys.exit()
        
        #Adjusting Parameters per user specification
        if sys.argv[i] == '-inputdata':
            p = sys.argv.index('-inputdata')
            datafile = sys.argv[p+1]    
            haveInputdata = True
        elif sys.argv[i] == '-inputH0': 
            p = sys.argv.index('-inputH0')
            h0file = sys.argv[p+1]
            haveInputh0 = True
            analyzeh0 = True
        elif sys.argv[i] == '-inputH1':
            p = sys.argv.index('-inputH1')
            h1file = sys.argv[p+1]
            haveInputh1 = True
            analyzeh1 = True
        elif sys.argv[i] == '-lam0':
            p = sys.argv.index('-lam0')
            lam0 = float(sys.argv[p+1])
        elif sys.argv[i] == '-lam1':
            p = sys.argv.index('-lam1')
            lam1 = float(sys.argv[p+1])
    
#############################################################################        
    # Initialization. To simplify the issue, only the aggregate data is being analyzed, i.e. we aren't looking at data on a experiment by experiment basis
    Sorter = MySort()
    dataNmeas = 0
    dataNexp = 0
    h0Nmeas = 0
    h0Nexp = 0
    h1Nmeas = 0
    h1Nexp = 0
    
    dataevents = [] # All measurements from the data file
    h1events = [] # All measurements from the H1 file
    h0events = [] # All measurements from the H0 file
        
    dataevents_avg = 0 # Measurements average for the data file
    h0events_avg = 0 # Measurements average for the h0 file
    h1events_avg = 0 # Measurements average for the h1 file
    
    datamedian = 0 #median initialization
    h0median = 0
    h1median = 0
    
    datasig1 = [] #data Sigma initialization
    datasig2 = []
    datasig3 = []
    
    h0sig1 = [] #h0 Sigma initialization
    h0sig2 = []
    h0sig3 = []
    
    h1sig1 = [] #h1 Sigma initialization
    h1sig2 = []
    h1sig3 = []
    
    sig1 = 0.68 #Sigma values initialization
    sig2 = 0.95
    sig3 = 0.99
    
###############################################################################
    #importing data
    datarate, dataNmeas, dataNexp, dataevents = data_import(datafile) #import data file 
    h0rate, h0Nmeas, h0Nexp, h0events = data_import(h0file) # H0 import
    h1rate, h1Nmeas, h1Nexp, h1events = data_import(h1file) # H1 import
              
    #Sorting and counting events
    dataevents  = Sorter.QuickSort(dataevents) #[x / (Nmeas*Nexp) for x in Sorter.QuickSort(eventsTot)] #Probability of each event occuring normalized by the total number of measurements
    h0events    = Sorter.QuickSort(h0events)
    h1events    = Sorter.QuickSort(h1events)
    
    # Calculating and appending the mean, and credible intervals 
    dataevents_avg  = np.mean(dataevents)
    h0events_avg    = np.mean(h0events)
    h1events_avg    = np.mean(h1events)
       
###############################################################################
    #Calculating stats (mean, median, sigma1, sigma2, sigma3)    
    dataevents_avg, datamedian, datasig1, datasig2, datasig3 = stats(dataevents)
    h0events_avg, h0median, h0sig1, h0sig2, h0sig3 = stats(h0events)
    h1events_avg, h1median, h1sig1, h1sig2, h1sig3 = stats(h1events)

################################################################################   
    #Plotting directives
    #H0 plot
    h0bins = theory_Plot('H_0 simulation', h0file, h0events, h0events_avg, h0median, h0sig1, h0sig2, h0sig3)
   
    #H1 plot
    h1bins = theory_Plot('H_1 simulation', h1file, h1events, h1events_avg, h1median, h1sig1, h1sig2, h1sig3)
    
    #Data Plot
    databins = theory_Plot('Data', datafile, dataevents, dataevents_avg, datamedian, datasig1, datasig2, datasig3)
#####################################################################################
    #Log Likelihood portion
   
    #Calculate the LLR if H0 is true given the H0 distribution
    LLR_H0 = [poiprobcalc.DiscretePoissonProb(h0rate, i)/poiprobcalc.DiscretePoissonProb(h1rate, i) for i in h0events]
    #Calculate the LLR if H1 is true given the H1 distribution
    LLR_H1 = [poiprobcalc.DiscretePoissonProb(h1rate, i)/poiprobcalc.DiscretePoissonProb(h0rate, i) for i in h1events]
   
    #Calculate the LLR for H0 for the data distribution
    Actual_H0 = [poiprobcalc.DiscretePoissonProb(datarate, i)/poiprobcalc.DiscretePoissonProb(h0rate, i) for i in dataevents]   
    #Calculate the LLR for H0 for the data distribution
    Actual_H1 = [poiprobcalc.DiscretePoissonProb(datarate, i)/poiprobcalc.DiscretePoissonProb(h1rate, i) for i in dataevents]

    #Plotting the LLR stuff
    nh0, binsh0, patchesh0 = plt.hist(LLR_H0, h0bins, density = True, facecolor='#ff0000', alpha = 0.75)
    nh1, binsh1, patchesh1 = plt.hist(LLR_H1, h1bins, density = True, facecolor='#0000ff', alpha = 0.75)
    
    plt.savefig('LLRdistributionsh0_h1.png')
    plt.show()
    
    #Plotting the LLR stuff for our contrived data
    nh0, binsh0, patchesh0 = plt.hist(Actual_H0, databins, density = True, facecolor='#ff0000', alpha = 0.75)
    nh1, binsh1, patchesh1 = plt.hist(Actual_H1, databins, density = True, facecolor='#0000ff', alpha = 0.75)
    
    plt.savefig('LLRdatah0_h1.png')
    plt.show()
    