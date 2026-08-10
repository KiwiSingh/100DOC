import os
import art
print(art.logo)

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    elif os.getenv("TERM"):
        os.system("clear")
    else:
        print("\n" * 50)

def find_highest_bidder(bidding_record):
    winner = max(bidding_record, key=bidding_record.get)
    highest_bid = max(bidding_record.values())
    print(f"The winner is {winner} with a bid of ${highest_bid}")




bids = {}
continue_bidding = True
while continue_bidding:
    name = input("Enter your name: ")
    bid = int(input("Enter your bid: $"))
    bids[name] = bid
    should_continue = input("Are there any other bidders? Type 'yes or 'no'.\n").lower()
    if should_continue == "no":
        continue_bidding = False
        find_highest_bidder(bids)
    elif should_continue == "yes":
        clear_screen()