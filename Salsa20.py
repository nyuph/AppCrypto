from Crypto.Cipher import Salsa20

plaintext = b'Attack at dawn'
print("Start plaintext: ", plaintext)
secret = b'*Thirty-two byte (256 bits) key*'
cipher = Salsa20.new(key=secret)
msg_nonce = cipher.nonce
print("Msg nonce: ", msg_nonce)
msg = cipher.nonce + cipher.encrypt(plaintext)
print("Msg: ", msg)

# decryption
# input k and msg (nonce + ciphertext)
# key the same as above
# secret = b'*Thirty-two byte (256 bits) key*'
# msg is from the encryption
msg_nonce = msg[:8]
ciphertext = msg[8:]
cipher = Salsa20.new(key=secret, nonce=msg_nonce)
plaintext = cipher.decrypt(ciphertext)
print("End Plaintext: ", plaintext)