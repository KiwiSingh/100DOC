import pandas as pd
import turtle
screen = turtle.Screen()
screen.title("US States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

states = pd.read_csv("50_states.csv")["state"].tolist()
states_with_coordinates = pd.read_csv("50_states.csv")
guessed_states = []
states_to_learn = []
game_is_on = True
while game_is_on:
    answer_state = screen.textinput(title=f"{len(guessed_states)}/50 states guessed", prompt="What's another state's name?").title()
    if answer_state == "Exit":
        for state in states:
            if state not in guessed_states:
                states_to_learn.append(state)
            pd.DataFrame(states_to_learn).to_csv("states_to_learn.csv")
        break
    if answer_state in states:
        guessed_states.append(answer_state)
        text = turtle.Turtle()
        text.hideturtle()
        text.penup()
        state_data = states_with_coordinates[states_with_coordinates.state == answer_state]
        text.goto(int(state_data.x.item()), int(state_data.y.item()))
        text.write(answer_state)
        screen.update()
    if answer_state not in guessed_states:
        states_to_learn.append(answer_state)

    if len(guessed_states) == 50:
        game_is_on = False
