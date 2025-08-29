def bubble_sort(unsorted_arr):
    n = len(unsorted_arr)
    # We need n - 1 passes to guarantee list is sorted
    for pass_num in range (n-1):
        for i in range(n -1 - pass_num):
            # ii loop in the pseudocode. 
            # n-1-pass_num: range of this loop decreases with each pass. 

            if unsorted_arr[i] > unsorted_arr[i + 1]:
                # Swap the elements
                unsorted_arr[i], unsorted_arr[i + 1] = unsorted_arr[i + 1], unsorted_arr[i]
        