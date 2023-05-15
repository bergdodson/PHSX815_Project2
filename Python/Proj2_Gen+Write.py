#! /usr/bin/env python

# imports of external packages to use in our code
import sys # Want sys to be able to read in command line flags
#import numpy as np # Want numpy to do math stuff if it's needed.

# import our Random class from python/Random.py file
sys.path.append("C:\\Users\\bergd\\Desktop\\github")#\\PHSX815_Project1") # For running in the IDE console
sys.path.append('/mnt/c/Users/bergd/Desktop/github') # For running in the Ubuntu terminal
import Random_Proj2 as ran


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
    doRateFile = False
    #gamma variables for the numpy distribution
    a = 1
    b = 1

    # read the user-provided seed from the command line (if there), run program with -h to see a description of what each flag does.
    # Code reflective of Rogan's CookieTimer.py code
    if '-seed' in sys.argv:
        p = sys.argv.index('-seed')
        seed = sys.argv[p+1]
    if '-rateFile' in sys.argv:
        p = sys.argv.index('-rateFile')
        rateFileName = str(sys.argv[p+1])
        doRateFile = True
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
    if '-alpha' in sys.argv:
        p = sys.argv.index('-alpha')
        a = float(sys.argv[p+1])
    if '-beta' in sys.argv:
        p = sys.argv.index('-beta')
        b = float(sys.argv[p+1])
    if '-output' in sys.argv:
        p = sys.argv.index('-output')
        OutputFileName = sys.argv[p+1]
        doOutputFile = True


    # Getting and Recording the random numbers to file
    # Code Reflective of Rogan's CookieTimer.py code 

    # class instance of our Random class using seed
    random = ran.Random(seed)

    #Getting the rates from the gamma distribution
    rates = []
    if doRateFile and doOutputFile:
        rateFile = open(rateFileName, 'w')
        outputFile = open(OutputFileName, 'w')

        #Getting the sampled rates for each individual measurement and recording them in the file
        for i in range(0, Nexp):
            for j in range(0, Nmeas):
                rate = random.Gamma(a, b)
                rates.append(rate)
                rateFile.write(str(rate) + ' ')
                outputFile.write(str(random.Poisson(rate)) + ' ')
            rateFile.write('\n')
            outputFile.write('\n')
        rateFile.close()
        outputFile.close()

    elif doRateFile and not doOutputFile:
        rateFile = open(rateFileName, 'w')

        #Getting the sampled rates for each individual measurement and recording them in the file
        for i in range(0, Nexp):
            for j in range(0, Nmeas):
                rate = random.Gamma(a, b)
                rates.append(rate)
                rateFile.write(str(rate) + ' ')
            rateFile.write('\n')
        rateFile.close()

    elif not doRateFile and doOutputFile:
        outputFile = open(OutputFileName, 'w')

        #Getting the sampled rates for each individual measurement and recording them in the file
        for i in range(0, Nexp):
            for j in range(0, Nmeas):
                rate = random.Gamma(a, b)
                rates.append(rate)
                outputFile.write(str(random.Poisson(rate)) + ' ')
            outputFile.write('\n')
        outputFile.close()
    
    else: 
        for i in range(0, Nexp):
            for j in range(0, Nmeas):
                rate = random.Gamma(a, b)
                rates.append(rate)
                print(str(random.Poisson(rate)), end = ' ')
            print()


