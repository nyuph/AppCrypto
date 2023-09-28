import collections

# Step 1: Check and store the relative frequencies of each letter in the cipher text
cipher_text = "TNFOSFOZSWPZLOCGQAOZWAGQRPJZPNABCZPQDOGRAMTHARAXTBAGZJOGMTHARAVAPZW"

letter_frequencies = collections.Counter(cipher_text)
total_letters = sum(letter_frequencies.values())

relative_frequencies = {}
for letter, count in letter_frequencies.items():
    relative_frequencies[letter] = count / total_letters

# Step 2: Find strings that contain 7 non-duplicate letters
def find_strings_with_7_letters(text):
    strings = []
    for i in range(len(text)-6):
        substring = text[i:i+7]
        if len(set(substring)) == 7:
            strings.append(substring)
    return strings

strings_with_7_letters = find_strings_with_7_letters(cipher_text)

# Step 3: Print the relative frequencies of letters in each string found in step 2
for string in strings_with_7_letters:
    string_frequencies = [relative_frequencies[letter] for letter in string]
    print(f"String: {string}")
    print(f"Relative Frequencies: {string_frequencies}")

# Step 4: Find and print strings in which letter 4 and letter 6 have the two highest relative frequencies
def find_strings_with_highest_frequencies(strings, relative_frequencies):
    result_strings = []
    highest_freqs = sorted(relative_frequencies.values(), reverse=True)[:2]

    for string in strings:
        if (relative_frequencies[string[3]] in highest_freqs) and (relative_frequencies[string[5]] in highest_freqs):
            result_strings.append(string)

    return result_strings

strings_with_highest_freqs = find_strings_with_highest_frequencies(strings_with_7_letters, relative_frequencies)

print("Strings with highest frequencies in positions 4 and 6:")
for string in strings_with_highest_freqs:
    print(string)

# Step 5: Find and print strings in which the highest letter relative frequency is more than 7 times the lowest letter relative frequency
def find_strings_with_frequency_ratio(strings, relative_frequencies):
    result_strings = []
    for string in strings:
        freqs = [relative_frequencies[letter] for letter in string]
        max_freq = max(freqs)
        min_freq = min(freqs)
        if max_freq > 7 * min_freq:
            result_strings.append(string)

    return result_strings

strings_with_frequency_ratio = find_strings_with_frequency_ratio(strings_with_highest_freqs, relative_frequencies)

print("Strings with highest frequency more than 7 times the lowest frequency:")
for string in strings_with_frequency_ratio:
    print(string)

# Step 6: Create an alphabet letter substitution table using the string from Step 5 and matching letters to "LIBERTY" and all others to "_"
def create_substitution_table(string):
    substitution_table = {}
    for i, letter in enumerate(string):
        substitution_table[letter] = "LIBERTY"[i % 7]
    
    for letter in set(cipher_text):
        if letter not in substitution_table:
            substitution_table[letter] = "_"
    
    return substitution_table

substitution_table = create_substitution_table(strings_with_frequency_ratio[0])

#print("Alphabet Letter Substitution Table:")
#for letter, substitution in substitution_table.items():
#    print(f"{letter}: {substitution}")

# Step 7: Convert ciphertext to plaintext using substitution table
plaintext = ''.join(substitution_table.get(letter, letter) for letter in cipher_text)

# Step 8: Print the resulting plaintext
print("Plaintext:")
print(plaintext)

# Step 9: Create a new list by removing duplicate letters from ciphertext and rank letters by decreasing relative frequencies
unique_letters = list(set(cipher_text))
ranked_letters = sorted(unique_letters, key=lambda letter: relative_frequencies[letter], reverse=True)

# print("Ranked Letters by Decreasing Relative Frequencies:")
# for letter in ranked_letters:
#    print(f"{letter}: {relative_frequencies[letter]}")

# Step 10: Remove letters contained in the string from step 5 from the new list
letters_to_remove = set(strings_with_frequency_ratio[0])
new_list = [letter for letter in ranked_letters if letter not in letters_to_remove]

# Step 11: Print the new list
print("New List after Removing Letters:")
print(new_list)
