import sys
import random
import time
from collections import Counter

# -----------------------------
# Normalize input (lowercase, keep only letters/spaces)
# -----------------------------
def normalize(s: str) -> str:
    t = []
    for c in s:
        if c.isalpha():
            t.append(c.lower())
        elif c == ' ':
            t.append(' ')
    return ''.join(t)

# -----------------------------
# Frequency count
# -----------------------------
def freq_count(s: str):
    f = [0] * 26
    for c in s:
        if 'a' <= c <= 'z':
            f[ord(c) - ord('a')] += 1
    return f

# -----------------------------
# Apply mapping to ciphertext
# -----------------------------
def apply_map(ct: str, mapping: list[str]) -> str:
    res = []
    for c in ct:
        if 'a' <= c <= 'z':
            res.append(mapping[ord(c) - ord('a')])
        else:
            res.append(c)
    return ''.join(res)

# -----------------------------
# Word-based scoring function
# -----------------------------
def word_score(s: str) -> int:
    common_words = [" the ", " and ", " to ", " of ", " that ", " is ", " in ", " it ", " a "]
    T = f" {s} "
    sc = 0
    for w in common_words:
        start = 0
        while True:
            pos = T.find(w, start)
            if pos == -1:
                break
            sc += 1
            start = pos + len(w)
    return sc

def score_text(plain: str) -> int:
    return word_score(plain)

# -----------------------------
# Initial mapping by frequency
# -----------------------------
def initial_map_by_freq(ct: str) -> list[str]:
    f = freq_count(ct)
    v = sorted([(f[i], i) for i in range(26)], reverse=True)
    eng_order = "etaoinshrdlcumwfgypbvkjxqz"
    mapping = ['x'] * 26
    for i in range(26):
        cidx = v[i][1]
        mapping[cidx] = eng_order[i]
    return mapping

# -----------------------------
# Main solver
# -----------------------------
def main():
    # Read ciphertext (either piped or from a file)
    ciphertext = sys.stdin.read().strip()
    if not ciphertext:
        print("Provide ciphertext via stdin or file input.")
        return

    ciphertext = normalize(ciphertext)

    # Initial mapping and scoring
    best_map = initial_map_by_freq(ciphertext)
    best_plain = apply_map(ciphertext, best_map)
    best_score = score_text(best_plain)

    rng = random.Random(time.time())

    # Hill-climbing (swap-based)
    for _ in range(30000):
        a, b = rng.randint(0, 25), rng.randint(0, 25)
        if a == b:
            continue
        trial = best_map[:]
        trial[a], trial[b] = trial[b], trial[a]
        trial_plain = apply_map(ciphertext, trial)
        sc = score_text(trial_plain)
        if sc > best_score:
            best_score = sc
            best_map = trial
            best_plain = trial_plain

    print("===== Decrypted guess (may be imperfect) =====")
    print(best_plain)
    print("\n===== Mapping (cipher letter -> plain letter) =====")
    for i in range(26):
        print(f"{chr(ord('a')+i)} -> {best_map[i]}")

if __name__ == "__main__":
    main()


