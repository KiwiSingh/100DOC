import random
from globals import clear_screen, logo


def deal_card():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    card = random.choice(cards)
    return card


def calculate_score(cards):
    while sum(cards) > 21 and 11 in cards:
        cards.remove(11)
        cards.append(1)

    return sum(cards)


def is_blackjack(cards):
    if calculate_score(cards) == 21 and len(cards) == 2:
        return True
    elif calculate_score(cards) > 21:
        return False
    else:
        return False


def compare_scores(userscore, computerscore):
    if userscore > computerscore and userscore <= 21:
        return "User wins!"
    elif userscore > 21:
        return "Computer wins!"
    elif computerscore > 21:
        return "User wins!"
    elif userscore == computerscore:
        return "Draw!"
    else:
        return "Computer wins!"


def bj_game():
    print(logo)
    usercards = []
    computercards = []

    for _ in range(2):
        usercards.append(deal_card())
        computercards.append(deal_card())
    print(f"Your first hand: {usercards}")
    print(f"Computer's first card: {computercards[0]}")

    userscore = calculate_score(usercards)
    computerscore = calculate_score(computercards)

    is_game_over = False

    while not is_game_over:
        if not is_blackjack(computercards) and not is_blackjack(usercards):
            draw_another_card = input("Would you like to draw another card? (y/n): ")

            if draw_another_card == "y":
                usercards.append(deal_card())
                userscore = calculate_score(usercards)

                if userscore > 21:
                    print(f"Your final hand: {usercards}")
                    print(f"Computer final hand: {computercards}")
                    print(f"User score: {userscore}")
                    print(f"Computer score: {computerscore}")
                    print(compare_scores(userscore, computerscore))
                    is_game_over = True

            else:
                while computerscore < 17:
                    computercards.append(deal_card())
                    computerscore = calculate_score(computercards)

                userscore = calculate_score(usercards)
                computerscore = calculate_score(computercards)
                print(f"Your final hand: {usercards}")
                print(f"Computer final hand: {computercards}")
                print(f"User score: {userscore}")
                print(f"Computer score: {computerscore}")
                print(compare_scores(userscore, computerscore))
                is_game_over = True

        elif is_blackjack(computercards) and is_blackjack(usercards):
            userscore = calculate_score(usercards)
            computerscore = calculate_score(computercards)
            print(f"User score: {userscore}")
            print(f"Computer score: {computerscore}")
            print("Computer wins!")
            is_game_over = True

        elif is_blackjack(usercards) and not is_blackjack(computercards):
            userscore = calculate_score(usercards)
            computerscore = calculate_score(computercards)
            print(f"User score: {userscore}")
            print(f"Computer score: {computerscore}")
            print("User wins!")
            is_game_over = True

        else:
            userscore = calculate_score(usercards)
            computerscore = calculate_score(computercards)
            print(f"User score: {userscore}")
            print(f"Computer score: {computerscore}")
            print(f"Your final hand: {usercards}")
            print(f"Computer final hand: {computercards}")
            print(compare_scores(userscore, computerscore))
            is_game_over = True


while input("Do you want to play a game of Blackjack? (y/n): ").lower() == "y":
    clear_screen()
    bj_game()