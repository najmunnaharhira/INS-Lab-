
#!/usr/bin/env python3
"""
caesar_attack.py

Break a Caesar (shift) cipher by brute force and rank candidate plaintexts
using a simple common-words heuristic.

Usage:
    python caesar_attack.py "odroboewscdrolocdcwkbdmyxdbkmdzvkdpybwyeddrobo"
    python caesar_attack.py -f cipher.txt
    python caesar_attack.py -n 8 "ciphertext..."
"""

from __future__ import annotations
import sys
import argparse
import string

COMMON_WORDS = {
    "the","and","to","of","a","in","is","that","it","you","for",
    "on","with","as","are","this","be","or","by","from","at","an"
}

def caesar_shift(s: str, shift: int) -> str:
    out = []
    for ch in s:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch) - base - shift) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)

def score_english(text: str) -> float:
    tokens = [w.strip(string.punctuation).lower() for w in text.split()]
    if not tokens:
        return 0.0
    hits = sum(1 for w in tokens if w in COMMON_WORDS)
    return hits / len(tokens)

def brute_force(ciphertext: str):
    results = []
    for shift in range(26):
        pt = caesar_shift(ciphertext, shift)
        score = score_english(pt)
        results.append((shift, score, pt))
    # sort by score desc, then by shift
    results.sort(key=lambda x: (-x[1], x[0]))
    return results

def print_all_shifts(ciphertext: str):
    print("All 26 shifts (shift = key; plaintext = ciphertext shifted BACK by key):\n")
    for shift in range(26):
        print(f"Shift {shift:2}: {caesar_shift(ciphertext, shift)}")
    print()

def main():
    parser = argparse.ArgumentParser(description="Attack a Caesar cipher by brute force")
    parser.add_argument("input", nargs="?", help="Ciphertext string (or use -f)")
    parser.add_argument("-f", "--file", help="Read ciphertext from a file")
    parser.add_argument("-n", "--candidates", type=int, default=6, help="Show top N candidates")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                ciphertext = fh.read().strip()
        except Exception as e:
            print("Error reading file:", e)
            sys.exit(1)
    elif args.input:
        ciphertext = args.input.strip()
    else:
        parser.print_help()
        sys.exit(1)

    if not ciphertext:
        print("Empty ciphertext.")
        sys.exit(1)

    print("\nCiphertext:\n")
    print(ciphertext + "\n")
    print_all_shifts(ciphertext)

    candidates = brute_force(ciphertext)
    n = max(1, min(len(candidates), args.candidates))
    print(f"Top {n} candidate decryptions (ranked by common-word score):\n")
    for i, (shift, score, pt) in enumerate(candidates[:n], 1):
        print(f"{i:2}. Shift={shift:2}  score={score:.3f}  plaintext: {pt}")
    print("\nInspect candidates for proper English to find the correct shift.\n")

if __name__ == "__main__":
    main()
