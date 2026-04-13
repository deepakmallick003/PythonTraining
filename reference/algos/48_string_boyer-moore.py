def create_bad_char_table(pattern):
    table = {}
    m = len(pattern)
    for i in range(m):
        table[pattern[i]] = max(1, m - i - 1)
    return table

def boyer_moore_search(text, pattern):
    bad_char_table = create_bad_char_table(pattern)
    m = len(pattern)
    n = len(text)
    
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        
        if j < 0:
            print(f"Pattern found at index {i}")
            i += m
        else:
            i += max(1, j - bad_char_table.get(text[i + j], -1))

text = "LO LOELLO O HELLO"
pattern = "HELLO"

text="GCAATGCCTATGTGACC"
pattern="TATGTG"
boyer_moore_search(text, pattern)
