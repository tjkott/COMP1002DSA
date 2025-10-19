# Author: Thejana Kottawatta Hewage (22307822)
# Data Structures and Algorithms COMP1002
# 
# Python file to hold all sorting methods
#
# Prac 09 Code additions by Gemini
#

import random

def bubbleSort(A):
    """
    Sorts an array using bubble sort. 
    """
    n = len(A)
    pass_num = 0
    swapped_status = True
    # We need n - 1 passes to guarantee list is sorted 
    while swapped_status == True: # loop will only continue as long long as swap was made in the previous pass/ 
        swapped_status = False
        for i in range(n - 1 - pass_num):
            # ii loop in the pseudocode. 
            # n-1-pass_num: range of this loop decreases with each pass. 
            if A[i] > A[i + 1]:
                A[i], A[i + 1] = A[i + 1], A[i] # swap the elements
                swapped_status = True
        # if no swaps occur, that means the array has been sorted. 
        pass_num += 1

def insertionSort(A):
    """
    Pick one block at a time from messy block and insert into correct spot in the tidy block.
    """ 
    n = len(A)
    for i in range(1, n): # Outer loop begins from 2nd element. 
        current_element = A[i]
        # position is the index where we will compare and shift elements to.
        position = i #  position is initialised at the current element's index. 
        while position > 0 and A[position -1] > current_element:
            A[position] = A[position -1] # shift larger element to the right. 
            position = position - 1 # keep moving left until we find the correct position.
        # place the current_element in its correct position. 
        A[position] = current_element 

def selectionSort(A):
    """
    During each pass, select the smallest item from unsorted array and swap with the first item (i.e. sorted position).
    """
    n = len(A)
    # Iterate through each element of the array.
    for i in range(n):
        # Assume the first element of the unsorted part is the minimum.
        min_idx = i
        # Iterate through the unsorted part to find the actual minimum.
        for j in range(i + 1, n):
            if A[j] < A[min_idx]:
                min_idx = j
        
        # Swap the found minimum element with the first element of the unsorted part.
        A[i], A[min_idx] = A[min_idx], A[i]

# --- MERGE SORT ---
def mergeSort(A):
    """ 
    mergeSort - front-end for kick-starting the recursive algorithm. 
    """
    _mergeSortRecurse(A, 0, len(A) - 1)

def _mergeSortRecurse(A, leftIdx, rightIdx):
    """ Recursive helper function for merge sort. """
    if leftIdx < rightIdx:
        midIdx = (leftIdx + rightIdx) // 2
        _mergeSortRecurse(A, leftIdx, midIdx)
        _mergeSortRecurse(A, midIdx + 1, rightIdx)
        _merge(A, leftIdx, midIdx, rightIdx)

def _merge(A, leftIdx, midIdx, rightIdx):
    """ Merges two sorted sub-arrays into a single sorted array. """
    tempArr = [0] * (rightIdx - leftIdx + 1)
    i = leftIdx      # Pointer for the left sub-array
    j = midIdx + 1   # Pointer for the right sub-array
    k = 0            # Pointer for the temporary array

    # Merge the two sub-arrays into the temporary array
    while i <= midIdx and j <= rightIdx:
        if A[i] <= A[j]:
            tempArr[k] = A[i]
            i += 1
        else:
            tempArr[k] = A[j]
            j += 1
        k += 1

    # Copy any remaining elements from the left sub-array
    while i <= midIdx:
        tempArr[k] = A[i]
        i += 1
        k += 1

    # Copy any remaining elements from the right sub-array
    while j <= rightIdx:
        tempArr[k] = A[j]
        j += 1
        k += 1

    # Copy the sorted elements from the temporary array back to the original array
    for i in range(len(tempArr)):
        A[leftIdx + i] = tempArr[i]

# --- QUICK SORT ---
def quickSort(A):
    """ 
    quickSort - front-end for the recursive algorithm.
    This implementation uses the left-most element as the pivot.
    """
    _quickSortRecurse(A, 0, len(A) - 1, "LEFT")

def quickSortMedian3(A):
    """ 
    quickSortMedian3 - front-end for the recursive algorithm.
    This implementation uses the median-of-three as the pivot.
    """
    _quickSortRecurse(A, 0, len(A) - 1, "MEDIAN")

def quickSortRandom(A):
    """ 
    quickSortRandom - front-end for the recursive algorithm.
    This implementation uses a random element as the pivot.
    """
    _quickSortRecurse(A, 0, len(A) - 1, "RANDOM")

def _quickSortRecurse(A, leftIdx, rightIdx, pivotStrategy):
    """ Recursive helper function for quick sort. """
    if rightIdx > leftIdx:
        pivotIdx = 0
        if pivotStrategy == "LEFT":
            pivotIdx = leftIdx
        elif pivotStrategy == "RANDD_QUICK_SORT": # Mistake in previous code, changed to RANDOM
            pivotIdx = random.randint(leftIdx, rightIdx)
        elif pivotStrategy == "MEDIAN":
            midIdx = (leftIdx + rightIdx) // 2
            # Simple sort to find the median of the three
            indices = [leftIdx, midIdx, rightIdx]
            indices.sort(key=lambda i: A[i])
            pivotIdx = indices[1]
        elif pivotStrategy == "RANDOM": # Added this else-if block to correct the logic
            pivotIdx = random.randint(leftIdx, rightIdx)

        if pivotStrategy != "LEFT" and pivotStrategy != "RANDOM" and pivotStrategy != "MEDIAN":
             pivotIdx = leftIdx # Default to left pivot if strategy is unknown

        newPivotIdx = _doPartitioning(A, leftIdx, rightIdx, pivotIdx)
        
        _quickSortRecurse(A, leftIdx, newPivotIdx - 1, pivotStrategy)
        _quickSortRecurse(A, newPivotIdx + 1, rightIdx, pivotStrategy)

def _doPartitioning(A, leftIdx, rightIdx, pivotIdx):
    """ 
    Partitions the array such that elements smaller than the pivot are on its left,
    and elements larger are on its right.
    """
    pivotVal = A[pivotIdx]
    # Move pivot to the end for partitioning
    A[pivotIdx], A[rightIdx] = A[rightIdx], A[pivotVal] # <--- POTENTIAL ERROR HERE
    
    currIdx = leftIdx
    for i in range(leftIdx, rightIdx):
        if A[i] < pivotVal:
            A[i], A[currIdx] = A[currIdx], A[i]
            currIdx += 1
            
    # Move pivot to its final sorted position
    A[currIdx], A[rightIdx] = A[rightIdx], A[currIdx] # <--- AND HERE
    return currIdx