def bucket_sort_recursive(arr, num_buckets=None, depth=0):
    if len(arr) <= 1 or depth > 10:  # Base case: Single element or max recursion depth
        return arr

    if num_buckets is None:
        num_buckets = len(arr)

    # Step 1: Create buckets
    max_value = max(arr)
    buckets = [[] for _ in range(num_buckets)]

    # Step 2: Distribute elements into buckets
    for value in arr:
        index = int(value * num_buckets / (max_value + 1))  # Map to a bucket index
        buckets[index].append(value)

    # Step 3: Sort each bucket recursively and concatenate
    sorted_array = []
    for bucket in buckets:
        if len(bucket) > 1:
            sorted_array.extend(bucket_sort_recursive(bucket, num_buckets, depth + 1))
        else:
            sorted_array.extend(bucket)

    return sorted_array

if __name__ == "__main__":
    # Example Usage
    arr = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47]
    print("Recursive Bucket Sort:", bucket_sort_recursive(arr))
