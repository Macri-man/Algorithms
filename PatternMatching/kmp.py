def compute_prefix_function(pattern):
    m = len(pattern)
    lps = [0] * m  # Longest prefix which is also a suffix
    length = 0  # Length of the previous longest prefix suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]  # Use the previous prefix
            else:
                lps[i] = 0
                i += 1
    
    return lps

def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    
    lps = compute_prefix_function(pattern)  # Preprocess the pattern
    i = 0  # Index for text
    j = 0  # Index for pattern
    matches = []  # Store positions of matches

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:  # Match found
            matches.append(i - j)  # Store the starting index of the match
            j = lps[j - 1]  # Use lps to find next match
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]  # Use the lps table to skip comparisons
            else:
                i += 1  # Move to the next character in the text
    
    return matches

# Example usage
if __name__ == "__main__":
    text = "ababcababcabc"
    pattern = "abc"
    matches = kmp_search(text, pattern)

    print("Pattern found at indices:", matches)
