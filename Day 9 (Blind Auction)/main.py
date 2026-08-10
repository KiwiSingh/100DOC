# TODO-1: Ask the user for input
# TODO-2: Save data into dictionary {name: price}
# TODO-3: Whether if new bids need to be added
# TODO-4: Compare bids in dictionary

import art
print(art.logo)

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
    should_continue = input("Are there any other bidders? Type 'yes or 'no'.\n")
    if should_continue == "no":
        continue_bidding = False
        find_highest_bidder(bids)
    elif should_continue == "yes":
        print("\n" * 50)