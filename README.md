# Cryptography Engineering Final Project
課程名稱 Course Name：密碼工程 Cryptography Engineering

授課教師 Lecturer：謝致仁

授課時間 Semester：111-2 2023 Spring
# DNA Encryption

A python program that can encrypt the text or image into DNA sequence, and decrypt it.

## Concept
1. User input the file path
2. Use Adaptive Huffman coding algorithm to compress the file
3. Use LFSR (Linear feedback shift register) to generate OTP (One time password) key
4. Use XOR to encrypt the plaintext with the key
5. Use a dictionary to translate binary into ACTG
6. Save the encrypted ATCG message in a .txt file

## Requirement

Make sure that you have install all required packages in **requirements.txt**

You can use `pip install -r requirements.txt` to install the packages

## How to Run


1. Navigate to the `./src` directory.
2. Use `python main.py` to start the program
3. Choose the mode (encryption or decryption) and specify the file type and path.
4. The encrypted result and its key would be saved into `cipher/Cipher.txt` and `key/Key.txt`
5. If you want to decrypt the file with the key, you can also use `python main.py` to decrypt it.

