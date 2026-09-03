from flask import Flask
import random

random_number = random.randint(0, 9)

app = Flask(__name__)

@app.route("/")
def home_page():
    return "<h1>Welcome to the Higher or Lower Game!</h1><p>Guess a number between 0 and 9.</p>" \
            "<img src = 'https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif' />"

@app.route("/<int:guess>")
def guess_number(guess):
    if guess < random_number:
        return "<h1>Too low, try again!</h1><img src = 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExODRnd3NhZGRlN2xscWxodDVsNHUzcjJ5bHB6M2s3bXY0Zm5zMDFpbSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/y31rRE5h3wyPXey8vx/giphy.gif' />"
    elif guess > random_number:
        return "<h1>Too high, try again!</h1><img src = 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeHlvM3c4aGcwdWxwaDZmNDJ6ZDM5c3kzbWxkNGt3bXQ3MHczZGVtNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/TJufnSz934AnK/giphy.gif' />"
    else:
        return "<h1>You found me!</h1><img src = 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWRoZW5sejg0N243bzJyMXp0enByb25oNWRjbWNrZnFpN28xOXN3dCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/4fLTgnoXPzh3iW80SY/giphy.gif' />"


if __name__ == "__main__":
    app.run(debug=True)