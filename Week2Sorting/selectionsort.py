def selection_sort(arr):
    n = len(arr) # total number of elements in the arry

    for i in range(n):
        min_idx = i # assume that the the first element of the unsorted array is its minimum. 

        for j in range(i + 1, n): 
            # iterate through the unsorted part of the array to find the actual nimimum. 
            if arr[j] < arr[min_idx]:
                # Swap the found minimum element with the first element of the unsorted part.
                min_idx = j
            # now min_idx holds the index of the mimum in the unsorted part of the array. 

        # swap the minimum element with the first element of the unsorted part.
        arr[i], arr[min_idx] = arr[min_idx], arr[i] 