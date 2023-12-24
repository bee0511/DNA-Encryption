import DNA
from utils import *
import os

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path + "\..\cipher\Cipher.txt")

    EncrypOrDecrypt = input(
        "Encrypt or decrypt a message?\nPress 1 for encryption, press 2 for decryption: "
    ).strip()

    if EncrypOrDecrypt == "1":
        ans = input(
            "What do you want to encrypt? \nPress 1 for std input, press 2 for file: "
        )
        if ans == "1":
            DNA.TextEncryption()
        elif ans == "2":
            file = input(
                "Enter your file name. Ex: '../example/test.txt' or '../example/test.jpg' \n"
            )
            if os.path.isfile(file) == False:
                print("File not found: " + file)
                exit(1)
            DNA.FileEncryption(file)
            print(
                "You can find your cipher in '../cipher/Cipher.txt' and your key in '../key/Key.txt'"
            )
        else:
            print("Invalid input!")

    elif EncrypOrDecrypt == "2":
        ans = input(
            "What do you want to decrypt? \nPress 1 for .txt file, press 2 for img file: "
        )
        if os.path.isfile(CIPHER_PATH) == False:
            print("File not found: " + CIPHER_PATH)
            exit(1)
        if os.path.isfile(KEY_PATH) == False:
            print("File not found: " + KEY_PATH)
            exit(1)
        if ans == "1":
            DNA.Decryption(
                CIPHER_PATH,
                KEY_PATH,
                type="text",
            )
            print(
                "You can find your decoded message in '{}'".format(
                    DECRYPT_PATH + "PlainTextResult.txt"
                )
            )
        elif ans == "2":
            DNA.Decryption(
                CIPHER_PATH,
                KEY_PATH,
                type="image",
            )
            print(
                "You can find your decoded image in '{}".format(
                    DECRYPT_PATH + "DecodedImage.png"
                )
            )
        else:
            print("Invalid input!")
    else:
        print("Invalid input!")
