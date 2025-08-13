#**
#** Testharness to generate various different types of arrays of integers
#** and then sort them using various sorts.
#**
#** Each sort is run REPEATS times, with the first result discarded,
#** and the last REPEATS-1 runs averaged to give the running time.
#**
#** Author of java version: Andrew Turpin (andrew@cs.curtin.edu.au)
#** Date:    August 2004
#** Modified (java): Patrick Peursum
#** Date:     Sep 2009
#** Modified (python): Valerie Maxville
#** Date:    August 2017
#** Modified (python): Hayden Richards
#** Date:    March 2018

import numpy as np
import sys
import timeit
import DSAsorts
import random


REPEATS = 10           # No. times to run sorts to get mean time
NEARLY_PERCENT = 0.10 #% of items to move in nearly sorted array
RANDOM_TIMES = 100    #No times to randomly swap elements in array

def usage():
    print(" Usage: java TestHarness n xy [xy ...]")
    print("        where")
    print("        n is number of integers to sort")
    print("        x is one of")
    print("           b - bubblesort")
    print("           i - insertion sort")
    print("           s - selection sort")
    print("           q - quicksort")
    print("           m - mergesort")
    print("        y is one of")
    print("           a - 1..n ascending")
    print("           d - 1..n descending")
    print("           r - 1..n in random order")
    print("           n - 1..n nearly sorted (10% moved)")

def doSort(n, sortType, arrayType):
        A = np.arange(1, n+1, 1)   #create array with values from 1 to n
        
        if arrayType == 'a':
            print("Ascending: ", A)
        elif arrayType =='d':  #convert to descending
            for i in range(0, int(n/2)):
                temp = A[i]
                A[i] = A[n-i-1]
                A[n-i-1] = temp
            print("Descending: ", A)
        elif arrayType == 'r':
            for i in range(RANDOM_TIMES*n):
                x = int(random.random()*n)
                y = int(random.random()*n)
                temp = A[x]
                A[x] = A[y]
                A[y] = temp
            print("Random: ", A)
        elif arrayType == 'n':
            for i in range(int(n*NEARLY_PERCENT/2+1)):
                x = int(random.random()*n)
                y = int(random.random()*n)
                temp = A[x]
                A[x] = A[y]
                A[y] = temp
            print("Nearly sorted: ", A)
        else:
            print("Unsupported array type")

        if sortType == "b":
            DSAsorts.bubbleSort(A)
        elif sortType == "s":
            DSAsorts.selectionSort(A)
        elif sortType == "i":
            DSAsorts.insertionSort(A)
        elif sortType == "m":
            DSAsorts.mergeSort(A)
        elif sortType == "q":
            DSAsorts.quickSort(A)
        else:
            print("Unsupported sort algorithm")
        
        # Print the array after sorting:
        print("Sorted list after: ", A)

        # Ensure entire is in order:
        for i in range(n-2):
            if (A[i] > A[i+1]):
                raise ValueError("Array not in order")

# main program
if len(sys.argv) < 3: # exception handling - if not enough arguments are given, print the how to use program.
    usage()
else: # args handling
    for aa in range(2, len(sys.argv)):
        
        n = int(sys.argv[1]) 
        sortType = sys.argv[aa][0] # in 'br' would be 'b'
        arrayType = sys.argv[aa][1] # in 'br' would be 'r'

        runningTotal = 0 # total sum of time taken for repetitions.

        for repeat in range(REPEATS):
             if repeat == 0: # to print the header only once. 
                 print(f"Running Test: size={n}, sort='{sortType}', type='{arrayType}'") # header
                 startTime = timeit.default_timer() # TIme before starting the sort. 
                 doSort(n, sortType, arrayType) # creates the sorted array. 
                 endTime = timeit.default_timer()
             else:
                 # For subsequent runs, doesn't print the header
                 startTime = timeit.default_timer()
                 doSort(n, sortType, arrayType) # This will still print, but the logic is for timing.
                 endTime = timeit.default_timer()

             # discard REPEAT = 0 to avoid setup time affecting final time result. 
             if repeat > 0:
                 runningTotal += (endTime - startTime) # Add time taken for the current run to the total sum. 
    
        # Average time
        averageTime = runningTotal / (REPEATS - 1)
        print(f"\nAverage time for '{sortType}{arrayType}' with n={n}: {averageTime:.10f} seconds.\n")