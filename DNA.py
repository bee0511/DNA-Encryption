import utils
import adaptiveHuffman
import os

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
    Compressor = adaptiveHuffman.AdaptiveHuffman()
    Compressor.compress(path,"Compression.txt")
    print("Saving files...")

    message = ""
    with open("CompressionBinary.txt","r") as f:
        message=f.read()
    key = utils.lfsr(len(message))
    xor = utils.keyXor(keys=key, text=message)
    output = ''.join(text for text in Encode(xor))

    with open("Key.txt","w") as f:
        f.write(key)
    with open("Cipher.txt","w") as f:
        f.write(output)

    os.remove("Compression.txt")
    os.remove("CompressionBinary.txt")

def TextEncryption():
    text = input("Enter your message to encrypt: ")
    with open("InputText.txt", "w") as f:
        f.write(text)
    FileEncryption("InputText.txt")
    os.remove("InputText.txt")

def Decode(ciphertext, key, type):
    xored_binary = "".join(list(TABLE.keys())[list(TABLE.values()).index(dna)] for dna in ciphertext)
    binary = utils.keyXor(keys=key, text=xored_binary)
    if type == "text":
        adaptiveHuffman.AdaptiveHuffman().expand(binary,"PlainTextResult.txt")
    elif type == "image": 
        adaptiveHuffman.AdaptiveHuffman().expand(binary,"DecodedImage.png")

def Decryption(ciphertext_path, key_path, type):
    print("Decrypting...")  
    with open(ciphertext_path,"r") as cipher_pointer, open(key_path,"r") as key_pointer:
        ciphertexts = cipher_pointer.read()
        keys = key_pointer.read()
        if type == "text":
            Decode(ciphertext=ciphertexts, key=keys, type="text")
        elif type == "image": 
            Decode(ciphertext=ciphertexts, key=keys, type="image")


if __name__ == '__main__':

    # FileEncryption("plaintext.txt")
    # Decryption("filecipher.txt", "filekey.txt")
    # DNAFileEncryption("plaintext.txt")
    # DNAFileDecryption("filecipher.txt", "filekey.txt")
    # TextEncryption()
    Decryption("filecipher.txt", "filekey.txt")
