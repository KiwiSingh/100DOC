"""
This part defines the coffee machine menu.
"""

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}


"""
This part defines the initial amount of money and resources in the coffee machine.
"""
profit = 0
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}


"""

This function checks if the resources in the coffee machine are sufficient, and returns True if they
are, otherwise returns False.

"""
def resources_sufficient(order_ingredients):
    for item in order_ingredients:
        if order_ingredients[item] > resources[item]:
            print(f"Sorry, there is not enough {item}.")
            return False

    return True

"""

This function processes the amount of coins the user provides.

"""
def process_coins():
    print("Please insert coins.")
    total = int(input("how many quarters?: ")) * 0.25
    total += int(input("how many dimes?: ")) * 0.1
    total += int(input("how many nickles?: ")) * 0.05
    total += int(input("how many pennies?: ")) * 0.01
    return total


"""

This function checks if the user provided sufficient money for the required coffee, and returns
True if it is, and returns False and refunds the money if it isn't.

"""
def is_transaction_successful(user_money, item_cost):
    if user_money >= item_cost:
        change_amount = round(user_money - item_cost, 2)
        print(f"Here is ${change_amount} in change.")
        global profit
        profit += item_cost
        return True
    else:
        print("Sorry! That's not enough money. Money refunded.")
        return False


"""

This function runs only after resource checks, and makes the user the requested coffee.

"""

def make_coffee(recipe, ingredients):
    for item in ingredients:
        resources[item] -= ingredients[item]
    print(f"Here is your {recipe} ☕️. Enjoy! ")

"""

The coffee machine is set to on by default. The while loop below iterates through
user choices, including invalid ones.

"""
is_on = True
while is_on:
    user_choice = input("What would you like? (espresso/latte/cappuccino): ")
    if user_choice == "off":
        is_on = False
    elif user_choice == "report":
        print(f"Water: {resources['water']}ml")
        print(f"Milk: {resources['milk']}ml")
        print(f"Coffee: {resources['coffee']}g")
        print(f"Money: ${profit}")
    elif user_choice in MENU:
        drink = MENU[user_choice]
        if resources_sufficient(drink["ingredients"]):
            user_money = process_coins()
            if is_transaction_successful(user_money, drink["cost"]):
                make_coffee(user_choice, drink["ingredients"])
    else:
        print("Invalid choice. Please try again.")

