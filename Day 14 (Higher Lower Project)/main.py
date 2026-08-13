import random
from globals import logo, vs, clear_screen, data

def choose_a_random_person(account):
    random_person = account["name"]
    description = account["description"]
    country = account["country"]

    return f"{random_person}, a {description}, from {country}"

def compare_followers(user_guess, a_followers, b_followers):
    if a_followers > b_followers:
        return user_guess == "a"
    elif b_followers > a_followers:
        return user_guess == "b"
    else:
        return True


print(logo)
score = 0
game_should_continue = True
account_b = random.choice(data)
while game_should_continue:
    account_a = account_b
    account_b = random.choice(data)

    while account_a == account_b:
        account_b = random.choice(data)

    print(f"Compare {choose_a_random_person(account_a)}")
    print(vs)
    print(f"{choose_a_random_person(account_b)}")

    guess = input("Who has more followers? A or B: ").lower()
    clear_screen()
    a_followers = account_a["follower_count"]
    b_followers = account_b["follower_count"]

    is_correct = compare_followers(guess, a_followers, b_followers)
    if is_correct:
        score += 1
        print(f"You are correct! Current score is {score}")
    else:
        print(f"Sorry, you are wrong! Current score is {score}")
        game_should_continue = False
