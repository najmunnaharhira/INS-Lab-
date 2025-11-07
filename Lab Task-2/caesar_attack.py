
from collections import Counter
import sys

cipher = "odroboewscdrolocdcwkbdmyxdbkmdzvkdpybwyeddrobo"

def shift_text(s, sh):
    out = []
    for ch in s:
        if 'a' <= ch <= 'z':
            out.append(chr((ord(ch) - ord('a') - sh) % 26 + ord('a')))
        elif 'A' <= ch <= 'Z':
            out.append(chr((ord(ch) - ord('A') - sh) % 26 + ord('A')))
        else:
            out.append(ch)
    return ''.join(out)

def score_text(t):
    words = ["the","and","to","of","that","is","in","it","you","he","was","for","on","are","as","with"]
    lower = t.lower()
    sc = 0
    for w in words:
        pos = 0
        while True:
            pos = lower.find(w, pos)
            if pos == -1:
                break
            # word boundaries
            left_ok = (pos == 0) or (not lower[pos-1].isalnum())
            right_ok = (pos + len(w) == len(lower)) or (not lower[pos+len(w)].isalnum())
            if left_ok and right_ok:
                sc += 1
            pos += len(w)
    for c in lower:
        if c in "etaoin":
            sc += 1
    return sc

candidates = []
for sh in range(26):
    plain = shift_text(cipher, sh)
    sc = score_text(plain)
    candidates.append((sc, sh, plain))
    print(f"Shift {sh}: {plain}")

best = max(candidates, key=lambda x: x[0])
print("\n====== Best candidate (score: {}) ======".format(best[0]))
print(best[2])
