import cv2
import numpy as np
import random


# transform bit to ATCG
TABLE = {"00": "A", "01": "G", "10": "C", "11": "T"}

# File path
CIPHER_PATH = "../cipher/Cipher.txt"
KEY_PATH = "../key/Key.txt"
DECRYPT_PATH = "../decrypted/"


def keyXor(keys, text):
    """
    Xor key with text
    Args:
        keys (str): key
        text (str): text
    Returns:
        str: xor result
    """
    return "".join(
        str(ord(key) - ord("0") ^ (ord(letter) - ord("0")))
        for key, letter in zip(keys, text)
    )


def generate_seed():
    """
    Generate seed for LFSR
    Returns:
        list: seed
    """
    seed = [random.randint(0, 1) for _ in range(5)]
    while seed == [0, 0, 0, 0, 0]:
        # Avoid 00000
        seed = [random.randint(0, 1) for _ in range(5)]
    return seed


def lfsr(n):
    """
    Generate key using LFSR
    Args:
        n (int): length of key
    Returns:
        str: key
    """
    seed = generate_seed()
    return_key = ""
    for round in range(n):
        if round != 0 and n > 10 and round % 10 == 0:
            seed = generate_seed()
        new_bit = seed[4] ^ seed[2] ^ seed[0]
        return_key += str(new_bit)
        if round == n - 1:
            break
        for shift in range(4, -1, -1):
            if shift == 0:
                seed[0] = new_bit
            else:
                seed[shift] = seed[shift - 1]
    return return_key


if __name__ == "__main__":
    pass
