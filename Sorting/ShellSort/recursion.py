def shell_sort_recursive(arr, gap):
    if gap == 0:
        return  # Base case: When gap becomes 0, sorting is complete.

    # Perform a gap-based insertion sort
    for i in range(gap, len(arr)):
        temp = arr[i]
        j = i
        while j >= gap and arr[j - gap] > temp:
            arr[j] = arr[j - gap]
            j -= gap
        arr[j] = temp

    # Recursive call with a reduced gap size
    shell_sort_recursive(arr, gap // 2)

if __name__ == "__main__":

    # Example Usage
    arr = [12, 34, 54, 2, 3]
    initial_gap = len(arr) // 2
    shell_sort_recursive(arr, initial_gap)
    print("Recursive Shell Sort:", arr)