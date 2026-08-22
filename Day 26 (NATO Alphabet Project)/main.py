import pandas as pd
nato_alphabet = pd.read_csv("nato_phonetic_alphabet.csv")
#TODO 1. Create a dictionary in this format:
{"A": "Alfa", "B": "Bravo"}

nato_alphabet_dict = {row.letter:row.code for (index, row) in nato_alphabet.iterrows()}
name = input("What is your name? ")
nato_name = [nato_alphabet_dict[letter.upper()] for letter in name if letter.upper() in nato_alphabet_dict]
print(nato_name)


#TODO 2. Create a list of the phonetic code words from a word that the user inputs.

