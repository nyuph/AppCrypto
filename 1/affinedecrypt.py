def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    if gcd(a, m) == 1:
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
    return None

def affine_decrypt(ciphertext, a, b):
    plaintext = ""
    m = 26  # Assuming the alphabet consists of 26 letters (English)

    if mod_inverse(a, m) is None:
        return "The value of 'a' is not valid. It must be coprime with 26."

    for character in ciphertext:
        if character.isalpha():
            character = character.upper()
            character_index = ord(character) - ord('A')
            decrypted_index = mod_inverse(a, m) * (character_index - b) % m
            decrypted_character = chr(decrypted_index + ord('A'))
            plaintext += decrypted_character
        else:
            plaintext += character

    return plaintext

# Get user input
ciphertext = input("Enter the ciphertext: ")
a = int(input("Enter the value of 'a' (must be coprime with 26): "))
b = int(input("Enter the value of 'b': "))

# Decrypt the ciphertext
decrypted_text = affine_decrypt(ciphertext, a, b)

# Display the decrypted text
print("Decrypted text:", decrypted_text)