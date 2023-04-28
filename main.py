import DNA
import utils

if __name__ == '__main__':

    # input plaintext
    text = input('plz input the message you want to encrypt:')
    
    key, ciphertext = DNA.DNAEncryption(text)
    
    print("\nThe original string is :" + "\n" + text + "\n")
    print("The key is : " + "\n" + key + "\n")
