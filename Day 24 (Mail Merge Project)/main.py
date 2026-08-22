PLACEHOLDER = "[name]"

with open("./Input/Names/invited_names.txt") as names_file:
    names = names_file.readlines()

with open("./Input/Letters/starting_letter.txt") as letters_file:
    letter_main = letters_file.read()
    for name in names:
        proper_name = name.strip()
        out_letter = letter_main.replace(PLACEHOLDER, proper_name)
        with open(f"./Output/ReadyToSend/letter_for_{proper_name}.txt", "w") as completed_letter:
            completed_letter.write(out_letter)
