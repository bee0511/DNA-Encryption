import DNA
import utils

if __name__ == '__main__':

    EncrypOrDecrypt = input("Encrypt or decrypt a message?\nPress 1 for encryption, press 2 for decryption: ")

    if EncrypOrDecrypt == "1":
        ans = input("What do you want to encrypt? \nPress 1 for std input, press 2 for .txt file, press 3 for img file: ")
        if ans == "1":
            DNA.TextEncryption()
        elif ans == "2": 
            file = input("Enter your .txt file name. Ex: 'test.txt' \n")
            DNA.FileEncryption(file)
        elif ans == "3":
            file = input("Enter your img file name. Ex: 'test.png' \n")
            DNA.PictureEncryption(file)

        print("You can find your cipher in 'Cipher.txt' and your key in 'Key.txt")
    
    elif EncrypOrDecrypt == "2":
        ans = input("What do you want to decrypt? \nPress 1 for .txt file, press 2 for img file: ")
        if ans == "1":
            DNA.Decryption("Cipher.txt", "Key.txt")
        elif ans == "2":
            DNA.PictureDecryption("Cipher.txt", "Key.txt")
        print("You can find your decoded message in 'PlainTextResult.txt'")
