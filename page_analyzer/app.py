from flask import Flask
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

@app.route("/")
def home():
    return "Егор лох"
