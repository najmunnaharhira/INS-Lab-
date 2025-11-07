# ✅ Checkpoint 1: Caesar Cipher Decryption (Brute Force Method)
# Course: CSE-478 - Introduction to Computer Security Lab
# Lab 2 - Attacking Classic Crypto Systems

# Cipher text
cipher = "odroboewscdrolocdcwkbdmyxdbkmdzvkdpybwyeddrobo"

# Try all 26 possible shifts
for shift in range(26):
    plain = ""
    for char in cipher:
        if char.isalpha():
            plain += chr((ord(char) - 97 - shift) % 26 + 97)
        else:
            plain += char
    print(f"Shift {shift}: {plain}")
