def merge_iterative(left, right):
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

def merge_sort_iterative(arr):
    if not arr:
        return arr

    # Start with each element as its own sorted array
    sorted_sublists = [[num] for num in arr]

    # Iteratively merge pairs of sublists
    while len(sorted_sublists) > 1:
        new_sorted_sublists = []
        for i in range(0, len(sorted_sublists), 2):
            left = sorted_sublists[i]
            right = sorted_sublists[i + 1] if i + 1 < len(sorted_sublists) else []
            new_sorted_sublists.append(merge_iterative(left, right))
        sorted_sublists = new_sorted_sublists

    return sorted_sublists[0]

if __name__ == "__main__":
    # Example usage
    arr = [12, 11, 13, 5, 6, 7]
    print("Sorted array:", merge_sort_iterative(arr))
