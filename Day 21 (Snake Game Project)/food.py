from turtle import Turtle
import random

class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.shapesize(stretch_len=0.5,stretch_wid=0.5)
        self.color("chocolate")
        self.speed("fastest")
        random_x = random.randint(-1060,1060)
        random_y = random.randint(-1060,1060)
        self.goto(random_x,random_y)
        self.refresh()

    def refresh(self):
        random_x = random.randint(-1060,1060)
        random_y = random.randint(-1060,1060)
        self.goto(random_x,random_y)