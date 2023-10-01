import string
def substitute_decrypt(ciphertext, key):
    alphabet = string.ascii_uppercase
    substitution = {alphabet[i]: key[i] for i in range(len(alphabet))}
    plaintext = []
    for char in ciphertext:
        decrypted_char = substitution[char]
        decrypted_char = decrypted_char.upper()
        plaintext.append(decrypted_char)
    return ''.join(plaintext)

def calculate_letter_occurrences(input_string):
    occurrences = {}
    for char in input_string:
        if char in occurrences:
            occurrences[char] += 1
        else:
            occurrences[char] = 1
    return occurrences

if __name__ == "__main__":
    ciphertext = "TNFOSFOZSWPZLOCGQAOZWAGQRPJZPNABCZPQDOGRAMTHARAXTBAGZJOGMTHARAVAPZW"
    letter_occurrences = calculate_letter_occurrences(ciphertext)

    for letter, count in letter_occurrences.items():
        print(f"{letter}: {count}")
    # alph = "abcdefghijklmnopqrstuvwxyz"
    key = "ebufrnrviykcgkoasmwiudhlyt"
    # frequency_order = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd','l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j','z']

    decrypted_text = substitute_decrypt(ciphertext, key)
    print("Decrypted Text:", decrypted_text)