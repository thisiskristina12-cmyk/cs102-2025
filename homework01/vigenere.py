def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key_len = len(keyword)
    key_index = 0
    for symbol in plaintext:
        shift = ord(keyword[key_index % key_len])
        if "A" <= symbol <= "Z":
            start = ord("A")
            move = shift - ord("A")
            ciphertext += chr(start + (ord(symbol) - start + move) % 26)
        elif "a" <= symbol <= "z":
            start = ord("a")
            move = shift - ord("a")
            ciphertext += chr(start + (ord(symbol) - start + move) % 26)
        else:
            ciphertext += symbol
        key_index += 1
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key_len = len(keyword)
    key_index = 0
    for symbol in ciphertext:
        shift = ord(keyword[key_index % key_len])
        if "A" <= symbol <= "Z":
            start = ord("A")
            move = shift - ord("A")
            plaintext += chr(start + (ord(symbol) - start - move) % 26)
        elif "a" <= symbol <= "z":
            start = ord("a")
            move = shift - ord("a")
            plaintext += chr(start + (ord(symbol) - start - move) % 26)
        else:
            plaintext += symbol
        key_index += 1
    return plaintext
