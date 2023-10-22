## Updated version to save ciphertext and key in separate files
import random
import string
import binascii

# characters, digits, symbols, and spaces used for key generation
ALLOWED_CHARS = string.ascii_lowercase + string.digits + string.punctuation + ' '

# random key generation function of a specific length that uses characters from allowable chars above
def key_gen(length):
    return ''.join(random.choice(ALLOWED_CHARS) for _ in range(length))

# encryption function for a given message using a given key, returns encrypted hex values
def otp_encrypt(message, key):
    encrypted_bytes = [ord(m) ^ ord(k) for m, k in zip(message, key)]
    print(encrypted_bytes)
    encrypted_hex = binascii.hexlify(bytes(encrypted_bytes))
    print(bytes(encrypted_bytes))
    print(encrypted_hex)
    return encrypted_hex.decode()

# get user message
message = input("enter message: ")
# generate key same length as message
key = key_gen(len(message))
#encypt user message
ciphertext = otp_encrypt(message, key)

#save key to file
with open('key1.txt', 'w') as f:
    f.write(key)

#save cipher to file
with open('ciphertext1.txt','w') as f:
    f.write(ciphertext)
