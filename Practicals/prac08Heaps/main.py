import csv
from DSAHeap import DSAHeap, heapSort
from DSAHeapEntry import DSAHeapEntry

def loadDataFromCsv(filename="RandomNames7000.csv"):
    """
    Loads data from the specified CSV file into a list of DSAHeapEntry objects.
    It reads the integer from the first column as priority and the name from the
    second column as the value.
    
    Args:
        filename (str): The name of the CSV file.
        
    Returns:
        list: A list of DSAHeapEntry objects.
    """
    entries = []
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                try:
                    priority = int(row[0])
                    value = row[1]
                    entries.append(DSAHeapEntry(priority, value))
                except (ValueError, IndexError):
                    # Skip rows that don't have the correct format
                    continue
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    return entries

def testHeap(data):
    """
    Tests the DSAHeap class by adding and removing elements.
    """
    print("\n----- Testing DSAHeap Implementation -----")
    # Create a heap with enough capacity
    heap = DSAHeap(len(data) + 1)
    
    print("Adding elements to the heap...")
    for entry in data:
        heap.add(entry.getPriority(), entry.getValue())
    
    print("\nHeap state after adding all elements:")
    heap.display()
    
    print("\nRemoving elements from heap (should be in descending priority order):")
    removedItems = []
    try:
        while True:
            removedItems.append(heap.remove())
    except IndexError:
        # This is expected when the heap becomes empty
        pass
    
    for item in removedItems:
        print(item, end=" ")
    print("\n\nDSAHeap test complete.")

def testHeapsort(data):
    """
    Tests the heapSort function.
    """
    print("\n----- Testing HeapSort Implementation -----")
    print("Original array (first 10 elements):")
    for i in range(min(10, len(data))):
        print(data[i], end=" ")
    print("\n")

    heapSort(data)

    print("Sorted array (first 10 elements):")
    for i in range(min(10, len(data))):
        print(data[i], end=" ")
    print("\n")

    print("Sorted array (last 10 elements):")
    for i in range(max(0, len(data) - 10), len(data)):
        print(data[i], end=" ")
    print("\n\nHeapSort test complete.")


if __name__ == "__main__":
    # Load the data from the CSV file
    heapEntries = loadDataFromCsv()

    if heapEntries:
        # Create a copy for the heapsort test, as it sorts in-place
        heapEntriesForSort = list(heapEntries)
        
        # Run the tests
        testHeap(heapEntries) # tests DSAHeap class. 
        testHeapsort(heapEntriesForSort) # tests heapSort
    else:
        print("No data loaded. Cannot run tests.")
        print("Please ensure 'RandomNames7000.csv' is in the same directory.")

