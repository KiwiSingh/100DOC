from globals import logo, clear_screen
import random

def main_game(attempts):
    number_to_guess = random.randint(1, 100)
    counter = attempts
    is_game_over = False
    while not is_game_over:
        print(f"You have {counter} attempts remaining to guess the number.")
        guess = int(input("Make a guess: "))
        if guess == number_to_guess:
            is_game_over = True
            print("Congratulations, you guessed the number.")
        elif guess < number_to_guess:
            counter -= 1
            print("""
            Too low.
            Guess again.
            """)
        elif guess > number_to_guess:
            counter -= 1
            print("""
            Too high.
            Guess again.
            """)

        if counter == 0 and guess != number_to_guess:
            is_game_over = True
            print(f"You're out of guesses! The number was {number_to_guess}")
            go_again = input("Do you want to play again? (y/n): ")
            if go_again == "y":
                clear_screen()
                main_game(attempts)
            else:
                break

print(logo)
print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")
difficulty = input("Choose a difficulty. Type 'easy' or 'hard': ")
if difficulty == "easy":
    attempts = 10
    main_game(attempts)
elif difficulty == "hard":
    attempts = 5
    main_game(attempts)
else:
    print("You have chosen an invalid difficulty. The game will exit now.")
    is_game_over = True
    while is_game_over:
        break