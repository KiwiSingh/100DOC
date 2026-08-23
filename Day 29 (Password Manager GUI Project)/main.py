from tkinter import *
from tkinter import messagebox
KIWIPASS_LOGO = "logo.png"
import random
import pyperclip
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)
    password = "".join(password_list)
    password_input.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    if len(website_input.get()) == 0 or len(email_uname_input.get()) == 0 or len(password_input.get()) == 0:
        messagebox.showerror("Error", "Please enter all fields")
    else:
        is_ok = messagebox.askokcancel(title=website_input.get(),
                                       message=f"These are the details entered: \nEmail: {email_uname_input.get()}\nPassword: {password_input.get()}\nIs it ok to save?")
        if is_ok:
            pyperclip.copy(password_input.get())
            with open("data.txt", "a") as file:
                file.write(f"{website_input.get()} | {email_uname_input.get()} | {password_input.get()}")
                website_input.delete(0, END)
                password_input.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("KiwiPass: Your Trusty Password Manager")
window.config(bg="white", padx=50, pady=50)
kiwi_canvas = Canvas(width=200, height=200, background="white", highlightthickness=0)
kiwi_img_big = PhotoImage(file=KIWIPASS_LOGO)
kiwi_img = kiwi_img_big.subsample(4)
kiwi_canvas.create_image(100, 100, image=kiwi_img)
kiwi_canvas.grid(row=0, column=1)
website_text = Label(window, text="Website: ", bg="white", fg="black", font=("Arial", 18))
website_text.grid(row=1, column=0)
website_input = Entry(window, width=35)
website_input.focus()
website_input.grid(row=1, column=1, columnspan=2)
email_uname_text = Label(window, text="Email/Username: ", bg="white", fg="black", font=("Arial", 18))
email_uname_text.grid(row=2, column=0)
email_uname_input = Entry(window, width=35)
email_uname_input.grid(row=2, column=1, columnspan=2)
email_uname_input.insert(0, "kiwisingh@proton.me")
password_text = Label(window, text="Password: ", bg="white", fg="black", font=("Arial", 18))
password_text.grid(row=3, column=0)
password_input = Entry(window, width=18)
password_input.grid(row=3, column=1, columnspan=1)
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=33, highlightthickness=0, command=save_password)
add_button.grid(row=4, column=1, columnspan=2)
window.mainloop()



