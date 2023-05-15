import utils
import adaptiveHuffman
import numpy as np

# transform bit to ATCG

TABLE = {"00" : "A",
         "01" : "G",
         "10" : "C",
         "11" : "T"}

def Encode(xor_message):
    if len(xor_message) % 2 != 0:
        print(len(xor_message))
        xor_message = xor_message + '0'

    return [TABLE[xor_message[i] + xor_message[i+1]] for i in range(0, len(xor_message), 2)]

def FileEncryption(path): 
    Encoder=adaptiveHuffman.AdaptiveHuffman()
    Encoder.encode(path,"Compression.txt")
    print("Saving files...")

    message=""
    with open("CompressionBinary.txt","r") as f:
        message=f.read()
    key = utils.lfsr(len(message))
    xor = utils.keyXor(keys=key, text=message)
    output = ''.join(text for text in Encode(xor))

    with open("Key.txt","w") as f:
        f.write(key)
    with open("Cipher.txt","w") as f:
        f.write(output)

def TextEncryption():
    text = input("Enter your message to encrypt: ")
    with open("InputText.txt", "w") as f:
        f.write(text)
    FileEncryption("InputText.txt")

def PictureEncryption(path):
    utils.diffPic(path)
    print("Integral Image Done.")
    print("Start Encoding...")
    FileEncryption("image.txt")

def Decode(ciphertext, key, type):
    if type == "text":
        xored_binary = "".join(list(TABLE.keys())[list(TABLE.values()).index(dna)] for dna in ciphertext)
        binary = utils.keyXor(keys=key, text=xored_binary)
        adaptiveHuffman.AdaptiveHuffman().decode(binary,"PlainTextResult.txt")

def Decryption(ciphertext_path, key_path):
    print("Decrypting...")  
    with open(ciphertext_path,"r") as cipher_pointer, open(key_path,"r") as key_pointer:
        ciphertexts = cipher_pointer.read()
        keys = key_pointer.read()
        Decode(ciphertext=ciphertexts, key=keys, type="text")

def PictureDecryption(ciphertext_path, key_path):
    # Decryption(ciphertext_path, key_path)
    print("Turning to image...")
    message = ""
    with open("PlainTextResult.txt", "r") as f:
        message = f.read()
    
    imgLinear = message.split()
    shape0 = int(imgLinear.pop(0))
    shape1 = int(imgLinear.pop(0))

    img = np.zeros((shape0, shape1))
    
    for i in range(shape0):
        for j in range(shape1):
            img[i][j] = int(imgLinear.pop(0))

    utils.recoverDiffPic(img)


if __name__ == '__main__':

    # FileEncryption("plaintext.txt")
    # Decryption("filecipher.txt", "filekey.txt")
    # DNAFileEncryption("plaintext.txt")
    # DNAFileDecryption("filecipher.txt", "filekey.txt")
    # TextEncryption()
    # Decryption("filecipher.txt", "filekey.txt")
    # PictureEncryption("test.tiff")
    PictureDecryption("Cipher.txt", "Key.txt")