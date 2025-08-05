#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#

def bubbleSort(A):
    """
    Sorts an array using bubble sort. 
    """
    n = len(A)
    # We need n - 1 passes to guarantee list is sorted
    for pass_num in range (n-1):
        swapped_status = False
        for i in range(n - 1 - pass_num):
            # ii loop in the pseudocode. 
            # n-1-pass_num: range of this loop decreases with each pass. 
            if A[i] > A[i + 1]:
                # Swap the elements
                A[i], A[i + 1] = A[i + 1], A[i]
                swapped_status = True
        # if no swaps occur, that means the array has been sorted. 
        if not swapped_status:
            break

def insertionSort(A):
    """
    Pick one block at a time from messy block and insert into correct spot in the tidy block.
    """
        # Outer loop begins from 2nd element / index 1. 
    n = len(A)
    for i in range(1, n):
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

def mergeSort(A):
    """ 
    mergeSort - front-end for kick-starting the recursive algorithm
    """
    ...

def mergeSortRecurse(A, leftIdx, rightIdx):
    ...

def merge(A, leftIdx, midIdx, rightIdx):
    ...

def quickSort(A):
    """ quickSort - front-end for kick-starting the recursive algorithm
    """
    ...

def quickSortRecurse(A, leftIdx, rightIdx):
    ...

def doPartitioning(A, leftIdx, rightIdx, pivotIdx):
    ...


