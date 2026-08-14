from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

my_profit = MoneyMachine()
ingredients_inventory = CoffeeMaker()
menu = Menu()

is_on = True
while is_on:
    options = menu.get_items()
    user_choice = input(f"What would you like? ({options}): ")
    if user_choice == "off":
        is_on = False
        break
    elif user_choice == "report":
        my_profit.report()
        ingredients_inventory.report()
    else:
        drink = menu.find_drink(user_choice)
        if ingredients_inventory.is_resource_sufficient(drink):
            if my_profit.make_payment(drink.cost):
                ingredients_inventory.make_coffee(drink)

