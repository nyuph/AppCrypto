import random
import string
import binascii

# Characters, digits, symbols, and spaces used for key generation
ALLOWED_CHARS = string.ascii_lowercase + string.digits + string.punctuation + ' '

# Random key generation function of a specific length that uses characters from ALLOWED_CHARS
def key_gen(length):
    return ''.join(random.choice(ALLOWED_CHARS) for _ in range(length))

# Encryption function for a given message using a given key, returns encrypted hex values
def one_time_pad_encrypt(message, key):
    encrypted_bytes = [ord(m) ^ ord(k) for m, k in zip(message, key)]
    encrypted_hex = binascii.hexlify(bytes(encrypted_bytes))
    return encrypted_hex.decode()

# List of plaintext messages
plaintexts = [
    "We learned that one time pad is proved to be perfect security.",
    "What happens if we do many time pad, that is a key is to be used more than once.",
    "Alice starts one program that asks Alice to enter a message on screen.",
    "The program then outputs the ciphertext on screen.",
    "It saves the cyphertext in hex in one file and the key in hex in another file.",
    "Assume the key length is longer than any of the plaintexts.",
    "These findings would be useful in the next problem.",
    "The hints below may give you some ideas.",
    "You can change the plaintexts or the key to verify your findings.",
    "This code is an extension to the code written for the one-time pad."
]

# Generate a key longer than the longest plaintext
max_plaintext_length = max(len(p) for p in plaintexts)
key_length = max_plaintext_length + 10
key = key_gen(key_length)

# Encrypt plaintexts using the same key
ciphertexts = []
for plaintext in plaintexts:
    ciphertext = one_time_pad_encrypt(plaintext, key)
    print("Ciphher:", ciphertext)
    ciphertexts.append(ciphertext)

# Save plaintext, key, and ciphertext in hex to a single file
with open('encrypted_data.txt', 'w') as f:
    # Save plaintexts in hex
    f.write("Plaintexts:\n")
    for plaintext in plaintexts:
        f.write(binascii.hexlify(plaintext.encode()).decode() + "\n")
    f.write("\n")
    
    # Save key in hex
    f.write("Key:\n")
    f.write(binascii.hexlify(key.encode()).decode() + "\n\n")

    # Save ciphertexts in hex
    f.write("Ciphertexts:\n")
    for ciphertext in ciphertexts:
        f.write(ciphertext + "\n")