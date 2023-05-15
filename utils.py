import cv2
import numpy as np
import random
import binascii
import math

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def overwriteFile(text, filename):
    with open(filename, 'w') as cyphertext_output:
        for letter in text:
            cyphertext_output.write(letter)
        # cyphertext_output.write('\n')

def writeFile(text, filename):
    with open(filename, 'a') as cyphertext_output:
        for letter in text:
            cyphertext_output.write(letter)
        # cyphertext_output.write('\n')

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
    # utils.writeFile(return_key, "key.txt")
    return return_key

def diffPic(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    imgAlter = np.zeros(img.shape)
    imgAlter[0][0] = img[0][0]
    for i in range(1,img.shape[0]):
        imgAlter[i][0] = (int(img[i][0]) - int(img[i-1][0])) % 256

    for i in range(img.shape[0]):
        for j in range(1,img.shape[1]):
            imgAlter[i][j] = (int(img[i][j]) - int(img[i][j-1])) % 256

    message = ""
    message += str(imgAlter.shape[0]) + " " + str(imgAlter.shape[1]) + " "

    for i in range(imgAlter.shape[0]):
        for j in range(imgAlter.shape[1]):
            message += str(math.trunc(imgAlter[i][j])) + " "

    with open("image.txt", "w") as f:
        f.write(message)

def recoverDiffPic(imgAlter):
    recoverFromDiff = np.zeros(imgAlter.shape)

    recoverFromDiff[0][0]=imgAlter[0][0]
    for i in range(1, imgAlter.shape[0]):
        recoverFromDiff[i][0] = (int(imgAlter[i][0]) + int(recoverFromDiff[i-1][0])) % 256

    for i in range(imgAlter.shape[0]):
        for j in range(1,imgAlter.shape[1]):
            recoverFromDiff[i][j] = (int(imgAlter[i][j]) + int(recoverFromDiff[i][j-1])) % 256

    recoverFromDiff = recoverFromDiff.astype(np.uint8)
    cv2.imwrite('DecodedResult.png',recoverFromDiff)

if __name__ == '__main__':
    diffPic("test.tiff")