#!/usr/bin/env python3
"""
substitution_attack.py

Helpers and a simple hill-climbing routine to attack monoalphabetic substitution ciphers.

Features:
- Frequency analysis helper
- Heuristic initial mapping (cipher frequency -> English frequency order)
- Simple hill-climbing (random swaps) to refine mapping using a small-word scoring function
- Interactive mode to apply manual mappings

Usage:
    python substitution_attack.py -t "ciphertext..."
    python substitution_attack.py -f cipher.txt --auto
    python substitution_attack.py -t "..." --interactive
"""

from __future__ import annotations
import argparse
import string
import random
from collections import Counter

ENGLISH_FREQ_ORDER = "etaoinshrdlcumwfgypbvkjxqz"
COMMON_WORDS = {
    "the","and","to","of","a","in","is","that","it","you","for","on","with",
    "as","are","this","was","be","by","he","she","we","they","not","or","an",
    "from","at","but","have","has","had","his","her","which","their","will"
}

def clean_text(text: str) -> str:
    return "".join(ch.lower() for ch in text if ch.isalpha() or ch.isspace())

def frequency_table(text: str):
    letters = [c for c in text.lower() if c.isalpha()]
    total = len(letters)
    freq = Counter(letters)
    return [(ch, freq.get(ch, 0), (freq.get(ch, 0) / total if total else 0.0)) for ch in string.ascii_lowercase]

def show_freq(table):
    print("Letter  Count  Freq")
    for ch, cnt, fr in table:
        print(f"{ch:>2}     {cnt:>4}   {fr:.4f}")
    print()

def initial_freq_mapping(ciphertext: str):
    table = frequency_table(ciphertext)
    table_sorted = sorted(table, key=lambda x: -x[1])
    mapping = {}
    for i, (ch, cnt, fr) in enumerate(table_sorted):
        mapping[ch] = ENGLISH_FREQ_ORDER[i] if i < len(ENGLISH_FREQ_ORDER) else '?'
    return mapping

def apply_mapping(ciphertext: str, mapping: dict) -> str:
    out = []
    for ch in ciphertext:
        if ch.isalpha():
            lower = ch.lower()
            if lower in mapping and mapping[lower] != '?':
                out_ch = mapping[lower]
                out.append(out_ch.upper() if ch.isupper() else out_ch)
            else:
                out.append('?')
        else:
            out.append(ch)
    return "".join(out)

def mapping_to_key(mapping: dict) -> str:
    return "".join(mapping.get(ch, '?') for ch in string.ascii_lowercase)

def key_to_mapping(key: str) -> dict:
    return {ch: key[i] for i, ch in enumerate(string.ascii_lowercase)}

def score_plaintext(plaintext: str) -> float:
    tokens = [w.strip(string.punctuation).lower() for w in plaintext.split()]
    if not tokens:
        return -999.0
    hits = sum(1 for w in tokens if w in COMMON_WORDS)
    unknowns = plaintext.count('?')
    # score: reward common words per token, penalize unknown chars
    return (hits / len(tokens)) - (unknowns * 0.01)

def random_swap_key(key: str) -> str:
    lst = list(key)
    i, j = random.sample(range(26), 2)
    lst[i], lst[j] = lst[j], lst[i]
    return "".join(lst)

def hill_climb(ciphertext: str, start_key: str | None = None, iterations: int = 2000, restarts: int = 4):
    best_key = None
    best_plain = None
    best_score = float("-inf")

    for r in range(restarts):
        if start_key:
            key = start_key
        else:
            mapping = initial_freq_mapping(ciphertext)
            key = mapping_to_key(mapping)

        current_key = key
        current_mapping = key_to_mapping(current_key)
        current_plain = apply_mapping(ciphertext, current_mapping)
        current_score = score_plaintext(current_plain)

        for it in range(iterations):
            new_key = random_swap_key(current_key)
            new_mapping = key_to_mapping(new_key)
            new_plain = apply_mapping(ciphertext, new_mapping)
            new_score = score_plaintext(new_plain)
            if new_score > current_score:
                current_key, current_plain, current_score = new_key, new_plain, new_score

        if current_score > best_score:
            best_score = current_score
            best_key = current_key
            best_plain = current_plain

    return best_key, best_plain, best_score

def interactive_mode(ciphertext: str):
    table = frequency_table(ciphertext)
    show_freq(table)

    mapping = initial_freq_mapping(ciphertext)
    print("Initial mapping (cipher -> plain):")
    for c in sorted(mapping.keys()):
        print(f"{c} -> {mapping[c]}", end="   ")
    print("\n\nPlaintext after heuristic mapping:\n")
    print(apply_mapping(ciphertext, mapping))
    print("\nCommands:  a=t  (set mapping), swap x y, auto, show, freq, score, quit\n")

    while True:
        cmd = input("cmd> ").strip()
        if not cmd:
            continue
        if cmd.lower() in ("q", "quit", "exit"):
            print("\nFinal plaintext:\n")
            print(apply_mapping(ciphertext, mapping))
            return
        if cmd.lower() == "freq":
            show_freq(table)
            continue
        if cmd.lower() == "show":
            print(apply_mapping(ciphertext, mapping))
            continue
        if cmd.lower() == "score":
            print("score:", score_plaintext(apply_mapping(ciphertext, mapping)))
            continue
        if cmd.lower() == "auto":
            start_key = mapping_to_key(mapping)
            print("Running hill-climb (this can take a few seconds)...")
            best_key, best_plain, best_score = hill_climb(ciphertext, start_key=start_key, iterations=3000, restarts=6)
            mapping = key_to_mapping(best_key)
            print(f"\nAuto-refined (score {best_score:.4f}):\n")
            print(best_plain)
            continue
        if "=" in cmd:
            parts = cmd.split()
            for part in parts:
                if "=" not in part:
                    continue
                a, b = part.split("=", 1)
                a = a.strip().lower()
                b = b.strip().lower()
                if len(a) != 1 or len(b) != 1 or a not in string.ascii_lowercase or b not in string.ascii_lowercase:
                    print("Invalid mapping part:", part)
                    continue
                # ensure one-to-one: remove b from any other mapping first
                for k, v in list(mapping.items()):
                    if v == b:
                        mapping[k] = '?'
                mapping[a] = b
            print("Applied mapping. Current plaintext:")
            print(apply_mapping(ciphertext, mapping))
            continue
        if cmd.lower().startswith("swap "):
            toks = cmd.split()
            if len(toks) != 3:
                print("swap requires two ciphertext letters: swap x y")
                continue
            x, y = toks[1].lower(), toks[2].lower()
            if x not in string.ascii_lowercase or y not in string.ascii_lowercase:
                print("invalid letters")
                continue
            mapping[x], mapping[y] = mapping[y], mapping[x]
            print("Swapped. Current plaintext:")
            print(apply_mapping(ciphertext, mapping))
            continue
        print("Unknown command.")

def parse_args():
    p = argparse.ArgumentParser(description="Substitution cipher helper/attack")
    p.add_argument("-t", "--text", help="Ciphertext string")
    p.add_argument("-f", "--file", help="Read ciphertext from file")
    p.add_argument("--auto", action="store_true", help="Run automatic hill-climb and print best result")
    p.add_argument("--interactive", action="store_true", help="Interactive mapping mode")
    p.add_argument("--iters", type=int, default=3000, help="Iterations per hill-climb run")
    p.add_argument("--restarts", type=int, default=6, help="Restarts for hill-climb")
    return p.parse_args()

def main():
    args = parse_args()
    if args.file:
        with open(args.file, "r", encoding="utf-8") as fh:
            ciphertext = fh.read().strip()
    elif args.text:
        ciphertext = args.text.strip()
    else:
        print("Provide ciphertext with -t or -f. Use -h for help.")
        return

    print("\nCiphertext (first 300 chars):\n")
    print(ciphertext[:300] + ("\n..." if len(ciphertext) > 300 else "\n"))

    table = frequency_table(ciphertext)
    print("\nFrequency analysis:\n")
    show_freq(table)

    mapping = initial_freq_mapping(ciphertext)
    print("Initial heuristic mapping (cipher -> plain):")
    for c in sorted(mapping.keys()):
        print(f"{c} -> {mapping[c]}", end="   ")
    print("\n\nPlaintext after heuristic mapping:\n")
    print(apply_mapping(ciphertext, mapping))
    print("\nScore:", score_plaintext(apply_mapping(ciphertext, mapping)))

    if args.auto:
        print("\nRunning automatic hill-climb refinement...")
        start_key = mapping_to_key(mapping)
        best_key, best_plain, best_score = hill_climb(ciphertext, start_key=start_key, iterations=args.iters, restarts=args.restarts)
        print(f"\nBest result (score {best_score:.4f}):\n")
        print(best_plain)
        print("\nKey (cipher a..z -> plaintext letters):")
        print(best_key)
        return

    if args.interactive:
        interactive_mode(ciphertext)
        return

if __name__ == "__main__":
    main()
