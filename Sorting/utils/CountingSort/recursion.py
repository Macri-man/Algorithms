def counting_sort_recursive(arr):
    if not arr:
        return []

    # Helper function to calculate counts
    def count_elements(arr, count, min_val):
        if not arr:
            return count
        count[arr[0] - min_val] += 1
        return count_elements(arr[1:], count, min_val)

    # Helper function to calculate prefix sums
    def calculate_positions(count, idx=1):
        if idx == len(count):
            return count
        count[idx] += count[idx - 1]
        return calculate_positions(count, idx + 1)

    # Helper function to build the sorted output
    def build_sorted(arr, output, count, min_val):
        if not arr:
            return output
        num = arr[-1]
        pos = count[num - min_val] - 1
        output[pos] = num
        count[num - min_val] -= 1
        return build_sorted(arr[:-1], output, count, min_val)

    # Find range
    max_val = max(arr)
    min_val = min(arr)
    range_of_elements = max_val - min_val + 1

    # Initialize count and output arrays
    count = [0] * range_of_elements
    output = [0] * len(arr)

    # Count elements
    count = count_elements(arr, count, min_val)

    # Calculate positions
    count = calculate_positions(count)

    # Build sorted array
    return build_sorted(arr, output, count, min_val)

if __name__ == "__main__":
    # Example usage
    arr = [4, 2, 2, 8, 3, 3, 1]
    print("Sorted array:", counting_sort_recursive(arr))
