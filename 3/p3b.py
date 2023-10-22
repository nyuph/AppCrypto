import string
import binascii

# Characters, digits, symbols, and spaces used for key generation
ALLOWED_CHARS = string.ascii_lowercase + string.digits + string.punctuation + ' '

# Decryption function for a given ciphertext using a given key, returns the decrypted plaintext
def one_time_pad_decrypt(ciphertext, key):
    ciphertext_bytes = binascii.unhexlify(ciphertext.encode())
    decrypted_bytes = [c ^ ord(k) for c, k in zip(ciphertext_bytes, key)]
    decrypted_plaintext = ''.join(chr(b) for b in decrypted_bytes)
    return decrypted_plaintext

# Read plaintexts, key, and ciphertexts from the file
plaintexts = []
key = ""
ciphertexts = []

with open('encrypted_data.txt', 'r') as f:
    lines = f.readlines()
    current_section = None

    for line in lines:
        line = line.strip()

        if line == "Plaintexts:":
            current_section = 'plaintexts'
        elif line == "Key:":
            current_section = 'key'
        elif line == "Ciphertexts:":
            current_section = 'ciphertexts'
        elif current_section == 'plaintexts':
            plaintext = binascii.unhexlify(line.encode()).decode()
            plaintexts.append(plaintext)
        elif current_section == 'key':
            if line != "":
                key = binascii.unhexlify(line.encode()).decode()
        elif current_section == 'ciphertexts':
            ciphertexts.append(line)

# Decrypt ciphertexts using the key and print the resulting plaintexts
for ciphertext in ciphertexts:
    plaintext = one_time_pad_decrypt(ciphertext, key)
    print("Decrypted plaintext:", plaintext)