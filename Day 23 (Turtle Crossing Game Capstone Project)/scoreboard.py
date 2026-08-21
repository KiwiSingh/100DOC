from turtle import Turtle
import random

COLORS = ["black", "golden", "blue", "purple"]
FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.level = 1
        self.hideturtle()
        self.penup()
        self.goto(-280, 250)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Level: {self.level}", align="left", font=FONT)

    def game_over(self):
        self.hideturtle()
        self.penup()
        self.goto(0, 0)
        self.pencolor(random.choice(COLORS))
        self.write(f"GAME OVER", align="center", font=FONT)
        self.goto(0, -50)
        self.write(f"Designed by Kiwi Singh", align="center", font=FONT)


    def increase_score(self):
        self.level += 1
        self.update_scoreboard()

