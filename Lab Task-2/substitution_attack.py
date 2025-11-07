# ✅ Checkpoint 2: Substitution Cipher (Frequency Analysis)
# Course: CSE-478 - Introduction to Computer Security Lab
# Lab 2 - Attacking Classic Crypto Systems

from collections import Counter

# Paste Cipher-1 text here
cipher1 = """af p xpkcaqvnpk pfg, af ipqe qpri, gauuikifc tpw, ceiri udvk tiki afgarxifrphni cd eao-
wvmd popkwn, hiqpvri du ear jvaql vfgikrcpfgafm du cei xkafqaxnir du xrwqedearcdkw pfg 
du ear aopmafpcasi xkdhafmr afcd fit pkipr. ac tpr qdoudkcafm cd lfdt cepc au pfwceafm 
epxxifig cd ringdf eaorinu hiudki cei opceiopcaqr du cei uaing qdvng hi qdoxnicinw tdklig dvc-
pfg edt rndtnw ac xkdqiigig, pfg edt odvfcpafdvr cei dhrcpqnir--ceiki tdvng pc niprc kiopaf dfi 
mddg oafg cepc tdvng qdfcafvi cei kiripkqe"""

# Count frequency of letters
freq = Counter([ch for ch in cipher1 if ch.isalpha()])
print("🔹 Frequency of letters in Cipher-1:\n", freq)

# Sort by frequency
freq_sorted = sorted(freq.items(), key=lambda x: x[1], reverse=True)
print("\n🔹 Letters sorted by frequency:\n", freq_sorted)

# Step 1: Replace common cipher letters with likely English letters (manually refine)
# Example replacements (you can adjust as you decode)
decoded = cipher1
decoded = decoded.replace('a', 't')
decoded = decoded.replace('f', 'h')
decoded = decoded.replace('p', 'e')
decoded = decoded.replace('g', 'r')
decoded = decoded.replace('i', 'a')
decoded = decoded.replace('e', 'n')

print("\n🔹 Partial Decoding Attempt:\n")
print(decoded)
