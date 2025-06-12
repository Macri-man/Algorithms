def rabin_karp_search(text, pattern):
    """ Perform the Rabin-Karp search. """
    d = 256  # Number of characters in the input alphabet
    q = 101  # A prime number for the modulus
    m = len(pattern)
    n = len(text)
    p = 0  # Hash value for the pattern
    t = 0  # Hash value for the text
    h = 1  # The value of d^(m-1)

    # The value of h would be "pow(d, m-1)%q"
    for i in range(m - 1):
        h = (h * d) % q

    # Calculate the hash value of pattern and first window of text
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    matches = []

    # Slide the pattern over text
    for i in range(n - m + 1):
        # Check the hash values of the current window of text and pattern
        if p == t:
            # Check for actual match (to handle hash collisions)
            if text[i:i + m] == pattern:
                matches.append(i)
        
        # Calculate the hash value for the next window of text
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            # We might get negative value of t, converting it to positive
            if t < 0:
                t += q

    return matches

# Example usage
if __name__ == "__main__":
    text = "ababcababcabc"
    pattern = "abc"
    matches = rabin_karp_search(text, pattern)

    print("Pattern found at indices:", matches)
