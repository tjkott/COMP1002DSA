from DSAHeapEntry import DSAHeapEntry

class DSAHeap:
    """
    Implementation of a max heap data structure.
    """
    def __init__(self, max_size=100):
        """
        Initializes the heap with a given maximum size.
        """
        self._heap = [None] * max_size
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
            
        new_entry = DSAHeapEntry(priority, value)
        self._heap[self._count] = new_entry
        self._trickle_up(self._count)
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
        root_entry = self._heap[0]
        self._count -= 1
        
        # Replace the root with the last element
        self._heap[0] = self._heap[self._count]
        self._heap[self._count] = None  # Clear the last element's spot

        # Restore the heap property
        _trickle_down(self._heap, 0, self._count)
        
        return root_entry

    def display(self):
        """
        Prints the contents of the heap array for debugging purposes.
        """
        print("Heap Array:")
        for i in range(self._count):
            print(f"  [{i}]: {self._heap[i]}")

    def _trickle_up(self, index):
        """
        Moves an element up the heap to its correct position.
        
        Args:
            index (int): The starting index of the element to trickle up.
        """
        parent_idx = (index - 1) // 2
        
        # Continue as long as we are not at the root and the child is greater than the parent
        while index > 0 and self._heap[index].get_priority() > self._heap[parent_idx].get_priority():
            # Swap child and parent
            self._heap[index], self._heap[parent_idx] = self._heap[parent_idx], self._heap[index]
            
            # Move up to the next level
            index = parent_idx
            parent_idx = (index - 1) // 2

def _trickle_down(heap_array, current_idx, num_items):
    """
    Moves an element down the heap to its correct position.
    This is a standalone function to be used by both DSAHeap and heap_sort.

    Args:
        heap_array (list): The array representing the heap.
        current_idx (int): The starting index of the element to trickle down.
        num_items (int): The current number of items in the heap.
    """
    left_child_idx = 2 * current_idx + 1
    
    while left_child_idx < num_items:
        large_idx = left_child_idx
        right_child_idx = left_child_idx + 1

        # Check if right child exists and is larger than the left child
        if right_child_idx < num_items:
            if heap_array[right_child_idx].get_priority() > heap_array[left_child_idx].get_priority():
                large_idx = right_child_idx
        
        # If the largest child is greater than the current node, swap them
        if heap_array[large_idx].get_priority() > heap_array[current_idx].get_priority():
            heap_array[current_idx], heap_array[large_idx] = heap_array[large_idx], heap_array[current_idx]
            
            # Move down to the next level
            current_idx = large_idx
            left_child_idx = 2 * current_idx + 1
        else:
            # If parent is larger, heap property is satisfied
            break

def _heapify(array, num_items):
    """
    Converts an array into a max heap in-place.
    
    Args:
        array (list): The list of DSAHeapEntry objects to heapify.
        num_items (int): The number of items in the array.
    """
    # Start from the last parent node and trickle down
    for i in range((num_items // 2) - 1, -1, -1):
        _trickle_down(array, i, num_items)

def heap_sort(array):
    """
    Sorts an array of DSAHeapEntry objects in-place using the HeapSort algorithm.
    The array will be sorted in ascending order of priority.
    
    Args:
        array (list): The list of DSAHeapEntry objects to sort.
    """
    num_items = len(array)
    
    # 1. Build a max heap from the input data.
    _heapify(array, num_items)
    
    # 2. One by one, extract elements from the heap.
    for i in range(num_items - 1, 0, -1):
        # Move current root to the end
        array[0], array[i] = array[i], array[0]
        
        # Call _trickle_down on the reduced heap
        _trickle_down(array, 0, i)
