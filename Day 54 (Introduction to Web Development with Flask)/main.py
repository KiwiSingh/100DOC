from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/bye")
def bye():
    return "Never gonna say goodbye. Never gonna tell a lie and hurt you."

if __name__ == "__main__":
    app.run()

