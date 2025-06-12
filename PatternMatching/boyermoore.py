def bad_character_rule(pattern):
    """ Create the bad character rule table. """
    bad_char = {}
    for i, char in enumerate(pattern):
        bad_char[char] = i  # Store the last occurrence of each character
    return bad_char

def good_suffix_rule(pattern):
    """ Create the good suffix rule table. """
    m = len(pattern)
    suffix = [-1] * m
    good_suffix = [0] * (m + 1)

    # Calculate the suffixes
    for i in range(m - 1):
        j = i
        while j >= 0 and pattern[j] == pattern[m - 1 - (i - j)]:
            j -= 1
            suffix[i - j] = j + 1

    # Fill good_suffix table
    for i in range(m):
        good_suffix[i + 1] = suffix[i]
    for i in range(m):
        if suffix[i] == -1:
            good_suffix[i + 1] = m
        else:
            good_suffix[i + 1] = min(good_suffix[i + 1], m - suffix[i] - 1)

    return good_suffix

def boyer_moore_search(text, pattern):
    """ Perform the Boyer-Moore search. """
    m = len(pattern)
    n = len(text)
    
    if m == 0:
        return []

    bad_char = bad_character_rule(pattern)
    good_suffix = good_suffix_rule(pattern)

    matches = []
    s = 0  # Shift of the pattern with respect to text

    while s <= n - m:
        j = m - 1  # Start comparing from the end of the pattern
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        
        if j < 0:  # A match was found
            matches.append(s)
            s += good_suffix[0]  # Shift by good suffix rule
        else:
            # Shift by bad character rule or good suffix rule
            bad_char_shift = bad_char.get(text[s + j], -1)
            good_suffix_shift = good_suffix[j + 1]
            s += max(j - bad_char_shift, good_suffix_shift)

    return matches

# Example usage
if __name__ == "__main__":
    text = "ababcababcabc"
    pattern = "abc"
    matches = boyer_moore_search(text, pattern)

    print("Pattern found at indices:", matches)
