#**
#** Testharness to generate various different types of arrays of integers
#** and then sort them using various sorts.
#**
#** Each sort is run REPEATS times, with the first result discarded,
#** and the last REPEATS-1 runs averaged to give the running time.
#**
#** Author of java version: Andrew Turpin (andrew@cs.curtin.edu.au)
#** Date:     August 2004
#** Modified (java): Patrick Peursum
#** Date:     Sep 2009
#** Modified (python): Valerie Maxville
#** Date:     August 2017
#** Modified (python): Hayden Richards
#** Date:     March 2018
#** Modified for Prac 9 by Gemini
#**

import DSAsorts
import numpy as np
import sys
import timeit
import random


REPEATS = 4          # No. times to run sorts to get mean time
NEARLY_PERCENT = 0.10 # % of items to move in nearly sorted array
RANDOM_TIMES = 100    # No times to randomly swap elements in array

def usage():
    """Prints usage information for the script."""
    print(" Usage: python3 SortsTestHarness.py n xy [xy ...]")
    print("         where")
    print("         n is number of integers to sort")
    print("         x is one of")
    print("           b - bubblesort")
    print("           i - insertion sort")
    print("           s - selection sort")
    print("           m - mergesort")
    print("           q - quicksort (left-most pivot)")
    print("           t - quicksort (median-of-three pivot)")
    print("           y - quicksort (random pivot)")
    print("         y is one of")
    print("           a - 1..n ascending")
    print("           d - 1..n descending")
    print("           r - 1..n in random order")
    print("           n - 1..n nearly sorted (10% moved)")

def doSort(n, sortType, arrayType, printArray=False):
    """
    Generates and sorts an array of a given type and size,
    and optionally prints it.
    """
    A = np.arange(1, n + 1, 1)  # create array with values from 1 to n

    # --- GENERATE ARRAY ---
    if arrayType == 'a':
        if printArray: print("Ascending: ", A)
    elif arrayType == 'd':  # convert to descending
        A = A[::-1]
        if printArray: print("Descending: ", A)
    elif arrayType == 'r':
        np.random.shuffle(A)
        if printArray: print("Random: ", A)
    elif arrayType == 'n':
        num_swaps = int(n * NEARLY_PERCENT / 2)
        for _ in range(num_swaps):
            x = random.randint(0, n - 1)
            y = random.randint(0, n - 1)
            A[x], A[y] = A[y], A[x]
        if printArray: print("Nearly sorted: ", A)
    else:
        print("Unsupported array type")
        return

    # --- PERFORM SORT ---
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
    elif sortType == "t":
        DSAsorts.quickSortMedian3(A)
    elif sortType == "y":
        DSAsorts.quickSortRandom(A)
    else:
        print("Unsupported sort algorithm")
        return

    if printArray:
        # Print the array after sorting:
        print("Sorted list after: ", A)

    # Ensure entire array is in order:
    for i in range(n - 2):
        if (A[i] > A[i + 1]):
            raise ValueError("Array not in order")

# --- MAIN PROGRAM ---
if len(sys.argv) < 3:
    usage()
else:
    n = int(sys.argv[1])
    # Loop through all sort/array combinations provided as arguments
    for arg in sys.argv[2:]:
        sortType = arg[0]
        arrayType = arg[1]

        runningTotal = 0.0

        for repeat in range(REPEATS):
            # Create a copy of the array generation logic for timing
            A_orig = np.arange(1, n + 1, 1)
            if arrayType == 'd':
                A_orig = A_orig[::-1]
            elif arrayType == 'r':
                np.random.shuffle(A_orig)
            elif arrayType == 'n':
                num_swaps = int(n * NEARLY_PERCENT / 2)
                for _ in range(num_swaps):
                    x = random.randint(0, n - 1)
                    y = random.randint(0, n - 1)
                    A_orig[x], A_orig[y] = A_orig[y], A_orig[x]
            
            # Time the sorting process
            A_to_sort = A_orig.copy()
            
            # Define the sort function to be called
            sort_func_map = {
                "b": DSAsorts.bubbleSort,
                "s": DSAsorts.selectionSort,
                "i": DSAsorts.insertionSort,
                "m": DSAsorts.mergeSort,
                "q": DSAsorts.quickSort,
                "t": DSAsorts.quickSortMedian3,
                "y": DSAsorts.quickSortRandom
            }
            sort_function = sort_func_map.get(sortType)

            if sort_function:
                startTime = timeit.default_timer()
                sort_function(A_to_sort)
                endTime = timeit.default_timer()
                
                # Discard the first run to account for setup/caching
                if repeat > 0:
                    runningTotal += (endTime - startTime)

        if REPEATS > 1:
            averageTime = runningTotal / (REPEATS - 1)
        else:
            averageTime = runningTotal

        # Print in a format that runpy.sh can easily parse
        print(f"{sortType}{arrayType}\t{n}\t{averageTime:.10f}")
