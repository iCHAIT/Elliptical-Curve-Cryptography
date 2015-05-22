def shift(char, key, dec=True):
    """
       Shifts one letter at a time. Dec is short for
       decipher, and is an optional parameter.
    """
    if dec:
        shifted = chr(ord(char) - key)
    else:
        shifted = chr(ord(char) + key)

    if shifted > 'Z':
        return chr(ord(shifted) - 26)
    elif shifted < 'A':
        return chr(ord(shifted) + 26)
    else:
        return shifted


def encipher(message):
    """
       Just loops each letter in the message, calling the shift
       function for each iteration.
    """
    key = int(input("Please enter the key: "))
    ciphertext = ""
    for char in message:
        ciphertext += shift(char, key, dec=False)
    print(ciphertext)


def decipher(message):
    """
       Does the opposite of encipher.
    """
    key = int(input("Please enter the key: "))
    plaintext = ""
    for char in message:
        plaintext += shift(char, key)
    print(plaintext)


def main():
    message = raw_input("Please enter text: ").upper().replace(" ", "")
    method = raw_input(
        "Please enter method, e for encryption, d for decryption.").upper()
    if method in OPTIONS_DICT:
        do_it = OPTIONS_DICT[method]
        do_it(message)
    else:
        print("Invalid option!")


if __name__ == "__main__":

    OPTIONS_DICT = {'D': decipher,
                    'E': encipher, }
    main()
