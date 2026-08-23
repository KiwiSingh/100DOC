from tkinter import *
window = Tk()
window.title("Miles to kilometers converter")
window.config(padx=20, pady=20)
window.minsize(300, 200)
miles_entry = Entry(window, width=7)
miles_entry.insert(0,"0")
miles_entry.grid(row=0, column=1)
miles_text = Label(window, text="miles")
miles_text.grid(row=0, column=2)
is_equal_to_text = Label(window, text="is equal to")
is_equal_to_text.grid(row=1, column=0)
km_conv = Label(window, text="0")
km_conv.grid(row=1, column=1)
km_text = Label(window, text="km")
km_text.grid(row=1, column=2)

def convert_to_kilometers():
    miles = miles_entry.get()
    try:
        kilometres = round((float(miles) * 1.609344), 2)
        km_conv.config(text=kilometres)
    except ValueError:
        km_conv.config(text="Error! Please enter a valid numerical value!")

convert_button = Button(window, text="Calculate", command=convert_to_kilometers)
convert_button.grid(row=2, column=1)
window.mainloop()