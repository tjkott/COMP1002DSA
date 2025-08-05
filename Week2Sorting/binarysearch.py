def BinarySearch(sorted_arr, target_val):
    """
    Finds target value from a sorted_array using binary search algorithm. 
    """
    lower_boundary = 0
    upper_boundary = len(sorted_arr) - 1

    while lower_boundary <= upper_boundary:
        halfway_idx = (lower_boundary + upper_boundary) // 2
        halfway_val = sorted_arr[halfway_idx]

        if halfway_val < target_val:
            # If halfway value is too low, becomes the new lower bound.
            lower_boundary = halfway_idx + 1
        elif halfway_val > target_val:
            # If halfway value is too high, becomes the new upper bound. 
            upper_boundary = halfway_idx - 1
        else:
            # if the middle value is equal to target we have found it
            return halfway_idx 

if __name__ = "__main__":
    sorted_array = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target_to_find = 23
    result = BinarySearch(sorted_array, target_to_find)