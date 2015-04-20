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


def bruteforce(message):
    """
       The inner loop does exactly the same thing as the decipher
       function. The outer loop ensures it happens 26 times, changing
       the key on each iteration.
    """
    for key in range(26):
        plaintext = ""
        for char in message:
            plaintext += shift(char, key)
        print(plaintext)


def main():
    """
       Gets the message and the cipher method. The correct function
       is selected from the OPTIONS_DICT constant.
    """
    message = raw_input("Please enter text: ").upper().replace(" ", "")
    method = raw_input("Please enter method, e for encipher, d for decipher, or b for bruteforce: ").upper()
    if method in OPTIONS_DICT:
        do_it = OPTIONS_DICT[method]
        do_it(message)
    else:
        print("Invalid option!")




if __name__ == "__main__":

    OPTIONS_DICT = {'D': decipher,
                    'E': encipher,
                    'B': bruteforce}
    main()
