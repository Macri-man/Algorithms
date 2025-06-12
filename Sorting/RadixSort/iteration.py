def counting_sort_for_radix(arr, exp):
    n = len(arr)
    output = [0] * n  # Output array to store sorted numbers
    count = [0] * 10  # Count array for each digit (0-9)

    # Count occurrences of each digit
    for num in arr:
        index = (num // exp) % 10
        count[index] += 1

    # Update count[i] to store actual positions
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array using the count array
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    # Copy the output array back to the original array
    for i in range(n):
        arr[i] = output[i]

def radix_sort_iterative(arr):
    if len(arr) == 0:
        return arr

    # Find the maximum number to determine the number of digits
    max_num = max(arr)
    exp = 1

    # Perform counting sort for each digit
    while max_num // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10

    return arr

if __name__ == "__main__":
    # Example usage
    arr = [170, 45, 75, 90, 802, 24, 2, 66]
    print("Sorted array:", radix_sort_iterative(arr))
