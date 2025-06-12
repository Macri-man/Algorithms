def merge_recursive(left, right):
    result = []
    i = j = 0

    # Merge the two arrays
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append the remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort_recursive(arr):
    # Base case: An array with 0 or 1 element is already sorted
    if len(arr) <= 1:
        return arr

    # Split the array into two halves
    mid = len(arr) // 2
    left = merge_sort_recursive(arr[:mid])
    right = merge_sort_recursive(arr[mid:])

    # Merge the sorted halves
    return merge_recursive(left, right)

if __name__ == "__main__":
    # Example usage
    arr = [12, 11, 13, 5, 6, 7]
    print("Sorted array:", merge_sort_recursive(arr))
