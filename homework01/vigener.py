def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    count = 0
    for i in plaintext:
        count += 1
        shift = ord(keyword[(count - 1) % len(keyword)])
        if shift < 91:
            shift -= 65
        else:
            shift -= 97
        index = ord(i)
        if index < 91:
            ciphertext += chr((index - 65 + shift) % 26 + 65)
        else:
            ciphertext += chr((index - 97 + shift) % 26 + 97)
    return ciphertext

def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    count = 0
    for i in ciphertext:
        count += 1
        shift = ord(keyword[(count - 1) % len(keyword)])
        if shift < 91:
            shift -= 65
        else:
            shift -= 97
        index = ord(i)
        if index < 91:
            plaintext += chr(90 - (90 + shift - index) % 26)
        else:
            plaintext += chr(122 - (122 + shift - index) % 26)
    return plaintext