from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
REPS = 0
CHECK_STRING = "✓"
timer = None
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(timer)
    pomo_canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", font=(FONT_NAME, 80, "bold"), fg=GREEN, bg=YELLOW)
    checkmark.config(text="", font=(FONT_NAME, 40), fg=GREEN, bg=YELLOW)
    global REPS
    REPS = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global REPS
    REPS += 1
    if REPS % 2 == 1:
        timer_label.config(text="Work", font=(FONT_NAME, 80, "bold"), fg = GREEN, bg = YELLOW)
        count_down(WORK_MIN * 60)
    elif REPS % 2 == 0 and REPS != 8:
        timer_label.config(text="Short break", font=(FONT_NAME, 80, "bold"), fg=PINK, bg=YELLOW)
        count_down(SHORT_BREAK_MIN * 60)
        checkmark.config(text=CHECK_STRING * (REPS//2))
    elif REPS == 8:
        timer_label.config(text="Long break", font=(FONT_NAME, 80, "bold"), fg=RED, bg=YELLOW)
        count_down(LONG_BREAK_MIN * 60)
        checkmark.config(text=CHECK_STRING*4)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = "0" + str(count_sec)
    pomo_canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
timer_label = Label(text="Timer", font=(FONT_NAME, 80, "bold"), fg=GREEN, bg=YELLOW)
timer_label.grid(row=0, column=1)
pomo_canvas = Canvas(width=500, height=500, bg=YELLOW, highlightthickness=0)
pomo_img = PhotoImage(file="tomato.png")
pomo_canvas.create_image(250, 250, image=pomo_img)
timer_text = pomo_canvas.create_text(255, 270, text="00:00", fill="white", font=(FONT_NAME, 40, "bold"))
pomo_canvas.grid(row=1, column=1)
start_button = Button(text="Start", highlightthickness=0, bg=YELLOW, command=start_timer)
start_button.grid(row=2, column=0)
reset_button = Button(text="Reset", highlightthickness=0, bg=YELLOW, command=reset_timer)
reset_button.grid(row=2, column=2)
checkmark = Label(text="", font=(FONT_NAME, 40), fg=GREEN, bg=YELLOW)
checkmark.grid(row=3, column=1)
window.mainloop()