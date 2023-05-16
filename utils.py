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

def diffPic(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    imgAlter = np.zeros(img.shape)
    imgAlter[0][0] = img[0][0]
    for i in range(1,img.shape[0]):
        imgAlter[i][0] = (int(img[i][0]) - int(img[i-1][0])) % 256

    for i in range(img.shape[0]):
        for j in range(1,img.shape[1]):
            imgAlter[i][j] = (int(img[i][j]) - int(img[i][j-1])) % 256
    
    cv2.imwrite('ImgAlter.png', imgAlter)


def recoverDiffPic(path):
    imgAlter = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
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