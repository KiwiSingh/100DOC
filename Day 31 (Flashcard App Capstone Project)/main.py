#----------------------------------IMPORTS--------------------------------#
from tkinter import *
import pandas as pd
import random

#---------------------------------CONSTANTS-------------------------------#
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
words_dict_list = {}
words_pool = list(words_dict_list)

#------------------------FLASH CARD CORE FUNCTIONS-----------------------#

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/dutch_words.csv")
    words_dict_list = original_data.to_dict(orient="records")
else:
    words_dict_list = data.to_dict(orient="records")


def pick_random_dutch_word(remove=False):
    global words_pool, flip_timer
    window.after_cancel(flip_timer)
    if remove:
        if not words_pool:
            words_pool = list(words_dict_list)
        random_word_with_tl = random.choice(words_pool)
        words_pool.remove(random_word_with_tl)
        pd.DataFrame(words_pool).to_csv("data/words_to_learn.csv", index=False)
    else:
        random_word_with_tl = random.choice(words_dict_list)
    global current_card
    current_card = random_word_with_tl
    random_word = current_card["Dutch"]
    flash_canvas.itemconfig(card_background, image=front_image)
    flash_canvas.itemconfig(word, text=random_word, fill="black")
    flash_canvas.itemconfig(lang_text, text="Dutch", fill="black")
    flip_timer = window.after(3000, func=flip_cards)

def pick_random_dutch_word_no_remove():
    pick_random_dutch_word(remove=False)

def pick_random_dutch_word_with_removal():
    pick_random_dutch_word(remove=True)

def flip_cards():
    flash_canvas.itemconfig(lang_text, text="English", fill="white")
    flash_canvas.itemconfig(word, text=current_card["English"], fill="white")
    flash_canvas.itemconfig(card_background, image=back_image)

#---------------------------------UI-------------------------------------#

window = Tk()
window.title("KiwiFlash: Learn Languages Through Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_cards)

flash_canvas = Canvas(width=800, height=526)
front_image = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")
card_background = flash_canvas.create_image(400, 263, image=front_image)
flash_canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
lang_text = flash_canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"), fill="black")
word = flash_canvas.create_text(400, 263, text="word", font=("Times New Roman", 60, "bold"), fill="black")
flash_canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=cross_image, command=pick_random_dutch_word_no_remove)
unknown_button.grid(row=1, column=0)
unknown_button.config(bg=BACKGROUND_COLOR, highlightthickness=0)

check_image = PhotoImage(file="./images/right.png")
known_button = Button(image=check_image, command=pick_random_dutch_word_with_removal)
known_button.grid(row=1, column=1)
known_button.config(bg=BACKGROUND_COLOR, highlightthickness=0)

pick_random_dutch_word_no_remove() # Init with a random word

window.mainloop()
