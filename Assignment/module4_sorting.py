# MODULE 4: Sorting Patients Records
# Author: Thejana Kottawatta (22307822)

import time
import random
import os
import sys

class TreatmentRecord:
    """A simple record to hold patient ID and treatment duration."""
    def __init__(self, patient_id, duration):
        self.patient_id = patient_id
        self.duration = duration

    def __repr__(self):
        """String representation for printing."""
        return f"(ID: {self.patient_id}, Dur: {self.duration}m)"

class SortStats:
    """A simple object to track comparisons and swaps."""
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0

    def __repr__(self):
        """String representation for the results table."""
        return f"{self.comparisons:<12} | {self.swaps:<12}"

## Merge Sort (top-down or bottom-up; justify choice).
def mergeSort(arr, stats): 
    """
    mergeSort - front-end for kick-starting the recursive algorithm.
    Sorts a list of TreatmentRecord objects in-place.
    """
    # Set recursion limit to be safe for 1000+ elements
    if len(arr) + 100 > sys.getrecursionlimit():
        sys.setrecursionlimit(len(arr) + 100)
    MergeSortRec(arr, 0, len(arr) - 1, stats)

def MergeSortRec(arr, leftIdx, rightIdx, stats):
    """ Recursive helper function for merge sort. """
    if leftIdx < rightIdx:
        midIdx = (leftIdx + rightIdx) // 2
        MergeSortRec(arr, leftIdx, midIdx, stats)
        MergeSortRec(arr, midIdx + 1, rightIdx, stats)
        Merge(arr, leftIdx, midIdx, rightIdx, stats)

def Merge(arr, leftIdx, midIdx, rightIdx, stats):
    """ Merges two sorted sub-arrays into a single sorted array. """
    # Create temp array matching the size of the sub-array we are merging
    tempArr = [None] * (rightIdx - leftIdx + 1)
    i = leftIdx      # Pointer for the left sub-array
    j = midIdx + 1   # Pointer for the right sub-array
    k = 0            # Pointer for the temporary array

    # Merge the two sub-arrays into the temporary array
    while i <= midIdx and j <= rightIdx:
        stats.comparisons += 1
        # We compare the .duration attribute of the TreatmentRecord
        if arr[i].duration <= arr[j].duration:
            tempArr[k] = arr[i]
            i += 1
        else:
            tempArr[k] = arr[j]
            j += 1
        k += 1

    # Copy any remaining elements from the left sub-array
    while i <= midIdx:
        tempArr[k] = arr[i]
        i += 1
        k += 1

    # Copy any remaining elements from the right sub-array
    while j <= rightIdx:
        tempArr[k] = arr[j]
        j += 1
        k += 1

    # Copy the sorted elements from the temporary array back to the
    # original array 'arr' at the correct 'leftIdx' offset
    for temp in range(len(tempArr)):
        arr[leftIdx + temp] = tempArr[temp]
        # This is a write/copy, not a swap. Swaps remain 0 for Merge Sort.

def quickSort(arr, stats):
    """ 
    quickSort - front-end for the recursive algorithm.
    This implementation uses the left-most element as the pivot.
    """
    # Set recursion limit to be safe for 1000+ elements
    if len(arr) + 100 > sys.getrecursionlimit():
        sys.setrecursionlimit(len(arr) + 100)
    _quickSortRec(arr, 0, len(arr) - 1, "LEFT", stats)

def quickSortMedian3(arr, stats):
    """ 
    quickSortMedian3 - front-end for the recursive algorithm.
    This implementation uses the median-of-three as the pivot.
    This is the justified and benchmarked version for the assignment.
    """
    # Set recursion limit to be safe for 1000+ elements
    if len(arr) + 100 > sys.getrecursionlimit():
        sys.setrecursionlimit(len(arr) + 100)
    _quickSortRec(arr, 0, len(arr) - 1, "MEDIAN", stats)

def quickSortRandom(arr, stats):
    """ 
    quickSortRandom - front-end for the recursive algorithm.
    This implementation uses a random element as the pivot.
    """
    # Set recursion limit to be safe for 1000+ elements
    if len(arr) + 100 > sys.getrecursionlimit():
        sys.setrecursionlimit(len(arr) + 100)
    _quickSortRec(arr, 0, len(arr) - 1, "RANDOM", stats)

def _quickSortRec(arr, leftIdx, rightIdx, pivotStrategy, stats):
    """ 
    Recursive helper function for quick sort. 
    Accepts a pivotStrategy string.
    """
    if rightIdx > leftIdx:
        pivotIdx = 0
        
        if pivotStrategy == "LEFT":
            pivotIdx = leftIdx
            
        elif pivotStrategy == "MEDIAN":
            midIdx = (leftIdx + rightIdx) // 2
            
            # Manually sort the 3 indices based on duration to find median
            # (This replaces the non-allowed indices.sort(key=...) from the example)
            stats.comparisons += 1
            if arr[leftIdx].duration > arr[midIdx].duration:
                Swap(arr, leftIdx, midIdx, stats)
                
            stats.comparisons += 1
            if arr[leftIdx].duration > arr[rightIdx].duration:
                Swap(arr, leftIdx, rightIdx, stats)
                
            stats.comparisons += 1
            if arr[midIdx].duration > arr[rightIdx].duration:
                Swap(arr, midIdx, rightIdx, stats)
            
            # The median is now at midIdx
            pivotIdx = midIdx
            
        elif pivotStrategy == "RANDOM":
            pivotIdx = random.randint(leftIdx, rightIdx)
            
        else: # Default case
            pivotIdx = leftIdx

        # Partition the array and get the pivot's new, final index
        newPivotIdx = _partitioning(arr, leftIdx, rightIdx, pivotIdx, stats)
        
        # Recursively sort the two subarrays
        _quickSortRec(arr, leftIdx, newPivotIdx - 1, pivotStrategy, stats)
        _quickSortRec(arr, newPivotIdx + 1, rightIdx, pivotStrategy, stats)

def _partitioning(arr, leftIdx, rightIdx, pivotIdx, stats):
    """ 
    Partitions the array using the Lomuto scheme.
    It swaps the chosen pivot to the end (rightIdx) to act as the sentinel.
    """
    # Get the value to compare against (the duration)
    pivotVal = arr[pivotIdx].duration
    
    # Move pivot to the end (rightIdx) for partitioning
    Swap(arr, pivotIdx, rightIdx, stats)
    
    currIdx = leftIdx
    # Loop from leftIdx up to (but not including) the pivot at rightIdx
    for i in range(leftIdx, rightIdx):
        stats.comparisons += 1
        # Compare against the pivot's duration
        if arr[i].duration <= pivotVal:
            Swap(arr, i, currIdx, stats)
            currIdx += 1
            
    # Move pivot to its final sorted position
    Swap(arr, currIdx, rightIdx, stats)
    return currIdx # Return the pivot's new index

def Swap(arr, i, j, stats):
    """
    Swaps two elements in the array and increments the swap counter.
    (This is now a top-level helper function, as required by
    both _quickSortRec and _partitioning).
    """
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp
    stats.swaps += 1

class DataGenerator:
    """Generates test datasets with a reproducible random seed."""
    def __init__(self, seed):
        self.seed = seed
        self.max_duration = 300 # Max treatment time in minutes

    def GenerateRecords(self, size):
        """Generates a list of records with random durations."""
        random.seed(self.seed)
        arr = []
        for i in range(size):
            arr.append(TreatmentRecord(i, random.randint(10, self.max_duration)))
        return arr

    def GetRandom(self, size):
        """Returns a randomly ordered list."""
        return self.GenerateRecords(size)

    def GetSorted(self, size):
        """Returns a fully sorted list (used as a base)."""
        arr = self.GenerateRecords(size)
        # We must use one of our own sorts to create the sorted list.
        # We use a dummy stats object as we don't care about these counts.
        mergeSort(arr, SortStats()) # Use our new in-place merge sort
        return arr

    def GetReversed(self, size):
        """Returns a list sorted in reverse order."""
        sorted_arr = self.GetSorted(size)
        
        # Manually reverse the list without using built-in .reverse()
        reversed_arr = []
        for i in range(len(sorted_arr) - 1, -1, -1):
            reversed_arr.append(sorted_arr[i])
        return reversed_arr

    def GetNearlySorted(self, size):
        """Returns a sorted list with 10% of elements swapped."""
        arr = self.GetSorted(size)
        displacements = int(size * 0.1)
        
        # We must use the *same seed* to ensure the swaps are reproducible
        random.seed(self.seed)
        
        for _ in range(displacements):
            idx1 = random.randint(0, size - 1)
            idx2 = random.randint(0, size - 1)
            
            # Manually swap
            temp = arr[idx1]
            arr[idx1] = arr[idx2]
            arr[idx2] = temp
            
        return arr

class Benchmark:
    """Runs the sorting algorithms and collects results."""
    def __init__(self):
        self.results = []

    def Run(self, sort_function, data, sort_name, condition_name):
        """Times a sort function, collects stats, and verifies correctness."""
        
        data_copy = []
        for r in data:
            data_copy.append(TreatmentRecord(r.patient_id, r.duration))
            
        stats = SortStats()
        
        # Start timer
        start_time = time.perf_counter()
        
        # Run the sort (both are in-place and return None)
        sort_function(data_copy, stats)
        sorted_data = data_copy # The copy is now sorted
            
        # Stop timer
        end_time = time.perf_counter()
        
        duration_ms = (end_time - start_time) * 1000
        is_sorted = self.CheckSorted(sorted_data)

        self.results.append({
            "Algorithm": sort_name,
            "Condition": condition_name,
            "Size": len(sorted_data),
            "Time (ms)": duration_ms,
            "Stats": stats,
            "Passed": "Yes" if is_sorted else "NO_FAIL"})

    def CheckSorted(self, arr):
        """Verifies if the list is correctly sorted by duration."""
        for i in range(len(arr) - 1):
            if arr[i].duration > arr[i+1].duration:
                return False
        return True

    def DisplayResults(self):
        """Builds the benchmark results table as a list of strings."""
        output = []
        
        table_width = 86
        header = "\n" + "="*table_width
        header += "\n--- Sorting Algorithm Benchmark Results ---"
        header += "\n" + "="*table_width
        output.append(header)
        
        cols = f"{'Algorithm':<12} | {'Condition':<18} | {'Size':<6} | {'Time (ms)':<10} | " \
               f"{'Comparisons':<12} | {'Swaps':<12} | {'Passed'}"
        output.append(cols)
        output.append("-"*table_width)
        
        for res in self.results:
            row = f"{res['Algorithm']:<12} | {res['Condition']:<18} | {res['Size']:<6} | " \
                  f"{res['Time (ms)']:<10.3f} | {res['Stats']!s} | {res['Passed']}"
            output.append(row)
            
        output.append("="*table_width)
        return output

def main():
    """Test driver
    """
    file_output = []
    
    Seed = 41 ## Use deterministic random seeds for reproducibility.
    sizes = [100, 500, 1000] ## Generate and sort datasets of size 100, 500, and 1000.
    
    generator = DataGenerator(Seed) # pass the seed to data gen
    benchmark = Benchmark()

    file_output.append("--- 1. Sample Sort Output (Size=100, Random) ---")
    sample_data = generator.GetRandom(100)
    file_output.append(f"Original (first 10): {[f'{r.duration}m' for r in sample_data[:10]]}")
    
    # Create a copy for the sample sort
    sorted_sample_copy = []
    for r in sample_data:
        sorted_sample_copy.append(TreatmentRecord(r.patient_id, r.duration))

    # Run the in-place sort on the copy
    mergeSort(sorted_sample_copy, SortStats()) 
    
    file_output.append(f"Sorted (first 10):   {[f'{r.duration}m' for r in sorted_sample_copy[:10]]}")
    file_output.append(f"Sorted (last 10):    {[f'{r.duration}m' for r in sorted_sample_copy[-10:]]}")

    file_output.append("\n--- 2. Running Full Benchmark ---")
    
    for size in sizes:
        file_output.append(f"Generating and testing datasets for size {size}...")
        ##  For each size, test three conditions: random, nearly sorted (≤10% elements displaced), and reversed. 
        datasets = {"Random": generator.GetRandom(size),
            "Reversed": generator.GetReversed(size),
            "Nearly Sorted": generator.GetNearlySorted(size)}
        
        for condition_name, data in datasets.items():
            benchmark.Run(mergeSort, data, "Merge Sort", f"{condition_name}")
            benchmark.Run(quickSortMedian3, data, "Quick Sort", f"{condition_name}") 

    # Add the formatted table (which is now a list of strings) to our log
    table_strings = benchmark.DisplayResults()
    file_output.extend(table_strings)
    
    # --- Final Analysis ---
    file_output.append("\n--- 3. Benchmark Analysis ---")
    file_output.append("Merge Sort (In-Place):")
    file_output.append(" - Consistent O(nlogn) performance. Time scales predictably with size.")
    file_output.append(" - Performance is almost identical for Random, Reversed, and Nearly Sorted data,")
    file_output.append("   proving it is not vulnerable to input order. Swaps are 0 as it copies.")
    file_output.append("\nQuick Sort (Median-of-Three):")
    file_output.append(" - Fastest on average (especially for Random and Nearly Sorted data).")
    file_output.append(" - The Mo3 pivot strategy successfully prevented $O(n^2)$ behavior on Reversed")
    file_output.append("   and Nearly Sorted lists, keeping performance at $O(n log n).")
    file_output.append(" - Shows the highest number of swaps, as it works in-place.")
    file_output.append("\nConclusion:")
    file_output.append(" - For general-purpose sorting, QuickSort (with Mo3) is fastest.")
    file_output.append(" - If stability is required (preserving order of 30m, 30m), Merge Sort is the only choice.")
    file_output.append(" - If predictable, worst-case performance is critical, Merge Sort is safer.")

    # --- 3. Join all output and save/print ---
    
    # Combine the list of strings into one single string
    final_output_string = "\n".join(file_output)

    # 3a. Print the final output to the terminal
    print(final_output_string)

    # 3b. Save the final output to the file "as well"
    output_dir = "output"
    output_file = os.path.join(output_dir, "4benchmark_results.txt")
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_output_string)
        print(f"\nBenchmark complete. Results also saved to {output_file}")
    except Exception as e:
        print(f"\nError: Could not save results file to {output_file}")
        print(f"Details: {e}")

if __name__ == "__main__":
    main()