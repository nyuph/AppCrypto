# S-box values as shown in the assignment
from collections import Counter

S_BOX = [
    '01', '00', '11', '10'
]


# Create inverse S-box
def inverse_sbox():
    global S_BOX
    inverse = [''] * 4
    for index, value in enumerate(S_BOX):
        value = int(value, 2)
        binary_value = bin(index)[2:]
        if len(binary_value) < 2:
            binary_value = '0' * (2 - len(binary_value)) + binary_value
        inverse[value] = binary_value

    return inverse


# Inverse S-box values
INVERSE_S_BOX = inverse_sbox()


def generate_key(key):
    # Translate decimal key into binary number
    key_binary = bin(key)
    # Remove 0b in front
    key_binary = key_binary[2:]

    # Add 0s in front of the bit stream if the length is less than 8
    if len(key_binary) < 8:
        key = "0" * (8 - len(key_binary)) + key_binary
    else:
        # Only last 8 bits is the key
        key = key_binary[-8:]

    return key


# Switch first 2 bits position with the last 2 bits
def rotate_nib(w):
    return w[-2:] + w[:2]


# Substitute bits in Wi using the S-box matrix
def substitute_nib(w):
    global S_BOX

    # Convert binary to integer
    w_first2 = int(w[:2], 2)
    w_last2 = int(w[-2:], 2)

    # Return corresponding value in the S-box matrix
    return S_BOX[w_first2] + S_BOX[w_last2]


# Substitute bits in Wi using the inverse S-box matrix
def inverse_substitute_nib(w):
    global INVERSE_S_BOX

    # Convert binary to integer
    w_first2 = int(w[:2], 2)
    w_last2 = int(w[-2:], 2)

    # Return corresponding value in the inverse S-box matrix
    return INVERSE_S_BOX[w_first2] + INVERSE_S_BOX[w_last2]


# XOR Wi with RCONi and SubstituteNIBi
# or
# XOR Wi with W(i+1)
def xor_str(str1, str2, str3=None):
    xor_result = ''
    if str3 is not None:
        for value1, value2, value3 in zip(str1, str2, str3):
            xor_result += str(int(value1) ^ int(value2) ^ int(value3))
    else:
        for value1, value2 in zip(str1, str2):
            xor_result += str(int(value1) ^ int(value2))
    return xor_result


# Calculate w2 - w5
# Get (Key0, Key1, Key2) from Key K
def key_expansion(key):
    # rcon(i) = x^(i+2) mod (x^2 + x + 1)
    rcon1 = '0100'
    rcon2 = '1000'
    w0 = key[:4]
    w1 = key[-4:]

    w2 = xor_str(w0, rcon1, substitute_nib(rotate_nib(w1)))
    w3 = xor_str(w1, w2)

    w4 = xor_str(w2, rcon2, substitute_nib(rotate_nib(w3)))
    w5 = xor_str(w3, w4)

    key0 = w0 + w1
    key1 = w2 + w3
    key2 = w4 + w5
    return key0, key1, key2


# Switch bottom rows
def shift_rows(key):
    rows = [key[i:i + 2] for i in range(0, len(key), 2)]
    temp = rows[1]
    rows[1] = rows[3]
    rows[3] = temp

    return ''.join(rows)



# Perform  matrix operation to mix columns
def mix_columns(rows):
    """
         (0)  (2)     1   2       (0) 1 ^ (1) 2   (3) 2 ^ (2) 1
                        x     =
         (1)  (3)     2   1       (1) 1 ^ (0) 2   (2) 2 ^ (3) 1
     """

    return [
        rows[0] ^ gf_mult(2, rows[1]),
        rows[1] ^ gf_mult(2, rows[0]),
        rows[2] ^ gf_mult(2, rows[3]),
        rows[3] ^ gf_mult(2, rows[2]),
    ]


# Perform  matrix operation to inverse mix columns
def inverse_mix_columns(rows):
    """
         (0)  (2)     3   1       (0) 3 ^ (1) 1   (3) 1 ^ (2) 3
                        x     =
         (1)  (3)     1   3       (1) 3 ^ (0) 1   (2) 1 ^ (3) 3
    """
    return [
        gf_mult(3, rows[0]) ^ gf_mult(1, rows[1]),
        gf_mult(3, rows[1]) ^ gf_mult(1, rows[0]),
        gf_mult(3, rows[2]) ^ gf_mult(1, rows[3]),
        gf_mult(3, rows[3]) ^ gf_mult(1, rows[2]),
    ]


# Galois field multiplication mod(x^2 +x+1)
def gf_mult(number1, number2):
    result = 0

    # Loop four times
    for _ in range(2):
        # If least significant bit of number2 is 1 add value of number1 to the result using XOR
        if number2 & 1:
            result = result ^ number1
        # Multiply number1 by 2 (shift one bit to the left)
        number1 <<= 1
        # If number1 overflows beyond 2nd bit XOR with the binary value 0b10011 (x^2 +x+1)
        if number1 & (1 << 2):
            number1 ^= 0b111
        # Divide number2 by 2 (shift one bit to the right)
        number2 >>= 1

    return result


# Mix key columns
def mix_columns_key(key):
    rows = [int(''.join(key[i:i + 2]), 2) for i in range(0, len(key), 2)]

    rows = mix_columns(rows)

    rows = ['0' * (2 - len(bin(row)[2:])) + bin(row)[2:] for row in rows]

    result = ''.join(rows)

    return result


# Inverse mix key columns
def inverse_mix_columns_key(key):
    rows = [int(''.join(key[i:i + 2]), 2) for i in range(0, len(key), 2)]

    rows = inverse_mix_columns(rows)

    rows = ['0' * (2 - len(bin(row)[2:])) + bin(row)[2:] for row in rows]

    return ''.join(rows)

# encrypt_round1() using Key1 on plaintext, P, and get intermediate state X
def encrypt_round1(plaintext, key1):
    # Substitute nibbles operation
    intermediate_ciphertext = substitute_nib(plaintext[:4]) + substitute_nib(plaintext[-4:])

    # Shift Rows operation
    intermediate_ciphertext = shift_rows(intermediate_ciphertext)

    # Mix columns operation
    intermediate_ciphertext = mix_columns_key(intermediate_ciphertext)

    # Add Round Key operation #1
    intermediate_ciphertext = xor_str(intermediate_ciphertext, key1)

    return intermediate_ciphertext


# encrypt_round2() using Key2 on intermediate state X, and get the ciphertext C
def encrypt_round2(intermediate_ciphertext, key2):
    # Substitute nibbles operation
    ciphertext = substitute_nib(intermediate_ciphertext[:4]) + substitute_nib(intermediate_ciphertext[-4:])

    # Shift Rows operation
    ciphertext = shift_rows(ciphertext)

    # Add Round Key operation
    ciphertext = xor_str(ciphertext, key2)

    return ciphertext


def encryption(plaintext, key):
    key0, key1, key2 = key_expansion(key)

    intermediate_ciphertext = encrypt_round1(plaintext, key1)
    ciphertext = encrypt_round2(intermediate_ciphertext, key2)

    return ciphertext


# decrypt_round2() using Key 2 on the ciphertext, C, and get intermediate state, X
def decrypt_round2(ciphertext, key2):
    # Add Round Key operation with key2
    intermediate_plaintext = xor_str(ciphertext, key2)

    # Shift Rows operation
    intermediate_plaintext = shift_rows(intermediate_plaintext)
    test = inverse_substitute_nib(intermediate_plaintext[:4])
    # Substitute nibbles operation
    intermediate_plaintext = inverse_substitute_nib(intermediate_plaintext[:4]) + inverse_substitute_nib(intermediate_plaintext[-4:])

    return intermediate_plaintext


# decrypt_round1() using Key1 on X to get plaintext P
def decrypt_round1(intermediate_plaintext, key1):
    # Add Round Key operation with key1
    plaintext = xor_str(intermediate_plaintext, key1)

    # Inverse mix columns operation
    plaintext = inverse_mix_columns_key(plaintext)

    # Shift Rows operation
    plaintext = shift_rows(plaintext)

    # Substitute nibbles operation
    plaintext = inverse_substitute_nib(plaintext[:4]) + inverse_substitute_nib(plaintext[-4:])

    return plaintext


# Encryption operation in reverse order
def decryption(ciphertext, key):
    key0, key1, key2 = key_expansion(key)

    intermediate_plaintext = decrypt_round2(ciphertext, key2)
    plaintext = decrypt_round1(intermediate_plaintext, key1)

    return plaintext


def zero_padding(number, size):
    number = bin(number)[2:]
    if len(number) < size:
        number = '0' * (size - len(number)) + number

    return number


def meet_in_the_middle_attack(pair):
    possible_keys = []
    for test_key1 in range(2 ** 8):
        for test_key2 in range(2 ** 8):
            x = encrypt_round1(pair['plaintext'], zero_padding(test_key1, 8))
            x_inv = decrypt_round2(pair['ciphertext'], zero_padding(test_key2, 8))
            if x == x_inv:
                possible_keys.append({'key1': zero_padding(test_key1, 8), 'key2': zero_padding(test_key2, 8)})

    return possible_keys


def iter_mitm_attack(test_pair, result):
    possible_keys = []
    for key in result:
        test_key1 = key['key1']
        x = encrypt_round1(test_pair['plaintext'], test_key1)
        test_key2 = key['key2']
        x_inv = decrypt_round2(test_pair['ciphertext'], test_key2)
        if x == x_inv:
            possible_keys.append({'key1': test_key1, 'key2': test_key2})

    return possible_keys




if __name__ == '__main__':
    key = 65

    known_plaintext1 = '00000001'
    known_plaintext2 = '00011000'
    known_plaintext3 = '11000011'

    generated_key = generate_key(key)
    key0, key1, key2 = key_expansion(generated_key)
    
    known_ciphertext1 = encryption(known_plaintext1, generated_key)
    known_ciphertext2 = encryption(known_plaintext2, generated_key)
    known_ciphertext3 = encryption(known_plaintext3, generated_key)

    pair1 = {'plaintext': known_plaintext1, 'ciphertext': known_ciphertext1}
    pair2 = {'plaintext': known_plaintext2, 'ciphertext': known_ciphertext2}
    pair3 = {'plaintext': known_plaintext3, 'ciphertext': known_ciphertext3}

    known_pairs = [pair1, pair2, pair3]

    print('Key: ' + generated_key)
    print(f"Actual keys used - key0: {key0}, key1: {key1}, key2: {key2}") #print keys for checking

    # Start round 1 of meet in the middle attack
    print('Round 1 of MITM attack')
    print('Known plaintext: ' + known_pairs[0]['plaintext'])
    print('Known ciphertext: ' + known_pairs[0]['ciphertext'])
    n = 0 # set starting index for mitm attack rounds
    result = meet_in_the_middle_attack(known_pairs[0])
    if len(result) == 1:
        print("Keys found by attack: Key 1:", result[0][0], " Key 2: ", result[0][1])
    else:
        print(f"Count of potential keys after attack round {n + 1} : {len(result)}")
        print("Unable to find the matched keys with single known plaintext/ciphertext pair, too many potential keys found!")        
   
        # if keys not found in round 1, iterate through all remaining known pairs until either keys found or all pairs exhausted
        n += 1
        for test_pair in known_pairs:
            if n == 1: # skip first known pair as it was used in first mitm attack round
                n += 1
            else:
                print('Round ', n , ' of MITM attack')
                print('Known plaintext: ' + test_pair['plaintext'])
                print('Known ciphertext: ' + test_pair['ciphertext'])
                test_keyset = result
                result = iter_mitm_attack(test_pair, test_keyset)
                if len(result) == 1:
                    print("Keys found by attack: Key 1:", result[0][0], " Key 2: ", result[0][1])
                else:
                    print("Count of potential keys after attack round ", n, ": ", len(result))
                    print("Unable to find the matched keys with single known plaintext/ciphertext pair, too many potential keys found!")        
                n += 1

    # print("Count of result: ", len(result) + 1)
    # for index, keys in enumerate(result):
    #     print(str(index + 1)+". Keys")
    #     print("Key 1: " + keys['key1'] )
    #     print("Key 2: " + keys['key2'] )