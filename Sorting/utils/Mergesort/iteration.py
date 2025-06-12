def merge_sort_iterative(arr, capture):
    if len(arr) <= 1:
        return arr

    # Initial chunk size
    step = 1

    # Iteratively merge pairs of elements
    while step < len(arr):
        new_sorted_sublists = []

        # Merge pairs of adjacent chunks
        for i in range(0, len(arr), 2 * step):
            # Get the left and right chunks
            left = arr[i:i + step]
            right = arr[i + step:i + 2 * step]

            # Merge the left and right chunks
            merged = []
            i_left, i_right = 0, 0

            # Merge the two sorted chunks
            while i_left < len(left) and i_right < len(right):
                if left[i_left] <= right[i_right]:
                    merged.append(left[i_left])
                    i_left += 1
                else:
                    merged.append(right[i_right])
                    i_right += 1

            # Append remaining elements
            merged.extend(left[i_left:])
            merged.extend(right[i_right:])

            # Append the merged chunk to the new list
            new_sorted_sublists.append(merged)
            # Update arr with the new sorted chunks
            arr = [item for sublist in new_sorted_sublists for item in sublist]
        
            # Capture the current merged state
            capture(arr)
    

       

        # Double the step size for the next iteration
        step *= 2

    # The final sorted list is in arr
    return arr

if __name__ == "__main__":
    # Example usage
    arr = [12, 11, 13, 5, 6, 7]
    print("Sorted array:", merge_sort_iterative(arr, print))  # Use `print` to visualize each step
