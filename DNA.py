import utils
import adaptiveHuffman

# transform bit to ATCG

TABLE = {"00" : "A",
         "01" : "G",
         "10" : "C",
         "11" : "T"}
def compression(path):
    Encoder=adaptiveHuffman.AdaptiveHuffman()
    Encoder.encode(path,"compression.txt")
    DNAFileEncryption("compressionBinary.txt")

def DNAFileEncryption(path):
    message=""
    with open(path,"r") as f:
        message=f.read()
    key = utils.lfsr(len(message))
    xor = utils.keyXor(keys=key, text=message)
    output = ''.join(text for text in DNAEncode(xor))

    with open("filekey.txt","w") as f:
        f.write(key)
    with open("filecipher.txt","w") as f:
        f.write(output)

            
def DNAFileDecryption(ciphertext_path, key_path):
    plaintext = ""
    with open(ciphertext_path,"r") as cipher_pointer, open(key_path,"r") as key_pointer:
        ciphertexts = cipher_pointer.read()
        keys = key_pointer.read()
        DNADecode(ciphertext=ciphertexts, key=keys, type="text")
            
def DNAEncryption(message):
    
    # turn into binary
    binary_string = utils.text_to_bits(text=message)

    # generate OTP
    key = utils.lfsr(len(binary_string))

    # XOR with OTP
    xor = utils.keyXor(keys=key, text=binary_string)

    # turn into ATCG
    output = ''.join(text for text in DNAEncode(xor))

    # print("\nThe original string is :" + "\n" + message + "\n")
    # print("The string after binary conversion is :" + "\n" + binary_string + "\n")
    # print("The key is : " + "\n" + key + "\n")
    # print("The string represented by single-letter codes is :" + "\n" + output + "\n")
    # utils.writeFile(output, "cypher.txt")
    # utils.writeFile(key, "key.txt")
    # utils.writeFile(binary_string, "binary.txt")
    # utils.writeFile(message, "plaintext.txt")
    return key, output

def DNAEncode(xor_message):

    if len(xor_message) % 2 != 0:
        xor_message = xor_message + '0'

    return [TABLE[xor_message[i] + xor_message[i+1]] for i in range(0, len(xor_message), 2)]

def DNADecode(ciphertext, key, type):
    if type == "text":
        xored_binary = "".join(list(TABLE.keys())[list(TABLE.values()).index(dna)] for dna in ciphertext)
        binary = utils.keyXor(keys=key, text=xored_binary)
        adaptiveHuffman.AdaptiveHuffman().decode(binary,"fileplain.txt")
# test DNA.py
if __name__ == '__main__':
    # after_xor_list = ['1', '1', '1', '0', '1', '1', '0', '0', '1', '0', '0', '0', '0', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '1', '1', '1', '1', '1', '0', '1',
                    #   '0', '1', '1', '0', '0', '1', '1', '0', '0', '0', '1', '1', '0', '0', '1', '1', '1', '0', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '0', '0', '0', '1', '0']
    # dna_list = DNAEncode(after_xor_list)
    # for segment in dna_list:
        # print(segment, end='')
    # DNADecode("GATCTTAGGACT", "001001101001010000111000", "text")
    # DNAFileEncryption("plaintext.txt")
    compression("plaintext.txt")
    DNAFileDecryption("filecipher.txt", "filekey.txt")
    # print(DNADecode("GCGTTTGAGGTCGTAAGTTGGCGTGAGCTGGCAGGTTTCTGATAAGAT", "000011101101010000111010000111110001001100010011011001101011110101111001100101000011101100011001", "text"))
