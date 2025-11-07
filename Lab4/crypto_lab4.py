
#!/usr/bin/env python3
"""
crypto_lab4.py

CSE-478 Lab 4 — Programming Symmetric & Asymmetric Cryptography
Features:
 - AES (ECB and CFB) encrypt/decrypt (AES-128 and AES-256)
 - RSA key generation, encrypt/decrypt (OAEP)
 - RSA signature & verification (PSS)
 - SHA-256 hashing
 - Timing measurements for AES and RSA (plots saved to graphs/)
"""

import os
import sys
import time
import hashlib
import argparse
from pathlib import Path

# Crypto imports
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import constant_time
from cryptography.exceptions import InvalidSignature

# Plotting
import matplotlib.pyplot as plt

# -----------------------
# Paths and Helpers
# -----------------------
ROOT = Path.cwd()
KEYS_DIR = ROOT / "keys"
FILES_DIR = ROOT / "files"
GRAPHS_DIR = ROOT / "graphs"

for d in (KEYS_DIR, FILES_DIR, GRAPHS_DIR):
    d.mkdir(parents=True, exist_ok=True)

def save_bytes(path: Path, data: bytes):
    path.write_bytes(data)
    print(f"[+] Wrote {path}")

def read_bytes(path: Path) -> bytes:
    return path.read_bytes()

def rand_bytes(n: int) -> bytes:
    return os.urandom(n)

# -----------------------
# AES (symmetric)
# -----------------------
def generate_aes_key(key_size_bytes: int) -> bytes:
    key = rand_bytes(key_size_bytes)
    return key

def save_aes_key(key: bytes, filename: str):
    save_bytes(KEYS_DIR / filename, key)

def load_aes_key(filename: str) -> bytes:
    return read_bytes(KEYS_DIR / filename)

def aes_encrypt(plaintext: bytes, key: bytes, mode_name: str = "CFB") -> dict:
    """
    Returns dict with fields: ciphertext, iv (maybe None), mode
    For ECB, iv is None.
    """
    if mode_name.upper() == "ECB":
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        # Need PKCS7 padding for ECB
        padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
        padded = padder.update(plaintext) + padder.finalize()
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded) + encryptor.finalize()
        return {"ciphertext": ct, "iv": None, "mode": "ECB"}
    elif mode_name.upper() == "CFB":
        iv = rand_bytes(algorithms.AES.block_size // 8)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(plaintext) + encryptor.finalize()
        return {"ciphertext": ct, "iv": iv, "mode": "CFB"}
    else:
        raise ValueError("Unsupported AES mode. Use 'ECB' or 'CFB'.")

def aes_decrypt(ciphertext: bytes, key: bytes, mode_name: str = "CFB", iv: bytes = None) -> bytes:
    if mode_name.upper() == "ECB":
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
        pt = unpadder.update(padded) + unpadder.finalize()
        return pt
    elif mode_name.upper() == "CFB":
        if iv is None:
            raise ValueError("CFB requires IV")
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        pt = decryptor.update(ciphertext) + decryptor.finalize()
        return pt
    else:
        raise ValueError("Unsupported AES mode. Use 'ECB' or 'CFB'.")


# -----------------------
# RSA (asymmetric)
# -----------------------
def generate_rsa_keypair(bits: int = 2048, priv_name="rsa_private.pem", pub_name="rsa_public.pem", passphrase: bytes = None):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=bits, backend=default_backend())
    # serialize private
    enc_algo = serialization.BestAvailableEncryption(passphrase) if passphrase else serialization.NoEncryption()
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=enc_algo
    )
    pub_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    save_bytes(KEYS_DIR / priv_name, priv_pem)
    save_bytes(KEYS_DIR / pub_name, pub_pem)
    print(f"[+] Generated RSA {bits}-bit keypair")

def load_rsa_private(filename: str, passphrase: bytes = None):
    data = read_bytes(KEYS_DIR / filename)
    return serialization.load_pem_private_key(data, password=passphrase, backend=default_backend())

def load_rsa_public(filename: str):
    data = read_bytes(KEYS_DIR / filename)
    return serialization.load_pem_public_key(data, backend=default_backend())

def rsa_encrypt(msg: bytes, pubkey) -> bytes:
    ct = pubkey.encrypt(
        msg,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ct

def rsa_decrypt(ciphertext: bytes, privkey) -> bytes:
    pt = privkey.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return pt

def rsa_sign(msg: bytes, privkey) -> bytes:
    signature = privkey.sign(
        msg,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def rsa_verify(msg: bytes, signature: bytes, pubkey) -> bool:
    try:
        pubkey.verify(
            signature,
            msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

# -----------------------
# Hashing / HMAC
# -----------------------
def sha256_hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def hmac_sha256(key: bytes, data: bytes) -> str:
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(data)
    return h.finalize().hex()

# -----------------------
# Timing & Plots
# -----------------------
def measure_aes_times(sizes_bytes, mode="CFB", rounds=20):
    times = []
    for k in sizes_bytes:
        key = rand_bytes(k)
        plaintext = rand_bytes(1024)  # 1 KiB test block
        start = time.perf_counter()
        for i in range(rounds):
            enc = aes_encrypt(plaintext, key, mode_name=mode)
            # decrypt to include both
            _ = aes_decrypt(enc["ciphertext"], key, mode_name=mode, iv=enc.get("iv"))
        end = time.perf_counter()
        avg_ms = (end - start) / rounds * 1000
        times.append(avg_ms)
    return times

def measure_rsa_times(key_sizes_bits, rounds=5):
    enc_times = []
    dec_times = []
    for bits in key_sizes_bits:
        # generate ephemeral keys to measure
        priv = rsa.generate_private_key(public_exponent=65537, key_size=bits, backend=default_backend())
        pub = priv.public_key()
        message = b"timing test: small msg"
        # encryption timing
        start = time.perf_counter()
        for _ in range(rounds):
            _ = rsa_encrypt(message, pub)
        end = time.perf_counter()
        enc_avg = (end - start) / rounds * 1000
        # decryption timing
        c = rsa_encrypt(message, pub)
        start = time.perf_counter()
        for _ in range(rounds):
            _ = rsa_decrypt(c, priv)
        end = time.perf_counter()
        dec_avg = (end - start) / rounds * 1000
        enc_times.append(enc_avg)
        dec_times.append(dec_avg)
    return enc_times, dec_times

def plot_and_save(x_labels, y_values, ylabel, title, filename):
    plt.figure(figsize=(8,5))
    plt.plot(x_labels, y_values, marker='o')
    plt.xlabel("Key size")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    path = GRAPHS_DIR / filename
    plt.savefig(path)
    plt.close()
    print(f"[+] Plot saved to {path}")

# -----------------------
# CLI / Menu
# -----------------------
def menu():
    print("========= CRYPTO LAB 4 =========")
    print("1) AES Encryption/Decryption (ECB/CFB)")
    print("2) RSA Encryption/Decryption")
    print("3) RSA Signature & Verification")
    print("4) SHA-256 Hashing")
    print("5) Measure Execution Time (AES & RSA) & plot")
    print("6) Exit")
    print("================================")

def do_aes_workflow():
    fname = input("Enter plaintext filename (in files/, default sample.txt): ").strip() or "sample.txt"
    fpath = FILES_DIR / fname
    if not fpath.exists():
        print(f"[!] {fpath} not found. Creating a sample file.")
        save_bytes(fpath, b"This is sample text for AES test.\n" * 4)

    key_choice = input("Key size: 16 or 32 bytes? (16): ").strip() or "16"
    key_bytes = int(key_choice)
    if key_bytes not in (16, 32):
        print("[!] Invalid; defaulting to 16")
        key_bytes = 16

    key = generate_aes_key(key_bytes)
    keyfile = f"aes_key_{key_bytes*8}.key"
    save_aes_key(key, keyfile)

    mode = input("Mode (ECB or CFB) [CFB]: ").strip().upper() or "CFB"
    data = read_bytes(fpath)

    enc = aes_encrypt(data, key, mode_name=mode)
    out_name = f"encrypted_aes_{mode.lower()}.bin"
    save_bytes(FILES_DIR / out_name, enc["ciphertext"])
    if enc.get("iv"):
        save_bytes(FILES_DIR / f"{out_name}.iv", enc["iv"])

    print("[*] Decrypting now to verify...")
    iv = enc.get("iv")
    dec = aes_decrypt(enc["ciphertext"], key, mode_name=mode, iv=iv)
    save_bytes(FILES_DIR / "decrypted_aes.txt", dec)
    print("[+] AES roundtrip done.")

def do_rsa_workflow():
    # Generate if not exists
    priv_name = "rsa_private.pem"
    pub_name = "rsa_public.pem"
    if not (KEYS_DIR / priv_name).exists():
        bits = int(input("RSA keysize (bits) [2048]: ") or "2048")
        generate_rsa_keypair(bits=bits, priv_name=priv_name, pub_name=pub_name)
    priv = load_rsa_private(priv_name)
    pub = load_rsa_public(pub_name)

    # choose file
    fname = input("Enter plaintext filename to encrypt (in files/, default sample.txt): ").strip() or "sample.txt"
    fpath = FILES_DIR / fname
    if not fpath.exists():
        save_bytes(fpath, b"Hello RSA sample\n")

    data = read_bytes(fpath)
    ct = rsa_encrypt(data, pub)
    save_bytes(FILES_DIR / "encrypted_rsa.bin", ct)
    pt = rsa_decrypt(ct, priv)
    save_bytes(FILES_DIR / "decrypted_rsa.txt", pt)
    print("[+] RSA encrypt/decrypt done. Compare files to verify.")

def do_rsa_sign_verify():
    priv_name = "rsa_private.pem"
    pub_name = "rsa_public.pem"
    if not (KEYS_DIR / priv_name).exists():
        generate_rsa_keypair(2048, priv_name=priv_name, pub_name=pub_name)
    priv = load_rsa_private(priv_name)
    pub = load_rsa_public(pub_name)

    fname = input("Enter filename to sign (in files/, default sample.txt): ").strip() or "sample.txt"
    fpath = FILES_DIR / fname
    if not fpath.exists():
        save_bytes(fpath, b"Default file to sign.\n")
    data = read_bytes(fpath)
    sig = rsa_sign(data, priv)
    save_bytes(FILES_DIR / "signature.bin", sig)

    verified = rsa_verify(data, sig, pub)
    print(f"[+] Verification result: {verified}")

def do_hashing():
    fname = input("Enter filename to hash (in files/, default sample.txt): ").strip() or "sample.txt"
    fpath = FILES_DIR / fname
    if not fpath.exists():
        save_bytes(fpath, b"Sample for hashing.\n")
    digest = sha256_hash_file(fpath)
    print(f"SHA-256 ({fpath.name}) = {digest}")
    save_bytes(FILES_DIR / "sha256_digest.txt", digest.encode())

    # HMAC demo
    key = rand_bytes(16)
    data = read_bytes(fpath)
    hmac_hex = hmac_sha256(key, data)
    print(f"HMAC-SHA256 (hex): {hmac_hex}")
    save_bytes(FILES_DIR / "hmac_sha256.txt", hmac_hex.encode())

def do_timing_and_plot():
    # AES timing
    aes_key_sizes = [16, 24, 32]  # bytes
    aes_modes = ["CFB", "ECB"]
    for mode in aes_modes:
        aes_times = measure_aes_times(aes_key_sizes, mode=mode, rounds=30)
        labels = [str(k*8) for k in aes_key_sizes]  # bits
        plot_and_save(labels, aes_times, "time (ms)", f"AES {mode} average roundtrip time (1KiB)", f"aes_{mode.lower()}_timing.png")

    # RSA timing
    rsa_sizes = [512, 1024, 2048, 3072]
    enc_times, dec_times = measure_rsa_times(rsa_sizes, rounds=3)
    plot_and_save([str(s) for s in rsa_sizes], enc_times, "time (ms)", "RSA encryption time (avg)", "rsa_enc_timing.png")
    plot_and_save([str(s) for s in rsa_sizes], dec_times, "time (ms)", "RSA decryption time (avg)", "rsa_dec_timing.png")
    print("[+] Timing plots saved to graphs/")

def main():
    while True:
        menu()
        choice = input("Select option: ").strip()
        if choice == "1":
            do_aes_workflow()
        elif choice == "2":
            do_rsa_workflow()
        elif choice == "3":
            do_rsa_sign_verify()
        elif choice == "4":
            do_hashing()
        elif choice == "5":
            do_timing_and_plot()
        elif choice == "6":
            print("Exiting.")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if _name_ == "_main_":
    main()