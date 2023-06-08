import cv2
import numpy as np
import random
import binascii
import math

def keyXor(keys, text):
    return "".join(str(ord(key) - ord('0') ^ (ord(letter) - ord('0'))) for key, letter in zip(keys, text))

def generate_seed():
    # generate seed for lfsr avoid 00000
    seed = [random.randint(0, 1) for _ in range(5)]
    while seed == [0, 0, 0, 0, 0]:
        seed = [random.randint(0, 1) for _ in range(5)]
    return seed

def lfsr(n):
    seed = generate_seed()
    return_key = ""
    for round in range(n):
        if round != 0 and n > 10 and round % 10 == 0:
            seed = generate_seed()
        new_bit = seed[4] ^ seed[2] ^ seed[0]
        return_key += str(new_bit)
        if round == n-1:
            break
        for shift in range(4, -1, -1):
            if shift == 0:
                seed[0] = new_bit
            else:
                seed[shift] = seed[shift-1]
    return return_key

if __name__ == '__main__':
    pass