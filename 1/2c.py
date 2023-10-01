import operator
from collections import Counter

#Set up cipher text and English letters (other than "LIBERTY" and "THE") to suggest ranked by frequencies
cipher_text = "TNFOSFOZSWPZLOCGQAOZWAGQRPJZPNABCZPQDOGRAMTHARAXTBAGZJOGMTHARAVAPZW"
letter_suggest = "AONSDCUMWFGPVKJXQZ"
letter_frequencies = {}
total_letters = 0

for letter in cipher_text:
    if letter.isalpha():
        letter = letter.upper()
        letter_frequencies[letter] = letter_frequencies.get(letter, 0) + 1
        total_letters += 1

relative_frequencies = {letter: frequency / total_letters for letter, frequency in letter_frequencies.items()}

#Search for "LIBERTY" as 7-letters non-duplicate string
strings_with_7_letters = []
for i in range(len(cipher_text) - 6):
    substring = cipher_text[i:i+7]
    if len(set(substring)) == 7:
        strings_with_7_letters.append(substring)

#Check 7-letters non-duplicate strings where letter 4 and 6 have the two highest relative frequencies as in E and T in LIBERTY
strings_with_highest_freqs = []
for string in strings_with_7_letters:
    frequencies = [relative_frequencies[letter] for letter in string]
    sorted_freqs = sorted(frequencies, reverse=True)
    if frequencies[3] == sorted_freqs[0] and frequencies[5] == sorted_freqs[1]:
        strings_with_highest_freqs.append(string)

#Check resulting strings where the highest letter relative frequency is more than 7 times the lowest frequency as B vs Y or B
final_strings = []
for string in strings_with_highest_freqs:
    frequencies = [relative_frequencies[letter] for letter in string]
    max_freq = max(frequencies)
    min_freq = min(frequencies)
    if max_freq > 7 * min_freq:
        final_strings.append(string)

print("Cipher text is:", cipher_text)
print("LIBERTY is matched to", final_strings[0])

#Create alphabet letter substitution table to decrypt cipher text
substitution_table = {}
for i, letter in enumerate(final_strings[0]):
    substitution_table[letter] = "LIBERTY"[i] if i < len("LIBERTY") else "_"

#Store cipher letters to decrypt in cipher_letters and rank by decreasing relative frequencies
cipher_letters = sorted(set(cipher_text), key=lambda x: relative_frequencies[x], reverse=True)

#Remove letters of matched string from cipher letters pending decryption
cipher_letters = [letter for letter in cipher_letters if letter not in final_strings[0]]

#Search for THE using decrypted T and E from LIBERTY
strings_with_3_letters = []
for i in range(len(cipher_text) - 2):
    substring = cipher_text[i:i+3]
    if substring[0] == final_strings[0][5] and substring[2] == final_strings[0][3]:
        strings_with_3_letters.append(substring)
print("THE is matched to", strings_with_3_letters[0])

#Update alphabet letter substitution table with matched letter H
substitution_table[strings_with_3_letters[0][1]] = "H"

#Remove solved THE from cipher letters pending decryption
cipher_letters.remove(strings_with_3_letters[0][1])

#Convert cipher text to plaintext using solved letters so far
plaintext = "".join(substitution_table.get(letter, "_") for letter in cipher_text)

# Step 13: Print cipher text and solved plaintext so far
print("Cipher text is:  ", cipher_text)
print("Plaintext so far:", plaintext)

#Cycle through each unsolved cipher letter and suggest English letters ranked by frequencies
while cipher_letters != []:

    #Print cipher_letter to solve one by one
    print("Remaining cipher letter to solve:", cipher_letters[0])

    #Setup 1st plaintext letter to suggest
    n = 1
    match = False

    while match == False:
        #Suggest plaintext letter to match the cipuer letter based on relative frequencies
        print("Plaintext letter suggestion:", letter_suggest[n-1])

        #Update alphabet letter substitution table by mapping cipher letter to suggested plaintext letter
        substitution_table[cipher_letters[0]] = letter_suggest[n-1]

        #Set up decrypted plaintext based on suggested plaintext letter
        plaintext = "".join(substitution_table.get(letter, "_") for letter in cipher_text)

        #Print plaintext based on suggested letter
        print("Plaintext based on suggested letter:", plaintext)

        #Check if user agrees with suggested letter
        user_input = input("Is the suggested letter correct? <Y or N>: ")

        #If user accepts suggestion, remove cipher_letters from pending list and remove suggested letter from suggetion list
        if user_input == "Y" or user_input == "y" or user_input == "yes" or user_input == "Yes":
            cipher_letters = cipher_letters[1:]
            letter_suggest = letter_suggest[:n-1] + letter_suggest[n:]
            match = True

        #End execution if all cipher letters are solved
        if not cipher_letters:
            print("Decrypted plaintext is: ", plaintext)
            break

        #Continue to next plaintext letter suggestion if user rejects suggestion, back to 1st suggestion if last one is rejected
        if n < len(letter_suggest):
            n += 1
        else:
            n = 1

