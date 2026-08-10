import art
import os
def clear_screen():
    if os.name == "nt":
        os.system("cls")
    elif os.getenv("TERM"):
        os.system("clear")
    else:
        print("\n" * 50)

def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

def exponent(n1, n2):
    return n1 ** n2

operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "^": exponent
}

def calculatron():
    print(art.logo)
    store_result = True
    num1 = float(input("Enter first number: "))

    while store_result:
        for symbol in operations:
            print(symbol)
        operation = input("Pick an operation: ")
        num2 = float(input("What is the next number?: "))
        answer = operations[operation](num1, num2)
        print(f"{num1} {operation} {num2} = {answer}")

        choice = input(f"Type 'y' to continue calculating with {answer}, type 'n' to start a new calculation, or type 'q' to quit: ")

        if choice == "y":
            num1 = answer
        elif choice == "n":
            store_result = False
            clear_screen()
            calculatron()
        elif choice == "q":
            clear_screen()
            break
        else:
            clear_screen()
            print("Invalid input. Program will exit now.")
            break

calculatron()



