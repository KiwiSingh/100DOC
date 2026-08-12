from globals import logo, clear_screen
import random

def main_game():
    print(logo)
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    difficulty = input("Choose a difficulty. Type 'easy' or 'hard': ")
    number_to_guess = random.randint(1, 100)
    if difficulty == "easy":
        counter_easy = 10
        is_game_over = False
        while not is_game_over:
            print(f"You have {counter_easy} attempts remaining to guess the number.")
            guess = int(input("Make a guess: "))
            if guess == number_to_guess:
                is_game_over = True
                print("Congratulations, you guessed the number.")
            elif guess < number_to_guess:
                counter_easy -= 1
                print("""
                Too low.
                Guess again.
                """)
            elif guess > number_to_guess:
                counter_easy -= 1
                print("""
                Too high.
                Guess again.
                """)

            if counter_easy == 0 and guess != number_to_guess:
                is_game_over = True
                print(f"You're out of guesses! The number was {number_to_guess}")
                go_again = input("Do you want to play again? (y/n): ")
                if go_again == "y":
                    clear_screen()
                    main_game()
                else:
                    break

    elif difficulty == "hard":
        counter_hard = 5
        is_game_over = False
        while not is_game_over:
            print(f"You have {counter_hard} attempts remaining to guess the number.")
            guess = int(input("Make a guess: "))
            if guess == number_to_guess:
                is_game_over = True
                print("Congratulations, you guessed the number.")
            elif guess < number_to_guess:
                counter_hard -= 1
                print("""
                Too low.
                Guess again.""")
            elif guess > number_to_guess:
                counter_hard -= 1
                print("""
                Too high.
                Guess again.
                """)
            if counter_hard == 0 and guess != number_to_guess:
                is_game_over = True
                print(f"You're out of guesses! The number was {number_to_guess}")
                go_again = input("Do you want to play again? (y/n): ")
                if go_again == "y":
                    clear_screen()
                    main_game()
                else:
                    break
    else:
        print("That's not a valid difficulty option, ano baka.")
        main_game()


main_game()