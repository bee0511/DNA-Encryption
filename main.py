import DNA
import utils

if __name__ == '__main__':

    EncrypOrDecrypt = input("Encrypt or decrypt a message?\nPress 1 for encryption, press 2 for decryption: ")

    match EncrypOrDecrypt: 
        case "1":
            ans = input("What do you want to encrypt? \nPress 1 for std input, press 2 for .txt file, press 3 for img file: ")
            match ans:
                case "1":
                    DNA.TextEncryption()
                case "2":
                    file = input("Enter your .txt file name. Ex: 'test.txt' \n")
                    DNA.FileEncryption(file)
                case "3": 
                    file = input("Enter your img file name. Ex: 'test.png' \n")
                    DNA.PictureEncryption(file)
            print("You can find your cipher in 'Cipher.txt' and your key in 'Key.txt")
        case "2":
            ans = input("What do you want to decrypt? \nPress 1 for .txt file, press 2 for img file: ")
            match ans:
                case "1":
                    DNA.Decryption("Cipher.txt", "Key.txt", type="text")
                    print("You can find your decoded message in 'PlainTextResult.txt'")
                case "2":
                    DNA.Decryption("Cipher.txt", "Key.txt", type="image")
                    print("You can find your decoded image in 'DecodedResult.png'")
