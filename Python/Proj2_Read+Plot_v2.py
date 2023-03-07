#! /usr/bin/env python

# imports of external packages to use in our code
import sys # sys to read the commandline flags and respond
import math # To do math stuff currently unused
import numpy as np # to do other math stuff
import matplotlib.pyplot as plt # To make a pretty plot
#import scipy.stats as st # Including scipy for its stat package
plt.figure(figsize = (14, 10), dpi = 100)   

# import our MySort class from PHSX815_Project1/MySort.py file
sys.path.append("C:\\Users\\bergd\\Desktop\\github")#\\PHSX815_Project1") # For running in the IDE console
sys.path.append('/mnt/c/Users/bergd/Desktop/github') # For running in the Ubuntu terminal
from PHSX815_Project1.MySort import MySort

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
    medianx = len(events) // 2
    oddlength = len(events) % 2
    
    if oddlength:
        median = events[medianx] 
    else:
        median = (events[medianx] + events[medianx-1]) / 2
    
    #calculate the mean
    mean = sum(events)/len(events)
    
    #calculate sigma
    sig68x = (len(events) * sig68) // 2 
    sig95x = (len(events) * sig95) // 2
    sig99x = (len(events) * sig99) // 2
    
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
    plt.axvline(theorysig1[1], color = '#fc0000', linestyle = 'dashed', linewidth = 2, label = '1 $\sigma$ C.I.')
    
    plt.axvline(theorysig2[0], color = '#0004fc', linestyle = 'dashed', linewidth = 2, label = '2 $\sigma$ C.I.')
    plt.axvline(theorysig2[1], color = '#0004fc', linestyle = 'dashed', linewidth = 2, label = '2 $\sigma$ C.I.')
  
    plt.axvline(theorysig3[0], color = '#107a00', linestyle = 'dashed', linewidth = 2, label = '3 $\sigma$ C.I.')
    plt.axvline(theorysig3[1], color = '#107a00', linestyle = 'dashed', linewidth = 2, label = '3 $\sigma$ C.I.')
    
    plt.legend(bbox_to_anchor=(1.0, 1), loc='upper left')
    
    plt.savefig(savename + '.png')
    plt.show()

    
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
    
    sig1 = 0.68 
    sig2 = 0.95
    sig3 = 0.99
    
###############################################################################
    #importing data
    datarate, dataNmeas, dataNexp, eventsdata = data_import(datafile) #import data file 
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
    theory_Plot('H_0 simulation', h0file, h0events, h0events_avg, h0median, h0sig1, h0sig2, h0sig3)
   
    #H1 plot
    theory_Plot('H_1 simulation', h1file, h1events, h1events_avg, h1median, h1sig1, h1sig2, h1sig3)
    
    #Data Plot
    theory_Plot('Data', datafile, dataevents, dataevents_avg, datamedian, datasig1, datasig2, datasig3)
#####################################################################################
    # Making the Log Likelihood ratios
    # My LogLikelihoodRatio (LLR) 
    lam0 = 5 #hairs/day natural
    lam1 = 15 #hairs/day gnomes    
    
    haveH0 = False
    haveH1 = False


    # default single coin-toss probability for hypothesis 0
    p0 = 0.5

    # default single coin-toss probability for hypothesis 1
    p1 = 0.9

    haveH0 = False
    haveH1 = False

    if '-lam0' in sys.argv:
        p = sys.argv.index('-lam0')
        ptemp = float(sys.argv[p+1])
        if ptemp >= 0:
            p0 = ptemp
    if '-lam1' in sys.argv:
        p = sys.argv.index('-lam1')
        ptemp = float(sys.argv[p+1])
        if ptemp >= 0:
            p1 = ptemp
    if '-input0' in sys.argv:
        p = sys.argv.index('-input0')
        InputFile0 = sys.argv[p+1]
        haveH0 = True
    if '-input1' in sys.argv:
        p = sys.argv.index('-input1')
        InputFile1 = sys.argv[p+1]
        haveH1 = True
    
    Ndays = 1 #Ntoss = 1
    Npass0 = []
    LogLikeRatio0 = []
    Npass1 = []
    LogLikeRatio1 = []

    Npass_min = 1e8
    Npass_max = -1e8
    LLR_min = 1e8
    LLR_max = -1e8
        
    with open(InputFile0) as ifile:
        for line in ifile:
            lineVals = line.split()
            Ndays = len(lineVals)
            Npass = 0
            LLR = 0
            
            hair_min = min(lineVals)
            hair_max = max(lineVals)
            
            for i in range(hair_min, hair_max + 1):
                val_index = eventsTot.index(i)
            
            for v in lineVals:
                Npass += float(v)
                
                
                
                # adding LLR for this toss
                if float(v) >= 1:
                    LLR += math.log( p1/p0 )
                else:
                    LLR += math.log( (1.-p1)/(1.-p0) )
                    
            if Npass < Npass_min:
                Npass_min = Npass
            if Npass > Npass_max:
                Npass_max = Npass
            if LLR < LLR_min:
                LLR_min = LLR
            if LLR > LLR_max:
                LLR_max = LLR
            Npass0.append(Npass)
            LogLikeRatio0.append(LLR)

    if haveH1:
        with open(InputFile1) as ifile:
            for line in ifile:
                lineVals = line.split()
                Ntoss = len(lineVals)
                Npass = 0
                LLR = 0
                for v in lineVals:
                    Npass += float(v);
                    # adding LLR for this toss
                    if float(v) >= 1:
                        LLR += math.log( p1/p0 )
                    else:
                        LLR += math.log( (1.-p1)/(1.-p0) )

                if Npass < Npass_min:
                    Npass_min = Npass
                if Npass > Npass_max:
                    Npass_max = Npass
                if LLR < LLR_min:
                    LLR_min = LLR
                if LLR > LLR_max:
                    LLR_max = LLR
                Npass1.append(Npass)
                LogLikeRatio1.append(LLR)

    title = str(Ntoss) +  " tosses / experiment"
    
    # make Npass figure
    plt.figure()
    plt.hist(Npass0, Ntoss+1, density=True, facecolor='b', alpha=0.5, label="assuming $\\mathbb{H}_0$")
    if haveH1:
        plt.hist(Npass1, Ntoss+1, density=True, facecolor='g', alpha=0.7, label="assuming $\\mathbb{H}_1$")
        plt.legend()

    plt.xlabel('$\\lambda = N_{pass}$')
    plt.ylabel('Probability')
    plt.title(title)
    plt.grid(True)

    plt.show()

    # make LLR figure
    plt.figure()
    plt.hist(LogLikeRatio0, Ntoss+1, density=True, facecolor='b', alpha=0.5, label="assuming $\\mathbb{H}_0$")
    if haveH1:
        plt.hist(LogLikeRatio1, Ntoss+1, density=True, facecolor='g', alpha=0.7, label="assuming $\\mathbb{H}_1$")
        plt.legend()

    plt.xlabel('$\\lambda = \\log({\\cal L}_{\\mathbb{H}_{1}}/{\\cal L}_{\\mathbb{H}_{0}})$')
    plt.ylabel('Probability')
    plt.title(title)
    plt.grid(True)

    plt.show()
    
