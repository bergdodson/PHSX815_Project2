#! /usr/bin/env python

# imports of external packages to use in our code
import sys # Want sys to be able to read in command line flags
#import numpy as np # Want numpy to do math stuff if it's needed.

# import our Random class from python/Random.py file
sys.path.append("C:\\Users\\bergd\\Desktop\\github")#\\PHSX815_Project1") # For running in the IDE console
sys.path.append('/mnt/c/Users/bergd/Desktop/github') # For running in the Ubuntu terminal
from PHSX815_Project1.Random import Random


# Starting the program
if __name__ == "__main__":

	# Flags the user can include to modify how the code runs
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv:
        print("These are the flags that will modify the program: \n")
        print("-seed \t: by entering an integer following this flag, you will modify the random number seed.\n")
        print("-rate \t: by entering a positive number you will change the rate the thing happens at.\n")
        print("-Nmeas \t: by entering in a positive integer you will set how many \"measurements\" the code will perform.\n")
        print("-Nexp \t: by entering in a positive integer you will be setting the number of times the code will collect X measuremets.\n")
        print("-output \t: by entering the name of a .txt file, the code will record the measurements and expirements to the a .txt file of that name.\n")
        sys.exit(1)

    # default seed
    seed = 394348

    # default rate parameter for hairs/day that are lost)
    rate = 7

    # default number of time measurements (time to next missing cookie) - per experiment
    Nmeas = 356

    # default number of experiments
    Nexp = 10

    # output file defaults
    doOutputFile = False

    # read the user-provided seed from the command line (if there), run program with -h to see a description of what each flag does.
    # Code reflective of Rogan's CookieTimer.py code
    if '-seed' in sys.argv:
        p = sys.argv.index('-seed')
        seed = sys.argv[p+1]
    if '-rate' in sys.argv:
        p = sys.argv.index('-rate')
        ptemp = float(sys.argv[p+1])
        if ptemp > 0:
            rate = ptemp
    if '-Nmeas' in sys.argv:
        p = sys.argv.index('-Nmeas')
        Nt = int(sys.argv[p+1])
        if Nt > 0:
            Nmeas = Nt
    if '-Nexp' in sys.argv:
        p = sys.argv.index('-Nexp')
        Ne = int(sys.argv[p+1])
        if Ne > 0:
            Nexp = Ne
    if '-output' in sys.argv:
        p = sys.argv.index('-output')
        OutputFileName = sys.argv[p+1]
        doOutputFile = True


    # Getting and Recording the random numbers to file
    # Code Reflective of Rogan's CookieTimer.py code 

    # class instance of our Random class using seed
    random = Random(seed)

    if doOutputFile:
        outfile = open(OutputFileName, 'w') # Create the file that will be record the rate and subsequent random number distribution
        outfile.write(str(rate)+" \n") # writing the rate to the file.
        for e in range(0,Nexp): # Do this loop for each experiment the user requested
            for t in range(0,Nmeas): # Do this loop for each measurement the user requested
                outfile.write(str(random.DiscretePoisson(rate))+" ") # Get and record a number from the random number distribution
            outfile.write(" \n") # Create a new line at the end of the experiment
        outfile.close() # Close the file
    else:
        print(rate)
        for e in range(0,Nexp):# Do this loop for each experiment the user requested
            for t in range(0,Nmeas):# Do this loop for each measurement the user requested
                print(random.DiscretePoisson(rate), end=' ') # Get and record a number from the random number distribution
            print(" ")