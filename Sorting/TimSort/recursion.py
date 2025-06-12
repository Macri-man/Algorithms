def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    L = arr[left:left + n1]
    R = arr[mid + 1:mid + 1 + n2]

    i = j = 0
    k = left
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def tim_sort_recursive(arr, left, right, min_run):
    n = len(arr)

    # Step 1: Sort small chunks (runs) using Insertion Sort
    for i in range(left, right, min_run):
        insertion_sort(arr, i, min(i + min_run - 1, n - 1))

    # Step 2: Recursively merge runs
    size = min_run
    while size < n:
        for start in range(0, n, 2 * size):
            mid = min(n - 1, start + size - 1)
            end = min((start + 2 * size - 1), (n - 1))
            if mid < end:
                merge(arr, start, mid, end)
        size *= 2

    return arr

def tim_sort_recursive_entry(arr):
    return tim_sort_recursive(arr, 0, len(arr), 32)

if __name__ == "__main__":
    # Example Usage
    arr = [5, 21, 7, 23, 19]
    print("Recursive Tim Sort:", tim_sort_recursive_entry(arr))
