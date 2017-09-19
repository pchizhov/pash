def encrypt_caesar(plaintext, shift):
    ciphertext = ''
    for letter in plaintext:
        index = ord(letter)
        if index < 91:
            ciphertext += chr((index - 65 + shift) % 26 + 65)
        else:
            ciphertext += chr((index - 97 + shift) % 26 + 97)
    return ciphertext


def decrypt_caesar(ciphertext, shift):
    plaintext = ''
    for letter in ciphertext:
        index = ord(letter)
        if index < 91:
            plaintext += chr(90 - (90 + shift - index) % 26)
        else:
            plaintext += chr(122 - (122 + shift - index) % 26)
    return plaintext


answer = input('encrypt or decrypt? ')
if answer == 'encrypt':
    word = str(input('enter the word: '))
    number = int(input('enter the shift: '))
    print(encrypt_caesar(word, number))
elif answer == 'decrypt':
    word = str(input('enter the word: '))
    number = int(input('enter the shift: '))
    print(decrypt_caesar(word, number))
