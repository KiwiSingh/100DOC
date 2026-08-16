from turtle import Turtle, Screen
import random
from tkinter import messagebox

is_race_on = False
screen = Screen()
screen.setup(width=1920, height=1080)
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")
colors = ["red", "orange", "yellow", "green", "blue", "purple", "chocolate"]
y_positions = [-480, -320, -160, 0, 160, 320, 480]
all_turtles = []


for turtle_index in range(0, 7):
    turt = Turtle(shape="turtle")
    turt.penup()
    turt.color(colors[turtle_index])
    turt.goto(x=-960, y=y_positions[turtle_index])
    all_turtles.append(turt)

if user_bet:
    is_race_on = True

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 940:
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                messagebox.showinfo(
                    "Race result",
                    f"You've won! The {winning_color} turtle is the winner!"
                )
            else:
                messagebox.showinfo(
                    "Race result",
                                    f"You've lost! The {winning_color} turtle is the winner!"
                                    )
        rand_dist = random.randint(0, 10)
        turtle.forward(rand_dist)

screen.exitonclick()