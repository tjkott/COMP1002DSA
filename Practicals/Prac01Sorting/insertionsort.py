def insertion_sort(arr):
    # Outer loop begins from 2nd element / index 1. 
    for i in range(1, len(arr)):
        current_element = arr[i]
        # position is the index where we will compare and shift elements to.
        position = i #  position is initialised at the current element's index. 
        while position > 0 and arr[position -1] > current_element
            arr[position] = arr[position -1] # shift larger element to the right. 
            position = position -1 # keep moving left until we find the correct position.
        arr[position] = current_element # place the current_element in its correct position. 