def counting_sort_iterative(arr):
    if not arr:
        return []

    # Find the range of the elements in the array
    max_val = max(arr)
    min_val = min(arr)
    range_of_elements = max_val - min_val + 1

    # Initialize the count array
    count = [0] * range_of_elements

    # Count the occurrences of each element
    for num in arr:
        count[num - min_val] += 1

    # Transform count into a prefix sum array for positions
    for i in range(1, range_of_elements):
        count[i] += count[i - 1]

    # Build the sorted array
    output = [0] * len(arr)
    for num in reversed(arr):  # Traverse in reverse to maintain stability
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1

    return output

if __name__ == "__main__":
    # Example usage
    arr = [4, 2, 2, 8, 3, 3, 1]
    print("Sorted array:", counting_sort_iterative(arr))
