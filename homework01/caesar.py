def encrypt_caesar(plaintext, shift):
    """
    >>> encrypt_caesar("PYTHON",3)
    'SBWKRQ'
    >>> encrypt_caesar("python",3)
    'sbwkrq'
    >>> encrypt_caesar("",3)
    ''
    """
    ciphertext = ''
    for letter in plaintext:
        index = ord(letter)
        if 64 < index < 91:
            ciphertext += chr((index - 65 + shift) % 26 + 65)
        elif 96 < index < 123:
            ciphertext += chr((index - 97 + shift) % 26 + 97)
        else:
            ciphertext += chr(index)
    return ciphertext


def decrypt_caesar(ciphertext, shift):
    """
    >>> decrypt_caesar("SBWKRQ",3)
    'PYTHON'
    >>> decrypt_caesar("sbwkrq",3)
    'python'
    >>> decrypt_caesar("",3)
    ''
    """
    plaintext = ''
    for letter in ciphertext:
        index = ord(letter)
        if 64 < index < 91:
            plaintext += chr(90 - (90 + shift - index) % 26)
        elif 96 < index < 123:
            plaintext += chr(122 - (122 + shift - index) % 26)
        else:
            plaintext += chr(index)
    return plaintext
