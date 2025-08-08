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
    swapped = True

def insertionSort(A):
    """
    Pick one block at a time from messy block and insert into correct spot in the tidy block.
    """
    n = len(A) # Number of integers to sort
    for i in range(1, n):
        key = A[i] # element that is inserted into the sorted position. 
        j = i - 1 # index of the last element in the sorted positions. 
        while j >= 0 and key < A[j]:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key # place the key in its correct position. 


def selectionSort(A):
    """
    """

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


