# 
from DSAHeapEntry import DSAHeapEntry

class DSAHeap:
    """
    Implementation of a max heap data structure.
    """
    def __init__(self, maxSize=100):
        """
        Initializes the heap with a given maximum size.
        """
        self._heap = [None] * maxSize
        self._count = 0

    def add(self, priority, value):
        """
        Adds a new entry to the heap and maintains the heap property.
        
        Args:
            priority (int): The priority of the new entry.
            value (any): The value of the new entry.
        
        Raises:
            IndexError: If the heap is full.
        """
        if self._count >= len(self._heap):
            raise IndexError("Heap is full.")
            
        newEntry = DSAHeapEntry(priority, value)
        self._heap[self._count] = newEntry
        self.trickleUp(self._count)
        self._count += 1

    def remove(self):
        """
        Removes and returns the entry with the highest priority (the root).
        
        Returns:
            DSAHeapEntry: The entry with the highest priority.
            
        Raises:
            IndexError: If the heap is empty.
        """
        if self._count == 0:
            raise IndexError("Heap is empty.")

        # Store the root to return later
        rootEntry = self._heap[0]
        self._count -= 1
        
        # Replace the root with the last element
        self._heap[0] = self._heap[self._count]
        self._heap[self._count] = None  # Clear the last element's spot

        # Restore the heap property
        trickleDown(self._heap, 0, self._count)
        
        return rootEntry

    def display(self):
        """
        Prints the contents of the heap array for debugging purposes.
        """
        print("Heap Array:")
        for i in range(self._count):
            print(f"  [{i}]: {self._heap[i]}")

    def trickleUp(self, index):
        """
        Moves an element up the heap to its correct position.
        
        Args:
            index (int): The starting index of the element to trickle up.
        """
        parentIdx = (index - 1) // 2
        
        # Continue as long as we are not at the root and the child is greater than the parent
        while index > 0 and self._heap[index].getPriority() > self._heap[parentIdx].getPriority():
            # Swap child and parent
            self._heap[index], self._heap[parentIdx] = self._heap[parentIdx], self._heap[index]
            
            # Move up to the next level
            index = parentIdx
            parentIdx = (index - 1) // 2

def trickleDown(heapArr, currentIdx, numItems):
    """
    Moves an element down the heap to its correct position.
    This is a standalone function to be used by both DSAHeap and heapSort.

    Args:
        heapArray (list): The array representing the heap.
        currentIdx (int): The starting index of the element to trickle down.
        numItems (int): The current number of items in the heap.
    """
    lChildIdx = 2 * currentIdx + 1
    
    while lChildIdx < numItems:
        largeIdx = lChildIdx
        rChildIdx = lChildIdx + 1

        # Check if right child exists and is larger than the left child
        if rChildIdx < numItems:
            if heapArr[rChildIdx].getPriority() > heapArr[lChildIdx].getPriority():
                largeIdx = rChildIdx
        
        # If the largest child is greater than the current node, swap them
        if heapArr[largeIdx].getPriority() > heapArr[currentIdx].getPriority():
            heapArr[currentIdx], heapArr[largeIdx] = heapArr[largeIdx], heapArr[currentIdx]
            
            # Move down to the next level
            currentIdx = largeIdx
            lChildIdx = 2 * currentIdx + 1
        else:
            # If parent is larger, heap property is satisfied
            break

def heapify(array, numItems):
    """
    Converts an array into a max heap in-place.
    
    array (list): The list of DSAHeapEntry objects to heapify.
    numItems (int): The number of items in the array.
    """
    # Start from the last parent node and trickle down
    for i in range((numItems // 2) - 1, -1, -1):
        trickleDown(array, i, numItems)

def heapSort(array):
    """
    Sorts an array of DSAHeapEntry objects in-place using the HeapSort algorithm.
    The array will be sorted in ascending order of priority.

    array (list): The list of DSAHeapEntry objects to sort.
    """
    numItems = len(array)
    heapify(array, numItems) # 1. Build a max heap from the input data.
    
    # 2. One by one, extract elements from the heap.
    for i in range(numItems - 1, 0, -1):
        # Move current root to the end
        array[0], array[i] = array[i], array[0]
        
        # Call trickleDown on the reduced heap
        trickleDown(array, 0, i)

