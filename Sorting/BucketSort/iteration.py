def bucket_sort_iterative(arr):
    if len(arr) == 0:
        return arr

    # Step 1: Create buckets
    num_buckets = len(arr)
    max_value = max(arr)
    buckets = [[] for _ in range(num_buckets)]

    # Step 2: Distribute elements into buckets
    for value in arr:
        index = int(value * num_buckets / (max_value + 1))  # Map to a bucket index
        buckets[index].append(value)

    # Step 3: Sort each bucket and concatenate results
    sorted_array = []
    for bucket in buckets:
        sorted_array.extend(sorted(bucket))  # Using built-in sort for simplicity

    return sorted_array

if __name__ == "__main__":
    # Example Usage
    arr = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47]
    print("Iterative Bucket Sort:", bucket_sort_iterative(arr))
