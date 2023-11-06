# S-box values as shown in the class slides
S_BOX = [
    '1001', '0100', '1010', '1011',
    '1101', '0001', '1000', '0101',
    '0110', '0010', '0000', '0011',
    '1100', '1110', '1111', '0111'
]


# Create inverse S-box
def inverse_sbox():
    global S_BOX
    inverse = [''] * 16
    for index, value in enumerate(S_BOX):
        value = int(value, 2)
        binary_value = bin(index)[2:]
        if len(binary_value) < 4:
            binary_value = '0' * (4 - len(binary_value)) + binary_value
        inverse[value] = binary_value

    return inverse


# Inverse S-box values
INVERSE_S_BOX = inverse_sbox()


def generate_key(key):
    # Translate decimal key into binary number
    key_binary = bin(key)
    # Remove 0b in front
    key_binary = key_binary[2:]

    # Add 0s in front of the bit stream if the length is less than 16
    if len(key_binary) < 16:
        key = "0" * (16 - len(key_binary)) + key_binary
    else:
        # Only last 16 bits is the key
        key = key_binary[-16:]

    return key


# Plaintext is binary representation of the first letter of the student’s first name
# combined with the binary representation the first letter of the student's last name
def generate_plaintext(letter1, letter2):
    # Convert to binary and remove 0b in front
    letter1_binary = bin(ord(letter1))[2:]
    if len(letter1_binary) < 8:
        letter1_binary = '0' * (8 - len(letter1_binary)) + letter1_binary
    letter2_binary = bin(ord(letter2))[2:]
    if len(letter2_binary) < 8:
        letter2_binary = '0' * (8 - len(letter2_binary)) + letter2_binary

    return letter1_binary + letter2_binary


def convert_to_text(plaintext):
    letters = [plaintext[i:i + 8] for i in range(0, len(plaintext), 8)]
    converted_plaintext = ''
    for letter in letters:
        converted_plaintext += chr(int(letter, 2))

    return converted_plaintext


# Switch first 4 bits position with the last 4 bits
def rotate_nib(w):
    return w[-4:] + w[:4]


# Substitute bits in Wi using the S-box matrix
def substitute_nib(w):
    global S_BOX

    # Convert binary to integer
    w_first4 = int(w[:4], 2)
    w_last4 = int(w[-4:], 2)

    # Return corresponding value in the S-box matrix
    return S_BOX[w_first4] + S_BOX[w_last4]


# Substitute bits in Wi using the inverse S-box matrix
def inverse_substitute_nib(w):
    global INVERSE_S_BOX

    # Convert binary to integer
    w_first4 = int(w[:4], 2)
    w_last4 = int(w[-4:], 2)

    # Return corresponding value in the inverse S-box matrix
    return INVERSE_S_BOX[w_first4] + INVERSE_S_BOX[w_last4]


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
    # rcon(i) = x^(i+2) mod (x^4 + x + 1)
    rcon1 = '10000000'
    rcon2 = '00110000'
    w0 = key[:8]
    w1 = key[-8:]

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
    rows = [key[i:i + 4] for i in range(0, len(key), 4)]
    temp = rows[1]
    rows[1] = rows[3]
    rows[3] = temp

    return ''.join(rows)


# Perform  matrix operation to mix columns
def mix_columns(rows):
    """
         (0)  (2)     1   4       (0) 1 ^ (1) 4   (3) 4 ^ (2) 1
                        x     =
         (1)  (3)     4   1       (1) 1 ^ (0) 4   (2) 4 ^ (3) 1
     """

    return [
        rows[0] ^ gf_mult(4, rows[1]),
        rows[1] ^ gf_mult(4, rows[0]),
        rows[2] ^ gf_mult(4, rows[3]),
        rows[3] ^ gf_mult(4, rows[2]),
    ]


# Perform  matrix operation to inverse mix columns
def inverse_mix_columns(rows):
    """
         (0)  (2)     9   2       (0) 9 ^ (1) 2   (3) 2 ^ (2) 9
                        x     =
         (1)  (3)     2   9       (1) 9 ^ (0) 2   (2) 2 ^ (3) 9
    """
    return [
        gf_mult(9, rows[0]) ^ gf_mult(2, rows[1]),
        gf_mult(9, rows[1]) ^ gf_mult(2, rows[0]),
        gf_mult(9, rows[2]) ^ gf_mult(2, rows[3]),
        gf_mult(9, rows[3]) ^ gf_mult(2, rows[2]),
    ]


# Galois field multiplication mod(x4 +x+1)
def gf_mult(number1, number2):
    result = 0

    # Loop four times
    for _ in range(4):
        # If least significant bit of number2 is 1 add value of number1 to the result using XOR
        if number2 & 1:
            result = result ^ number1
        # Multiply number1 by 2 (shift one bit to the left)
        number1 <<= 1
        # If number1 overflows beyond 4th bit XOR with the binary value 0b10011 (x4 +x+1)
        if number1 & (1 << 4):
            number1 ^= 0b10011
        # Divide number2 by 2 (shift one bit to the right)
        number2 >>= 1

    return result


# Mix key columns
def mix_columns_key(key):
    rows = [int(''.join(key[i:i + 4]), 2) for i in range(0, len(key), 4)]

    rows = mix_columns(rows)

    rows = ['0' * (4 - len(bin(row)[2:])) + bin(row)[2:] for row in rows]

    result = ''.join(rows)

    return result


# Inverse mix key columns
def inverse_mix_columns_key(key):
    rows = [int(''.join(key[i:i + 4]), 2) for i in range(0, len(key), 4)]

    rows = inverse_mix_columns(rows)

    rows = ['0' * (4 - len(bin(row)[2:])) + bin(row)[2:] for row in rows]

    return ''.join(rows)


# encrypt_round1() using Key1 on plaintext, P, and get intermediate state X
def encrypt_round1(plaintext, key1):
    # Substitute nibbles operation
    intermediate_ciphertext = substitute_nib(plaintext[:8]) + substitute_nib(plaintext[-8:])

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
    ciphertext = substitute_nib(intermediate_ciphertext[:8]) + substitute_nib(intermediate_ciphertext[-8:])

    # Shift Rows operation
    ciphertext = shift_rows(ciphertext)

    # Add Round Key operation
    ciphertext = xor_str(ciphertext, key2)

    return ciphertext


def encryption(plaintext, key):
    key0, key1, key2 = key_expansion(key)
    print(f"key0: {key0}, key1: {key1}, key2: {key2}") #print keys for checking
    intermediate_ciphertext = encrypt_round1(plaintext, key1)
    ciphertext = encrypt_round2(intermediate_ciphertext, key2)

    return ciphertext

# decrypt_round2() using Key 2 on the ciphertext, C, and get intermediate state, X
def decrypt_round2(ciphertext, key2):
    # Add Round Key operation with key2
    intermediate_plaintext = xor_str(ciphertext, key2)

    # Shift Rows operation
    intermediate_plaintext = shift_rows(intermediate_plaintext)

    # Substitute nibbles operation
    intermediate_plaintext = inverse_substitute_nib(intermediate_plaintext[:8]) + inverse_substitute_nib(intermediate_plaintext[-8:])

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
    plaintext = inverse_substitute_nib(plaintext[:8]) + inverse_substitute_nib(plaintext[-8:])

    return plaintext


# Encryption operation in reverse order
def decryption(ciphertext, key):
    key0, key1, key2 = key_expansion(key)

    intermediate_plaintext = decrypt_round2(ciphertext, key2)
    plaintext = decrypt_round1(intermediate_plaintext, key1)

    return plaintext

# Initial meet in the middle attack using all possible Key1 and Key2 values
# Returns all potential Key1 and Key2 pairs
def meet_in_the_middle_attack(known_plaintext, known_ciphertext):
    potential_keys = []
    #setting up dictionary to store first round enc result with potential key1 vals
    first_round_encryption_results = {}
    #loop iterates through all possible Key1 values, each potential Key1 is generated using generate_key(potential_key1)
    #encrypt_round1 is then used to encrypt the known_plaintext with the current Key1
    for potential_key1 in range(0, 1 << 16):
        key1 = generate_key(potential_key1)
        intermediate_ciphertext = encrypt_round1(known_plaintext, key1)
        first_round_encryption_results[intermediate_ciphertext] = key1
    #loop iterates through all possible Key2 values. each potential Key2 is generated using generate_key(potential_key2).
    #known_ciphertext is decrypted using decrypt_round2 with current Key2
    #then check if the resulting intermediate plaintext exists as key in first_round_encryption_results.
    for potential_key2 in range(0, 1 << 16):
        key2 = generate_key(potential_key2)
        intermediate_plaintext = decrypt_round2(known_ciphertext, key2)

        #if theres a match, intermediate plaintext from decrypting the known_ciphertext with Key2 matches the intermediate
        #ciphertext obtained from encrypting the known_plaintext with Key1.
        if intermediate_plaintext in first_round_encryption_results:
            found_key1 = first_round_encryption_results[intermediate_plaintext]
            #print(f"potential key pair: {found_key1}, {key2}")
            #takes potential Key1 and Key2, and checks if encrypting the known_plaintext with these keys yields known_ciphertext
            generated_ciphertext = encrypt_round1(known_plaintext, found_key1)
            generated_ciphertext = encrypt_round2(generated_ciphertext, key2)
            if generated_ciphertext == ciphertext:
                potential_keys.append({'key1': found_key1, 'key2': key2})

    return potential_keys

# Iterative rounds of meet in the middle attack using all potential Key1 and Key2 values generated from previous attack
def iter_mitm_attack(known_plaintext, known_ciphertext, test_keys):
    potential_keys = []
    #loop iterates through all test_key pair values
    #encrypt_round1 is then used to encrypt the known_plaintext with the current key1
    #decrypt_round2 is then used to decrypt the known_ciphertext with the current key2
    for key_pairs in test_keys:
        #print("Testing key pair: ", key_pairs)
        #print("Testing Known Plaintext: ", known_plaintext)
        #print("Testing Known Ciphertext: ", known_ciphertext)
        key1 = key_pairs['key1']
        intermediate_ciphertext = encrypt_round1(known_plaintext, key1)
        key2 = key_pairs['key2']
        intermediate_plaintext = decrypt_round2(known_ciphertext, key2)
        if intermediate_ciphertext == intermediate_plaintext:
                potential_keys.append({'key1': key1, 'key2': key2})

    return potential_keys



if __name__ == '__main__':
    # NYU student ID number (N number)
    key = 214348990
    letter1 = 'D'
    letter2 = 'S'

    generated_key = generate_key(key)

    generated_plaintext = generate_plaintext(letter1, letter2)

    print('Student ID: ' + str(key))
    print('Generated key: ' + generated_key)
    print('First letter of the student’s first name: ' + letter1)
    print('First letter of the student’s last name: ' + letter2)
    print('Generated plaintext: ' + generated_plaintext)

    ciphertext = encryption(generated_plaintext, generated_key)
    print("Encrypted ciphertext: ", ciphertext)
    
    plaintext = decryption(ciphertext, generated_key)
    print("Decrypted plaintext: ", plaintext)
    print("Recovered Initials: ", convert_to_text(plaintext))

    # Starting MITM attack
    print("Round 1 of MITM attack")
    print('Known plaintext: ' + generated_plaintext)
    print("Known ciphertext: ", ciphertext)

    # Generate possible key1 and key2 pairs using meet_in_the_middle_attack
    keys = meet_in_the_middle_attack(generated_plaintext, ciphertext)
    if len(keys) == 1:
        print("Keys found: Key 1:", keys[0][0], " Key 2: ", keys[0][1])
    else:
        print("Count of potential keys after attack round 1 : ", len(keys))
        print("Unable to find the matched keys with single known plaintext/ciphertext pair, too many potential keys found!")
        
        # set up 4 more plaintext and ciphertext pairs for 4 additional rounds of attack
        letter_sets = [('M','M'),('P','H'),('M','I'),('E','A')]
        i=0
        while len(keys) > 1:
            letter1 = letter_sets[i][0]
            letter2 = letter_sets[i][1]
            generated_plaintext = generate_plaintext(letter1, letter2)
            ciphertext = encryption(generated_plaintext, generated_key)
            print("Round",i+2,"of MITM attack")
            print('First letter of the student’s first name: ' + letter1)
            print('First letter of the student’s last name: ' + letter2)
            print('Known plaintext: ' + generated_plaintext)
            print("Known ciphertext: ", ciphertext)

            # Generate possible key1 and key2 pairs using interative iter_mitm_attack 
            keys = iter_mitm_attack(generated_plaintext, ciphertext, keys)
            if len(keys) == 1:
                print("Keys found: Key 1:", keys[0]['key1'], " Key 2: ", keys[0]['key2'])
                break
            else:
                print("Count of potential keys after attack round",i+2,": ", len(keys))
                print("Unable to find the matched keys with", i+2, "known plaintext/ciphertext pairs, too many potential keys found!")
            if i >= 3:
                break
            else:
                i+=1